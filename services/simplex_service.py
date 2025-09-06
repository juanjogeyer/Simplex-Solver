from scipy.optimize import linprog

def solve_simplex(c, A, b):
    """
    Resuelve un problema de programación lineal con SciPy.
    Minimiza:     c^T x
    Sujeto a:     A @ x <= b
                  x >= 0
    Parámetros:
        c: lista de coeficientes de la función objetivo
        A: matriz (lista de listas) de restricciones
        b: lista con los términos independientes de las restricciones
    Retorna:
        dict con la solución, valor óptimo y estado
    """
    result = linprog(c=c, A_ub=A, b_ub=b, method="highs")

    return {
        "success": result.success,
        "status": result.message,
        "objective_value": result.fun,
        "solution": result.x.tolist() if result.success else None
    }
