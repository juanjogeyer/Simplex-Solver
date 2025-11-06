from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routers import router 

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_html():
    with open("frontend/templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/tablas", response_class=HTMLResponse)
async def get_tablas_html():
    with open("frontend/templates/tablas.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

app.include_router(router)