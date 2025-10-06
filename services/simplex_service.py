from scipy.optimize import linprog

def solve_simplex(c, A, b):
    # Validación: al menos 2 coeficientes en la función objetivo
    if not isinstance(c, list) or len(c) != 2:
        return {
            "success": False,
            "status": -1,
            "message": "La función objetivo debe tener exactamente 2 coeficientes (c)."
        }

    result = linprog(c=c, A_ub=A, b_ub=b, method="highs")

    if result.success:
        # Caso de éxito: devuelve la solución y el valor óptimo
        return {
            "success": True,
            "solution": result.x.tolist(),
            "objective_value": result.fun
        }
    else:
        # Caso de error: interpretar el status
        message = "Problema desconocido"
        if result.status == 2:
            message = "No existe solución factible (restricciones incompatibles)."
        elif result.status == 3:
            message = "Problema no acotado (la función objetivo puede crecer indefinidamente)."

        return {
            "success": False,
            "status": result.status,
            "message": message
        }
