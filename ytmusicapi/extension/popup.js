const startBtn = document.getElementById("startBtn");
const statusEl = document.getElementById("status");

// --- Función para actualizar estado del botón según nonce ---
function checkNonceAndUpdateButton() {
  chrome.runtime.sendMessage({ cmd: "GET_NONCE" }, (resp) => {
    if (resp && resp.ok && resp.nonce) {
      startBtn.disabled = false;
      statusEl.textContent = "Listo para capturar headers";
    } else {
      startBtn.disabled = true;
      statusEl.textContent = "⚠ No se ha emitido solicitud de captura de headers";
    }
  });
}

// --- Revisar al cargar popup ---
checkNonceAndUpdateButton();

startBtn.addEventListener("click", async () => {
  statusEl.textContent = "Solicitando permiso y abriendo YouTube Music...";
  startBtn.disabled = true;

  // Enviar mensaje al background para iniciar captura
  chrome.runtime.sendMessage({ cmd: "START_CAPTURE" }, (resp) => {
    if (!resp) {
      statusEl.textContent = "Error: no hay respuesta del background.";
      startBtn.disabled = false;
      return;
    }
    if (resp.ok) {
      statusEl.textContent = "Capturando... espera la confirmación (se cerrará solo).";
    } else {
      statusEl.textContent = `Error: ${resp.err || "no especificado"}`;
      startBtn.disabled = false;
    }
  });
});

// escuchar mensajes del background sobre resultado
chrome.runtime.onMessage.addListener((msg) => {
  if (msg && msg.type === "CAPTURE_RESULT") {
    if (msg.ok) {
      statusEl.textContent = "✅ Captura enviada correctamente";
      // cerramos el popup en 2s para UX
      setTimeout(() => window.close(), 2000);
    } else {
      statusEl.textContent = `Error envío: ${msg.err || "fallo"}`;
      startBtn.disabled = false;
    }
  }

  // Actualizar botón si nonce cambia
  if (msg && msg.type === "NONCE_UPDATED") {
    checkNonceAndUpdateButton();
  }
});
// Crear referencia al punto de estado
const statusDot = document.getElementById("statusDot");

// Escuchar actualizaciones de estado WS
chrome.runtime.onMessage.addListener((msg) => {
  if (msg && msg.type === "STATUS_UPDATE") {
    // Usa clases en lugar de estilos inline
    statusDot.className = "status-dot " + msg.state;

    switch (msg.state) {
      case "green":
        statusDot.setAttribute("data-tooltip", "Conectado al backend");
        break;
      case "yellow":
        statusDot.setAttribute("data-tooltip", "Backend bloqueó la conexión");
        break;
      case "red":
        statusDot.setAttribute("data-tooltip", "Desconectado o sin respuesta");
        break;
    }
  }
});
