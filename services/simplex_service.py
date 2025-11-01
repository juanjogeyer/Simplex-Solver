import numpy as np
from scipy.optimize import linprog

def _execute_linprog_solver(c, A, b):
    """Función interna que ejecuta el solver de SciPy."""
    result = linprog(c=c, A_ub=A, b_ub=b, method="highs")

    if result.success:
        variables_dict = {}
        for i, value in enumerate(result.x):
            variables_dict[f"x{i+1}"] = round(value, 4)

        return {
            "status": "success",
            "solution": {
                "variables": variables_dict,
                "objective_value": round(result.fun, 4)
            }
        }
    else:
        message = "El solver no pudo encontrar una solución."
        if result.status == 2:
            message = "Problema no factible (no hay solución que cumpla las restricciones)."
        elif result.status == 3:
            message = "Problema no acotado (la solución tiende a infinito)."
        return {"status": "error", "message": message}

class SimplexService:
    def solve_with_components(self, model: str, c: list, A: list, b: list):
        """
        Resuelve el problema recibiendo los componentes c, A, y b directamente.
        """
        try:
            c_np = np.array(c, dtype=float)
            A_np = np.array(A, dtype=float)
            b_np = np.array(b, dtype=float)

            num_vars = len(c_np)
            if num_vars > 0 and A_np.shape[1] != num_vars:
                raise ValueError(
                    f"Inconsistencia: La función objetivo tiene {num_vars} variables, "
                    f"pero la matriz 'A' tiene {A_np.shape[1]} columnas."
                )

            c_to_solve = c_np.copy()
            if model.lower() == 'max':
                c_to_solve = -c_to_solve
            elif model.lower() == 'min':
                A_np = -A_np
                b_np = -b_np

            result = _execute_linprog_solver(c_to_solve, A_np, b_np)

            if model.lower() == 'max' and result.get("status") == "success":
                result["solution"]["objective_value"] *= -1

            return result

        except ValueError as e:
            return {"status": "error", "message": str(e)}
        except Exception as e:
            return {"status": "error", "message": f"Ocurrió un error interno: {str(e)}"}

simplex_service = SimplexService()