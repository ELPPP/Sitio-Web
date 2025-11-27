const startBtn = document.getElementById("startBtn");
const statusEl = document.getElementById("status");
const statusDot = document.getElementById("statusDot");

// ---------------------------------------------------------------------------
//  ESTADO INICIAL DEL SEMÁFORO
// ---------------------------------------------------------------------------
chrome.runtime.sendMessage({ cmd: "GET_STATUS" }, (resp) => {
  if (resp && resp.status) {
    statusDot.className = "status-dot " + resp.status;

    switch (resp.status) {
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

// ---------------------------------------------------------------------------
//  BOTÓN LISTO/NO LISTO SEGÚN NONCE
// ---------------------------------------------------------------------------
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

checkNonceAndUpdateButton();

// ---------------------------------------------------------------------------
//  BOTÓN PARA INICIAR LA CAPTURA
// ---------------------------------------------------------------------------
startBtn.addEventListener("click", async () => {
  statusEl.textContent = "Solicitando permiso y abriendo YouTube Music...";
  startBtn.disabled = true;

  chrome.runtime.sendMessage({ cmd: "START_CAPTURE" }, (resp) => {
    if (!resp) {
      statusEl.textContent = "Error: no hay respuesta del background.";
      startBtn.disabled = false;
      return;
    }

    if (resp.ok) {
      statusEl.textContent = "Capturando... espera la confirmación.";
    } else {
      statusEl.textContent = `Error: ${resp.err || "no especificado"}`;
      startBtn.disabled = false;
    }
  });
});

// ---------------------------------------------------------------------------
//  LISTENER ÚNICO PARA TODOS LOS MENSAJES DEL BACKGROUND
// ---------------------------------------------------------------------------
chrome.runtime.onMessage.addListener((msg) => {

  // --- Resultado de captura
  if (msg && msg.type === "CAPTURE_RESULT") {
    if (msg.ok) {
      statusEl.textContent = "✅ Captura enviada correctamente";
      setTimeout(() => window.close(), 2000);
    } else {
      statusEl.textContent = `Error envío: ${msg.err || "fallo"}`;
      startBtn.disabled = false;
    }
  }

  // --- Nonce nuevo: actualizar botón
  if (msg && msg.type === "NONCE_UPDATED") {
    checkNonceAndUpdateButton();
  }

  // --- Actualización del semáforo vía WebSocket
  if (msg && msg.type === "STATUS_UPDATE") {
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
