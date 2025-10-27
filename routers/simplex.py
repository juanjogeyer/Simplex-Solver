from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.simplex_service import simplex_service

router = APIRouter(
    prefix="/simplex",
    tags=["Simplex Solver"]
)
class SimplexRequest(BaseModel):
    model: str
    c: List[float]
    A: List[List[float]]
    b: List[float]

@router.post("/solve")
def solve(request: SimplexRequest):
    result = simplex_service.solve_with_components(
        model=request.model,
        c=request.c,
        A=request.A,
        b=request.b
    )
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
        
    return result