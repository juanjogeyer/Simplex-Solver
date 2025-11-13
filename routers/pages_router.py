from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Rutas de Páginas Estáticas (HTML) ---
# Movimos esto desde main.py para mantenerlo limpio.

@router.get("/", response_class=HTMLResponse, tags=["Pages"])
async def get_html():
    """Sirve la página principal index.html."""
    try:
        with open("frontend/templates/index.html", "r", encoding="utf-8") as f:
            logger.info("Cargando página principal: index.html")
            return HTMLResponse(content=f.read(), status_code=200)
    except Exception as e:
        logger.exception("Error cargando index.html")
        return HTMLResponse(content=f"<h1>Error interno: {e}</h1>", status_code=500)


@router.get("/tablas", response_class=HTMLResponse, tags=["Pages"])
async def get_tablas_html():
    """Sirve la página de tablas.html."""
    try:
        with open("frontend/templates/tablas.html", "r", encoding="utf-8") as f:
            logger.info("Cargando página de tablas: tablas.html")
            return HTMLResponse(content=f.read(), status_code=200)
    except Exception as e:
        logger.exception("Error cargando tablas.html")
        return HTMLResponse(content=f"<h1>Error interno: {e}</h1>", status_code=500)