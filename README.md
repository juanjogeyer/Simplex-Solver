# Simplex Solver API

Simplex Solver es una aplicación web completa diseñada para resolver problemas de **Programación Lineal (PL)** mediante el **Método Simplex Tabular**. Incluye una API backend robusta construida con **FastAPI**, un frontend interactivo en **HTML/CSS/JS**, visualización gráfica, exportación a PDF y soporte completo para problemas de maximización, minimización y restricciones avanzadas.

---

## Descripción General

El núcleo del sistema es un solver que implementa:

- **Método Simplex Tabular**
- **Método de Dos Fases** (cuando existen restricciones ≥ o =)
- **Visualización paso a paso del proceso**
- **Generación de gráficos 2D**
- **Exportación de reportes en PDF**

La aplicación cuenta con un frontend intuitivo para formular problemas y visualizar los resultados de manera clara.

---

## Características Principales

- **Solver Simplex Tabular**  
  Implementación completa del método tabular clásico.

- **Método de Dos Fases**  
  Activación automática cuando correspondan restricciones de tipo ≥ o =.

- **Tipos de Problema**  
  ✔ Maximización  
  ✔ Minimización

- **Manejo de Restricciones**  
  - Holgura (≤)  
  - Exceso (≥)  
  - Igualdad (=)

- **Análisis de Solución**  
  Detección automática de:
  - Óptimo
  - Problema infactible
  - Problema no acotado

- **Interfaz Web Interactiva**  
  Añadir/eliminar restricciones dinámicamente.

- **Visualización Paso a Paso**  
  Todas las iteraciones del algoritmo Simplex en formato tabular.

- **Gráficos 2D (para 2 variables)**  
  Representación geométrica de restricciones y función objetivo.

- **Exportación a PDF**  
  Informe profesional con solución, tablas y gráficos.

- **Contenerización con Docker**

- **CI/CD con GitHub Actions**  
  Testing automatizado + publicación de imagen en Docker Hub.

---

## Tecnologías Utilizadas

### Backend
- **FastAPI**
- **Uvicorn**
- **NumPy**

### Reportes y Gráficos
- **Matplotlib**
- **ReportLab**

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript (Vanilla)**

### Entorno y Despliegue
- **Python 3.12+**
- **uv** (gestor de paquetes ultrarrápido)
- **Pytest**
- **Docker**
- **GitHub Actions**

---

## Instalación y Ejecución

### Requisitos Previos

- Python **3.12+**
- `uv` (instalable vía: `pip install uv`)

---

### ▶ Ejecución Local (Modo Desarrollo)

Clonar el repositorio:

```bash
git clone https://github.com/juanjogeyer/Simplex-Solver.git
cd Simplex-Solver
```

Instalar dependencias
```bash
uv sync
```

Levantar el servidor con autoreload:
```bash
uv run fastapi dev
```

Abrir en el navegador:

- **Aplicación Web**: http://127.0.0.1:8000
- **API Docs (Swagger)**: http://127.0.0.1:8000/docs

## Uso de la Aplicación Web

1. **Definir Problema**  
   Seleccionar número de variables y tipo (Max/Min).

2. **Ingresar Función Objetivo**  
   Completar coeficientes para cada variable.

3. **Agregar Restricciones**
   - Coeficientes de cada variable  
   - Operador (≤, =, ≥)  
   - Lado Derecho (LD)

4. **Resolver**  
   La aplicación mostrará:
   - Estado de solución  
   - Valores óptimos  
   - Variables básicas y no básicas  

5. **Acciones Adicionales**
   - **Ver Tablas** (todas las iteraciones)  
   - **Ver Gráfico** (solo para 2 variables)  
   - **Exportar PDF** con toda la solución  


---

## Estructura del Proyecto

```bash
.
├── .github/workflows/      # Flujos de CI/CD para tests y Docker
├── frontend/
│   ├── static/             # Archivos CSS y JS
│   └── templates/          # Archivos HTML (index.html, tablas.html)
├── routers/
│   ├── pages_router.py     # Endpoints que sirven el HTML
│   └── simplex_router.py   # Endpoints de la API (/solve, /graph, /pdf)
├── services/
│   ├── PDF_service/        # Lógica para construir el PDF con ReportLab
│   ├── graph_service.py    # Lógica para generar gráficos con Matplotlib
│   └── simplex_service.py  # Implementación del Método Simplex Tabular
├── test/                   # Tests unitarios y de integración (Pytest)
├── .dockerignore           # Archivos a ignorar por Docker
├── .gitignore              # Archivos a ignorar por Git
├── Dockerfile              # Define la imagen Docker de producción
├── main.py                 # Punto de entrada de la aplicación FastAPI
├── pyproject.toml          # Definición del proyecto y dependencias
├── schemas.py              # Modelos Pydantic (request/response de la API)
└── uv.lock                 # Lockfile de dependencias de uv
```


---

## 📡 API para Desarrolladores

### **POST /simplex/solve-tabular**
Resuelve un problema de Programación Lineal usando el método Simplex tabular.

#### Request Body (SimplexRequest)

```json
{
  "problem_type": "maximization",
  "C": [3, 5],
  "LI": [
    [1, 0],
    [0, 2],
    [3, 2]
  ],
  "LD": [4, 12, 18],
  "O": ["<=", "<=", "<="]
}
```

#### Response Body (SimplexRequest)
```json
{
  "status": "optimo",
  "tablas": [
    {
      "titulo": "Fase 0 - Iteración 1 (Tabla Inicial)",
      "headers": ["Base", "x1", "x2", "s1", "s2", "s3", "LD (RHS)"],
      "filas": [
        ["s1", 1.0, 0.0, 1.0, 0.0, 0.0, 4.0],
        ["s2", 0.0, 2.0, 0.0, 1.0, 0.0, 12.0],
        ["s3", 3.0, 2.0, 0.0, 0.0, 1.0, 18.0]
      ],
      "fila_obj": ["Z", -3.0, -5.0, 0.0, 0.0, 0.0, 0.0]
    }
  ],
  "solucion": {
    "variables": {
      "x1": 4.0,
      "x2": 6.0,
      "s1": 0.0,
      "s2": 0.0,
      "s3": 2.0
    },
    "valor_optimo": 30.0
  }
}
```

## Otros Endpoints

### **POST /simplex/generate-graph-html**
- Solo para problemas con **2 variables**.  
- Devuelve un documento HTML con el gráfico (imagen PNG embebida en base64).

### **POST /simplex/generate-pdf**
- Resuelve el problema y genera un **reporte PDF completo**, incluyendo tablas y gráficos.  
- Devuelve un `FileResponse` con el PDF.


---

## Testing

Ejecutar los tests con:

```bash
pytest
```

### Funcionalidades de los tests

Los tests verifican exhaustivamente el correcto funcionamiento del algoritmo en los siguientes casos:

- **Casos óptimos**: problemas con solución finita y alcanzable
- **Problemas infactibles**: detección correcta de inconsistencias en las restricciones
- **Problemas no acotados**: identificación de soluciones ilimitadas
- **Casos de minimización**: soporte completo para problemas de minimización
- **Ejecución del Método de Dos Fases**: implementación y verificación del método completo

## Docker y Despliegue

### Construir la imagen localmente

```bash
docker build -t simplex-solver .
```

### Ejecutar el contenedor

```bash
docker run -d -p 5000:5000 --name simplex-app simplex-solver
```

## Autores

- [@juanjo_geyer](https://github.com/juanjogeyer)
- [@juan_lopez](https://github.com/juan1lopez)
- [@manuel_olivares](https://github.com/manuolivares05)
- [@tomas_alfaro](https://github.com/tomasalfaro)
- [@joaquin_lepez](https://github.com/JoaquinLepez)