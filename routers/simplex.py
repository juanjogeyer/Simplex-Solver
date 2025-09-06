from fastapi import APIRouter
from pydantic import BaseModel
from services.simplex_service import solve_simplex

simplex = APIRouter(
    prefix="/simplex",
)


@simplex.get("/")
def simplex_solver():
    return "Aquí debería devolver el resultado del simplex"

class SimplexRequest(BaseModel):
    model: str
    c: list[float]
    A: list[list[float]]
    b: list[float]

@simplex.post("/solve")
def solve(request: SimplexRequest):
    # Copiar coeficientes de la función objetivo
    c = request.c.copy()

    # Si el modelo es de maximización, se transforma en un problema de minimización
    if request.model.lower() == "max":
        c = [-x for x in c]

    # Resolver con tu servicio simplex
    result = solve_simplex(c, request.A, request.b)

    # Ajustar el valor de la función objetivo en caso de maximización
    if request.model.lower() == "max" and result["success"]:
        result["objective_value"] = -result["objective_value"]

    # Agregar el modelo al resultado
    result["model"] = request.model

    return result