from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
import logging

# --- Importamos nuestros routers separados ---
from routers import simplex_router, pages_router

# --- Configuración de Logging ---
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Iniciando aplicación FastAPI...")

# --- Creación de la App ---
app = FastAPI(
    title="Simplex Solver API",
    description="API para resolver problemas de Programación Lineal con el método Simplex Tabular.",
    version="1.0.0"
)

# --- Manejador de Excepciones de Validación ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejador global para errores de validación de Pydantic."""
    logger.warning(f"Error de validación en {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Datos de entrada inválidos. Verifica el formato del JSON.", "errors": exc.errors()},
    )

# --- Montaje de Routers ---
# Incluimos los endpoints de las páginas HTML
app.include_router(pages_router.router) 
# Incluimos los endpoints de la API del Simplex
app.include_router(simplex_router.router)

# --- Montaje de Archivos Estáticos ---
# Esto sirve archivos como CSS y JS
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


logger.info("Aplicación lista. Servidor iniciado correctamente.")