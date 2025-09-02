from fastapi import APIRouter

simplex = APIRouter(
    prefix="/simplex",
)


@simplex.get("/")
def simplex_solver():
    return "Aquí debería devolver el resultado del simplex"

