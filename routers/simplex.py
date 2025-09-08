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
    c = request.c.copy()

    if request.model.lower() == "max":
        c = [-x for x in c]

    result = solve_simplex(c, request.A, request.b)

    if request.model.lower() == "max" and result["success"]:
        result["objective_value"] = -result["objective_value"]

    result["model"] = request.model

    return result