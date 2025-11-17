import numpy as np
from typing import List, Tuple, Optional
from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def generar_grafico_2d(
    C: List[float],
    LI: List[List[float]],
    LD: List[float],
    titulo: str = "Grafico de Restricciones y Funcion Objetivo",
    save_path: Optional[str] = None,
    xlim: Optional[Tuple[float, float]] = None,
    ylim: Optional[Tuple[float, float]] = None,
    show: bool = False,
    mark_point: Optional[Tuple[float, float]] = None,
):
    """
    Genera un gráfico que muestra las restricciones y la función objetivo.
    Solo funciona para problemas con 2 variables.

    Args:
        C: Coeficientes de la función objetivo.
        LI: Coeficientes de las restricciones.
        LD: Lados derechos de las restricciones.
        titulo: Título del gráfico.
        save_path: Ruta para guardar el archivo PNG. Si es None, devuelve bytes.
        xlim: Límites del eje X como tupla (min, max).
        ylim: Límites del eje Y como tupla (min, max).
        show: Si es True, muestra el gráfico (usar solo en entornos interactivos).
        mark_point: Punto (x1, x2) a marcar como óptimo en el gráfico.
        
    Returns:
        str: Ruta del archivo si save_path fue especificado.
        bytes: Contenido PNG en bytes si save_path es None.
        
    Raises:
        ValueError: Si el problema no tiene exactamente 2 variables.
    """
    if len(C) != 2:
        raise ValueError("El gráfico solo puede generarse para problemas con exactamente 2 variables.")

    def _finite_vals(vals: List[float]) -> List[float]:
        """Filtra valores finitos de una lista."""
        return [v for v in vals if v is not None and np.isfinite(v)]

    xs: List[float] = []
    ys: List[float] = []
    
    # Interceptos con ejes por cada restricción a*x1 + b*x2 = r
    for coef, r in zip(LI, LD):
        a, b = coef[0], coef[1]
        if a != 0:
            xs.append(r / a)
            ys.append(0.0)
        if b != 0:
            xs.append(0.0)
            ys.append(r / b)
    
    # Intersecciones entre pares de rectas
    n = len(LI)
    for i in range(n):
        a1, b1 = LI[i]
        r1 = LD[i]
        for j in range(i + 1, n):
            a2, b2 = LI[j]
            r2 = LD[j]
            det = a1 * b2 - a2 * b1
            if abs(det) > 1e-12:
                x_int = (r1 * b2 - r2 * b1) / det
                y_int = (a1 * r2 - a2 * r1) / det
                xs.append(x_int)
                ys.append(y_int)

    xs = _finite_vals(xs)
    ys = _finite_vals(ys)

    # Restringir a valores no negativos por convención (x1>=0, x2>=0)
    xs_pos = [v for v in xs if v >= 0]
    ys_pos = [v for v in ys if v >= 0]

    # Límites con margen
    if xlim is None:
        if xs_pos:
            xmax = max(xs_pos)
            x_min, x_max = 0.0, max(1.0, xmax) * 1.1
        else:
            x_min, x_max = 0.0, 10.0
    else:
        x_min, x_max = xlim

    if ylim is None:
        if ys_pos:
            ymax = max(ys_pos)
            y_min, y_max = 0.0, max(1.0, ymax) * 1.1
        else:
            y_min, y_max = 0.0, 10.0
    else:
        y_min, y_max = ylim

    # Asegurar que el punto óptimo quede dentro de los límites
    if mark_point is not None:
        mx, my = mark_point
        if np.isfinite(mx) and mx >= 0:
            x_max = max(x_max, mx * 1.1 if mx > 0 else 1.0)
        if np.isfinite(my) and my >= 0:
            y_max = max(y_max, my * 1.1 if my > 0 else 1.0)

    x = np.linspace(x_min, x_max, 400)

    plt.figure(figsize=(10, 6))

    # Graficar restricciones
    for i, (coef, ld) in enumerate(zip(LI, LD)):
        if coef[1] != 0:
            y = (ld - coef[0] * x) / coef[1]
            plt.plot(x, y, label=f"Restricción {i+1}")
        else:
            plt.axvline(x=ld / coef[0], label=f"Restricción {i+1}")

    # Graficar función objetivo
    if C[1] != 0:
        y_obj = (-C[0] * x) / C[1]
        plt.plot(x, y_obj, 'r--', label="Función Objetivo")
    else:
        plt.axvline(x=0, color='r', linestyle='--', label="Función Objetivo")

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title(titulo)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    # Marcar punto óptimo si se proporciona
    if mark_point is not None:
        mx, my = mark_point
        if np.isfinite(mx) and np.isfinite(my):
            plt.scatter([mx], [my], c='k', s=60, zorder=5, label='Óptimo')
            # Asegurar que la leyenda muestre el punto (manejar duplicación)
            handles, labels = plt.gca().get_legend_handles_labels()
            seen = set()
            new = []
            for h, l in zip(handles, labels):
                if l not in seen:
                    new.append((h, l))
                    seen.add(l)
            if new:
                plt.legend(*zip(*new))

    # Guardar si se especifica ruta; si no, devolver bytes PNG
    result = None
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        result = save_path
    else:
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        result = buf.getvalue()
        buf.close()

    # Mostrar solo si se solicita (por defecto False en entorno servidor)
    if show:
        plt.show()

    plt.close()
    return result
