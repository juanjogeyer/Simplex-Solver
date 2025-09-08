import pytest
from services.simplex_service import solve_simplex

def test_simplex_solver_maximization():
    """
    Problema:
    Max Z = 3x1 + 5x2
    Sujeto a:
        x1 <= 4
        2x2 <= 12
        3x1 + 2x2 <= 18
        x1, x2 >= 0
    """

    model = "max"
    c = [-3, -5]
    A = [
        [1, 0],   # x1 <= 4
        [0, 2],   # 2x2 <= 12
        [3, 2]    # 3x1 + 2x2 <= 18
    ]
    b = [4, 12, 18]

    result = solve_simplex(c, A, b)

    assert result["success"] is True
    assert pytest.approx(result["solution"][0], rel=1e-3) == 2.0
    assert pytest.approx(result["solution"][1], rel=1e-3) == 6.0
    assert pytest.approx(-result["objective_value"], rel=1e-3) == 36.0
