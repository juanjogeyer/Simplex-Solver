from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List, Literal
from services.simplex_service import resolver_simplex_tabular
import os

router = APIRouter(
    prefix="/simplex",
    tags=["Simplex Solver"]
)

class SimplexRequest(BaseModel):
    problem_type: Literal['minimization', 'maximization']
    C: List[float]
    LI: List[List[float]]
    LD: List[float]
    O: List[Literal['<=', '>=', '=']]


def _cleanup_file(path: str) -> None:
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        # Silenciar errores de limpieza
        pass

@router.post("/solve-tabular")
async def solve_tabular(request: SimplexRequest):
    try:
        result = resolver_simplex_tabular(
            problem_type=request.problem_type,
            C=request.C,
            LI=request.LI,
            LD=request.LD,
            O=request.O
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
