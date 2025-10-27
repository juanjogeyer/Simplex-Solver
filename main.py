from fastapi import FastAPI
from routers.simplex import router as simplex_router

app = FastAPI(
    title="Simplex Solver API",
    description="Una API para resolver problemas de Programación Lineal.",
    version="1.0.0"
)

app.include_router(simplex_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Simplex Solver"}
