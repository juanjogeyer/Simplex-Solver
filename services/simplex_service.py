from scipy.optimize import linprog

def solve_simplex(c, A, b):
    result = linprog(c=c, A_ub=A, b_ub=b, method="highs")

    return {
        "success": result.success,
        "status": result.message,
        "objective_value": result.fun,
        "solution": result.x.tolist() if result.success else None
    }
