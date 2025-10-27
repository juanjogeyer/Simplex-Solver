import pytest
from services.simplex_service import SimplexService

def test_simplex_solver_maximization():
    """
    Max Z = 7x1 + 8x2 + 5x3 + 4x4 + 6x5 + 2x6
    Sujeto a:
        0.5x1 + 0.45x2 + 0.6x3 <= 2400
        x1 + x2 + x3 <= 5500
        x1 + x4 <= 2000
        x2 + x5 <= 4000
        x3 + x6 <= 5000
        x1, x2, x3, x4, x5, x6 >= 0
    """

    # Definición del problema
    model = "max"  # Maximización
    c = [7, 8, 5, 4, 6, 2]  # Coeficientes de la función objetivo
    A = [
        [0.5, 0.45, 0.6, 0, 0, 0],  # 0.5x1 + 0.45x2 + 0.6x3 <= 2400
        [1, 1, 1, 0, 0, 0],         # x1 + x2 + x3 <= 5500
        [1, 0, 0, 1, 0, 0],         # x1 + x4 <= 2000
        [0, 1, 0, 0, 1, 0],         # x2 + x5 <= 4000
        [0, 0, 1, 0, 0, 1]          # x3 + x6 <= 5000
    ]
    b = [2400, 5500, 2000, 4000, 5000]  # Restricciones del lado derecho

    simplex = SimplexService()

    result = simplex.solve_with_components(model, c, A, b)

    # Verificaciones
    assert result["status"] == "success"  # El problema debe resolverse con éxito
    assert isinstance(result["solution"]["variables"], dict)  # La solución debe ser un diccionario
    assert result["solution"]["objective_value"] is not None  # Debe devolver un valor objetivo