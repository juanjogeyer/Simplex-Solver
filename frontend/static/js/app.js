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
        actualizarRestricciones();
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

    restricciones.forEach(r => r.remove());
    agregarRestriccion();
}

// ---------------------------
// Obtener coeficientes de la función objetivo
// ---------------------------
function getFunctionObjective() {
    const numVariables = parseInt(document.getElementById("numVariables").value);
    const c = [];
    for (let i = 1; i <= numVariables; i++) {
        const valor = document.getElementById(`coef${i}`).value;
        const numero = parseFloat(valor);
        if (isNaN(numero) || valor.trim() === "") {
            throw new Error(`Coeficiente x${i} de la función objetivo inválido o vacío`);
        }
        c.push(numero);
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
            const valor = restriccion.querySelector(`.a${i}`).value;
            const numero = parseFloat(valor);
            if (isNaN(numero) || valor.trim() === "") {
                throw new Error(`Valor inválido en coeficiente x${i}`);
            }
            coefs.push(numero);
            i++;
        }
        const operador = restriccion.querySelector(".operador").value;
        const valorB = restriccion.querySelector(".b").value;
        const numeroB = parseFloat(valorB);
        
        if (isNaN(numeroB) || valorB.trim() === "") {
            throw new Error("Valor inválido en el lado derecho de la restricción");
        }
        
        restricciones.push([...coefs, operador, numeroB]);
    });

    return restricciones;
}

// ---------------------------
// Preparar y enviar solicitud al backend
// ---------------------------
function prepareRequestData() {
    try {
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
    } catch (error) {
        throw error; // Re-lanzar para que lo capture solveProblem
    }
}

// ---------------------------
// Resolver el problema con backend
// ---------------------------
async function solveProblem() {
    const resultDiv = document.getElementById("resultado");
    
    resultDiv.innerHTML = "⏳ Calculando...";
    resultDiv.style.color = "blue";

    try {
        const data = prepareRequestData();

        const response = await fetch("/resolver_simplex", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        console.log("Respuesta del servidor:", result); // Para debugging

        // Mostrar resultados según status
        if (result.status === 1) {
            resultDiv.innerHTML = `
                <h3>✅ Solución encontrada</h3>
                <p><strong>Valor óptimo:</strong> ${result.solution.objective_value}</p>
                <p><strong>Variables:</strong></p>
                <ul>
                    ${Object.entries(result.solution.variables)
                        .map(([v, val]) => `<li>${v}: ${val.toFixed(4)}</li>`)
                        .join("")}
                </ul>
            `;
            resultDiv.style.color = "green";
        } else if (result.status === 2) {
            resultDiv.innerHTML = "<h3>❌ Problema no factible</h3><p>No existe una solución que cumpla todas las restricciones.</p>";
            resultDiv.style.color = "red";
        } else if (result.status === 3) {
            resultDiv.innerHTML = "<h3>⚠️ Problema ilimitado</h3><p>La función objetivo no tiene límite (puede crecer infinitamente).</p>";
            resultDiv.style.color = "orange";
        } else {
            resultDiv.innerHTML = `<h3>❌ Error desconocido</h3><p>${result.message || "Verifica los datos ingresados."}</p>`;
            resultDiv.style.color = "red";
        }

    } catch (error) {
        console.error("Error:", error);
        
        // Diferenciar entre errores de validación y errores de conexión
        if (error.message.includes("inválido") || error.message.includes("vacío")) {
            resultDiv.innerHTML = `<h3>⚠️ Error en los datos</h3><p>${error.message}</p><p>Por favor, verifica que todos los campos contengan números válidos.</p>`;
            resultDiv.style.color = "orange";
        } else {
            resultDiv.innerHTML = `<h3>❌ Error de conexión</h3><p>${error.message}</p>`;
            resultDiv.style.color = "red";
        }
    }
}

// Validación de entrada en tiempo real
document.addEventListener("input", e => {
    if (e.target.tagName === "INPUT" && e.target.type === "number") {
        // Permitir solo números, punto decimal y signo negativo
        e.target.value = e.target.value.replace(/[^\d\.\-]/g, "");
        
        // Resaltar en rojo si está vacío o inválido
        if (e.target.value.trim() === "" || isNaN(parseFloat(e.target.value))) {
            e.target.style.border = "2px solid red";
        } else {
            e.target.style.border = "";
        }
    }
});