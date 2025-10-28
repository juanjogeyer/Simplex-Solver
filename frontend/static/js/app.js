let tipoModelo = "max"; // Define la variable globalmente

document.addEventListener("DOMContentLoaded", () => {
    const contenedor = document.getElementById("restricciones");
    const btnAgregar = document.getElementById("btnAgregar");
    const btnResolver = document.getElementById("btnResolver");

    // ---------------------------
    // Alternar entre Max y Min
    // ---------------------------
    const btnMax = document.getElementById("btnMax");
    const btnMin = document.getElementById("btnMin");

    btnMax.addEventListener("click", () => {
        tipoModelo = "max";
        btnMax.classList.add("active");
        btnMin.classList.remove("active");
        renderFuncionObjetivo();
    });

    btnMin.addEventListener("click", () => {
        tipoModelo = "min";
        btnMin.classList.add("active");
        btnMax.classList.remove("active");
        renderFuncionObjetivo();
    });

    // ---------------------------
    // Agregar nueva restricción
    // ---------------------------
    btnAgregar.addEventListener("click", () => agregarRestriccion());

    // ---------------------------
    // Eliminar restricción individual
    // ---------------------------
    contenedor.addEventListener("click", (e) => {
        if (e.target.classList.contains("btnEliminar")) {
            e.target.parentElement.remove();
        }
    });

    // ---------------------------
    // Cambiar cantidad de variables dinámicamente
    // ---------------------------
    document.getElementById("numVariables").addEventListener("change", () => {
        renderFuncionObjetivo();
        actualizarRestricciones(); // ✅ Ahora actualiza también las restricciones
    });

    // ---------------------------
    // Conectar el botón Resolver con la función
    // ---------------------------
    btnResolver.addEventListener("click", solveProblem);

    // Inicializar función objetivo y restricción base
    renderFuncionObjetivo();
    actualizarRestricciones();
});

// ---------------------------
// Renderizar función objetivo
// ---------------------------
function renderFuncionObjetivo() {
    const contenedor = document.getElementById("funcionObjetivo");
    const numVariables = parseInt(document.getElementById("numVariables").value);
    contenedor.innerHTML = "";

    const label = document.createElement("label");
    label.innerHTML = (tipoModelo === "max" ? "Max" : "Min") + " Z = ";
    contenedor.appendChild(label);

    for (let i = 1; i <= numVariables; i++) {
        const input = document.createElement("input");
        input.type = "number";
        input.value = "1";
        input.id = `coef${i}`;
        contenedor.appendChild(input);

        const sub = document.createElement("span");
        sub.innerHTML = ` x${i}`;
        contenedor.appendChild(sub);

        if (i < numVariables) contenedor.appendChild(document.createTextNode(" + "));
    }
}

// ---------------------------
// Agregar restricción nueva
// ---------------------------
function agregarRestriccion() {
    const contenedor = document.getElementById("restricciones");
    const btnAgregar = document.getElementById("btnAgregar");
    const numVars = parseInt(document.getElementById("numVariables").value);
    const restriccionDiv = document.createElement("div");
    restriccionDiv.classList.add("restriccion");

    let contenido = "";
    for (let i = 1; i <= numVars; i++) {
        contenido += ` <input type="number" value="1" class="a${i}">x${i} ${i < numVars ? '+' : ''}`;
    }

    contenido += `
        <select class="operador">
            <option value="<=" selected>≤</option>
            <option value="=">=</option>
            <option value=">=">≥</option>
        </select>
        <input type="number" value="10" class="b">
        <button class="btn secondary btnEliminar">✖</button>
    `;

    restriccionDiv.innerHTML = contenido;
    contenedor.insertBefore(restriccionDiv, btnAgregar);
}

// ---------------------------
// Actualizar todas las restricciones al cambiar n° variables
// ---------------------------
function actualizarRestricciones() {
    const contenedor = document.getElementById("restricciones");
    const restricciones = contenedor.querySelectorAll(".restriccion");

    restricciones.forEach(r => r.remove()); // eliminar todas
    agregarRestriccion(); // deja al menos una base
}

// ---------------------------
// Obtener coeficientes de la función objetivo
// ---------------------------
function getFunctionObjective() {
    const numVariables = parseInt(document.getElementById("numVariables").value);
    const c = [];
    for (let i = 1; i <= numVariables; i++) {
        const coef = parseFloat(document.getElementById(`coef${i}`).value);
        c.push(coef);
    }
    return c;
}

// ---------------------------
// Obtener restricciones dinámicamente
// ---------------------------
function getRestrictions() {
    const restricciones = [];
    const restriccionElements = document.querySelectorAll(".restriccion");

    restriccionElements.forEach(restriccion => {
        const coefs = [];
        let i = 1;
        while (restriccion.querySelector(`.a${i}`)) {
            coefs.push(parseFloat(restriccion.querySelector(`.a${i}`).value));
            i++;
        }
        const operador = restriccion.querySelector(".operador").value;
        const valor = parseFloat(restriccion.querySelector(".b").value);
        restricciones.push([...coefs, operador, valor]);
    });

    return restricciones;
}

// ---------------------------
// Preparar y enviar solicitud al backend
// ---------------------------
function prepareRequestData() {
    const c = getFunctionObjective();
    const restricciones = getRestrictions();

    const A = restricciones.map(r => r.slice(0, -2));
    const b = restricciones.map(r => r.at(-1));

    return {
        model: tipoModelo,
        c,
        A,
        b
    };
}

// ---------------------------
// Resolver el problema con backend
// ---------------------------
async function solveProblem() {
    const requestData = prepareRequestData();

    try {
        const response = await fetch("/simplex/solve", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData)
        });
        console.log("Respuesta del servidor:", requestData);

        const result = await response.json();
        if (response.ok) displayResult(result);
        else alert("Error: " + result.message);
    } catch (error) {
        console.error("Error al resolver:", error);
        alert("Hubo un error al resolver el problema.");
    }
}

// ---------------------------
// Mostrar resultado
// ---------------------------
function displayResult(result) {
    const resultDiv = document.getElementById("resultado");
    resultDiv.innerHTML = `
        <h3>Resultado</h3>
        <p>Valor de la función objetivo: ${result.solution.objective_value}</p>
        <p>Solución:</p>
        <ul>
            ${Object.entries(result.solution.variables).map(([v, val]) => `<li>${v}: ${val}</li>`).join("")}
        </ul>
    `;
}
