from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from typing import List, Literal, Optional, Tuple
from services.simplex_service import resolver_simplex_tabular, generar_grafico_2d
# Importamos nuestros modelos centralizados
from schemas import SimplexRequest, SimplexResponse 
import uuid
import tempfile
import os
import logging
import base64

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/simplex",
    tags=["Simplex Solver"]
)

# --- Funciones Helper ---

def _cleanup_file(path: str) -> None:
    """Función de limpieza para borrar archivos temporales en background."""
    try:
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Archivo temporal eliminado: {path}")
    except Exception as e:
        logger.warning(f"No se pudo eliminar el archivo temporal {path}: {e}")

def _solve_and_get_mark_point(request: SimplexRequest) -> Optional[Tuple[float, float]]:
    """
    HELPER REFACTORIZADO: Resuelve el simplex y retorna el punto óptimo (x1, x2) o None.
    Esto elimina la duplicación en los endpoints de gráficos.
    """
    try:
        solve = resolver_simplex_tabular(
            problem_type=request.problem_type,
            C=request.C,
            LI=request.LI,
            LD=request.LD,
            O=request.O,
        )
        # Extraer punto óptimo si existe
        if solve.get("status") == "optimo" and solve.get("solucion"):
            vars_ = solve["solucion"]["variables"]
            mx = float(vars_.get("x1", 0.0))
            my = float(vars_.get("x2", 0.0))
            return (mx, my)
    except Exception as e:
        # Si falla la solución, al menos el gráfico se puede generar sin el punto
        logger.warning(f"Error al pre-resolver para el gráfico: {e}. Se graficará sin punto óptimo.")
    
    return None

# --- Endpoints de la API ---

@router.post("/solve-tabular", response_model=SimplexResponse)
async def solve_tabular(request: SimplexRequest):
    """
    Resuelve un problema Simplex y devuelve todas las tablas (iteraciones).
    """
    try:
        result = resolver_simplex_tabular(
            problem_type=request.problem_type,
            C=request.C,
            LI=request.LI,
            LD=request.LD,
            O=request.O
        )
        logger.info("Resolviendo problema simplex tabular.")
        return result
    except ValueError as e:
        logger.warning(f"Error de validación en /solve-tabular: {e}")
        raise HTTPException(status_code=400, detail=f"Datos inválidos: {e}")
    except Exception as e:
        logger.exception("Error interno en /solve-tabular")        
        raise HTTPException(status_code=500, detail="Ocurrió un error interno al resolver el problema.")

@router.post("/generate-graph")
async def generate_graph(request: SimplexRequest, background_tasks: BackgroundTasks):
    """
    Genera un gráfico del problema (solo 2D) y lo devuelve como un archivo PNG.
    """
    if len(request.C) != 2:
        raise HTTPException(status_code=400, detail="El gráfico solo puede generarse para problemas con exactamente 2 variables.")

    try:
        # Usamos el helper para obtener el punto óptimo
        mark = _solve_and_get_mark_point(request)

        # Generar gráfico como archivo temporal
        tmp_dir = tempfile.gettempdir()
        filename = f"simplex_graph_{uuid.uuid4().hex}.png"
        graph_path = os.path.join(tmp_dir, filename)
        
        saved_path = generar_grafico_2d(
            request.C,
            request.LI,
            request.LD,
            titulo="Gráfico de Restricciones y Función Objetivo",
            save_path=graph_path,
            mark_point=mark,
        )
        
        if not saved_path or not os.path.exists(saved_path):
            raise HTTPException(status_code=500, detail="No se pudo generar el gráfico.")
        
        # Programar eliminación del archivo después de enviar
        background_tasks.add_task(_cleanup_file, saved_path)
        
        logger.info(f"Generando gráfico como archivo: {filename}")
        return FileResponse(saved_path, media_type="image/png", filename="graph.png")
        
    except Exception as e:
        logger.exception("Error interno en /generate-graph")
        # Limpiar archivo si la respuesta falla antes de enviarse
        if 'graph_path' in locals() and os.path.exists(graph_path):
            _cleanup_file(graph_path)
        raise HTTPException(status_code=500, detail="Ocurrió un error al generar el gráfico.")

@router.post("/generate-graph-html", response_class=HTMLResponse)
async def generate_graph_html(request: SimplexRequest):
    """
    Genera un gráfico del problema (solo 2D) y lo devuelve incrustado en HTML.
    """
    if len(request.C) != 2:
        raise HTTPException(status_code=400, detail="Solo se puede graficar con exactamente 2 variables.")
    
    try:
        # Usamos el helper para obtener el punto óptimo
        mark = _solve_and_get_mark_point(request)

        # Generar gráfico como bytes en memoria
        raw_png = generar_grafico_2d(
            request.C,
            request.LI,
            request.LD,
            titulo="Gráfico de Restricciones y Función Objetivo",
            mark_point=mark,
            save_path=None # <-- Esto hace que retorne bytes
        )
        
        if not isinstance(raw_png, (bytes, bytearray)):
            raise HTTPException(status_code=500, detail="Error generando imagen en memoria.")
        
        # Convertir a Base64 para HTML
        b64 = base64.b64encode(raw_png).decode("ascii")
        html = f"""
        <html><head><title>Gráfico Simplex</title></head>
        <body style='font-family: Arial; text-align: center; padding: 20px;'>
        <h2>Gráfico de Restricciones y Función Objetivo</h2>
        <img src='data:image/png;base64,{b64}' alt='Grafico Simplex' style='max-width:90%;height:auto;border:1px solid #ccc;border-radius:8px;' />
        </body></html>
        """
        logger.info("Generando gráfico en HTML.")
        return HTMLResponse(content=html)
        
    except Exception as e:
        logger.exception("Error interno en /generate-graph-html")
        raise HTTPException(status_code=500, detail="Ocurrió un error al generar el gráfico en HTML.")