// --- MODAL ---
const modal = document.getElementById("modal");
const abrir = document.getElementById("abrirModal");
const cerrar = document.querySelector(".cerrar");

abrir.onclick = () => (modal.style.display = "block");
cerrar.onclick = () => (modal.style.display = "none");
window.onclick = (event) => {
  if (event.target == modal) modal.style.display = "none";
};

// --- POPUP ---
function mostrarPopup(mensaje, tipo = "success") {
  const popup = document.getElementById("popupMensaje");
  popup.textContent = mensaje;
  popup.className = `popup ${tipo} show`;

  setTimeout(() => {
    popup.className = "popup"; // desaparece automáticamente
  }, 3000); // 3 segundos
}

// --- GENERAR TOKEN ---
const botonToken = document.getElementById("generarToken");
const tokenOutput = document.getElementById("tokenOutput");
const instruccion = document.getElementById("instruccionToken");

// Generar token
botonToken.addEventListener("click", async () => {
  try {
    const response = await fetch("/auth/generar-shortcode", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ clase_id: 1 }),
    });

    const data = await response.json();
    tokenOutput.textContent = data.shortcode || "";

    if (data.shortcode) {
      instruccion.textContent =
        "Copia este código y compártelo con tus alumnos";
    } else {
      instruccion.textContent = "";
    }
  } catch (err) {
    console.error("Error generando token:", err);
    tokenOutput.textContent = "Error al generar el codigo";
    instruccion.textContent = "";
  }
});

// Copiar al hacer click sobre el token
tokenOutput.addEventListener("click", () => {
  const token = tokenOutput.textContent.trim();
  if (!token || token === "Codigo se asistencia no generado") return;

  navigator.clipboard.writeText(token).then(() => {
    const originalBackground = tokenOutput.style.backgroundColor;
    tokenOutput.style.backgroundColor = "#469e66ff";
    setTimeout(
      () => (tokenOutput.style.backgroundColor = originalBackground),
      1000
    );
  });
});

// --- SOCKET.IO ---
const socket = io();

socket.on("connect", () => console.log("✅ Conectado al servidor WebSocket"));

// Escuchar nuevas asistencias en tiempo real
socket.on("asistencia_actualizada", (data) => {
  console.log("📡 Nueva asistencia recibida:", data);

  const row = document.querySelector(`tr[data-id='${data.alumno_id}']`);
  if (row) {
    const estadoCell = row.querySelector(".estado");
    estadoCell.textContent = "✔ Presente";
    estadoCell.className = "estado asistido";
  }
});

// --- AGREGAR ALUMNO SIN RECARGAR ---
const formAgregar = document.getElementById("formAgregarAlumno");

formAgregar.addEventListener("submit", async (e) => {
  e.preventDefault(); // Evita recarga de página
  console.log("Submit capturado correctamente");
  const formData = new FormData(formAgregar);
  const data = Object.fromEntries(formData.entries());

  try {
    const response = await fetch(formAgregar.action, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.ok) {
      mostrarPopup(result.message, "success");

      // Opcional: actualizar la tabla dinámicamente
      const tbody = document.querySelector("#tablaAlumnos tbody");
      const nuevaFila = document.createElement("tr");
      nuevaFila.setAttribute("data-id", result.alumno.id);
      nuevaFila.innerHTML = `
        <td>${result.alumno.nombre}</td>
        <td>${result.alumno.dni}</td>
        <td><span class="estado inasistido">✖ Ausente</span></td>
      `;
      tbody.appendChild(nuevaFila);

      formAgregar.reset(); // Limpiar formulario
      modal.style.display = "none"; // Cerrar modal
    } else {
      mostrarPopup(result.message, "error");
    }
  } catch (err) {
    console.error("Fetch falló:", err);
    mostrarPopup("Error de conexión o servidor", "error"); // toast rojo
  }
});
