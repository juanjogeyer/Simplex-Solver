from pydantic import BaseModel
from typing import List, Literal, Dict, Any, Optional

# --- Modelos de Request ---

class SimplexRequest(BaseModel):
    """
    Define la entrada para cualquier endpoint del solver Simplex.
    """
    problem_type: Literal['minimization', 'maximization']
    C: List[float]
    LI: List[List[float]]
    LD: List[float]
    O: List[Literal['<=', '>=', '=']]
    
    # Esto agrega un ejemplo en la documentación /docs
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "problem_type": "maximization",
                    "C": [3, 2],
                    "LI": [[1, 1], [1, -1]],
                    "LD": [4, 2],
                    "O": ["<=", "<="]
                }
            ]
        }
    }

# --- Modelos de Response ---
# Estos modelos aseguran que la salida de la API sea consistente
# y esté bien documentada.

class Tableau(BaseModel):
    """
    Define la estructura de una única tabla (iteración) del Simplex.
    """
    titulo: str
    headers: List[str]
    filas: List[List[Any]]
    fila_obj: List[Any]

class SimplexSolution(BaseModel):
    """
    Define la estructura de la solución final óptima.
    """
    variables: Dict[str, float]
    valor_optimo: float

class SimplexResponse(BaseModel):
    """
    Define la respuesta completa del endpoint /solve-tabular.
    """
    status: Literal["optimo", "infactible", "no acotado", "max_iterations_reached"]
    tablas: List[Tableau]
    solucion: Optional[SimplexSolution] = None