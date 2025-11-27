// background.js
// One-shot capture: activa escucha, abre YT Music, captura primera request con cookie, envía a backend y desactiva.

console.log("[BG] background loaded (one-shot)");

const API_URL = "http://127.0.0.1:8002"; // <-- modificar si cambia backend
const WS_URL = "ws://127.0.0.1:8002/auth/ytm/ws";    // <-- WebSocket del backend (para nonce)
let captureActive = false;
let listenerRegistered = false;
let currentNonce = null;

let connectionStatus = "red";
chrome.storage.local.set({ connectionStatus });


// ============================================================================
// WEBSOCKET: Conexión persistente para recibir nonces en tiempo real
// ============================================================================
// ============================================================================
// WEBSOCKET: Conexión persistente para recibir nonce + handshake de token
// ============================================================================
(function connectWebSocket() {
  let ws;
  let activeToken = null;
  let pingInterval = null;

  const openConnection = () => {
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      Semstate="GREEN"
      chrome.runtime.sendMessage({ type: "STATUS_UPDATE", state: "green" });
      console.log("[BG][WS] Conectado al backend, esperando token inicial...");
      connectionStatus = "green";
      chrome.storage.local.set({ connectionStatus: "green" });
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        // Caso 1: backend manda error
        if (data.error) {
          Semstate="YELLOW"
          chrome.runtime.sendMessage({ type: "STATUS_UPDATE", state: "yellow" });
          console.warn("[BG][WS] Error del backend:", data.error);
          return;
        }

        // Caso 2: backend entrega nuevo token (siempre debe actualizarse)
        if (data.token) {
          activeToken = data.token;
        }

        // Caso 3: si trae nonce nuevo, lo guardamos y notificamos
        if (data.nonce) {
          currentNonce = data.nonce;
          console.log("[BG][WS] Nuevo nonce recibido:", currentNonce);
          chrome.runtime.sendMessage({ type: "NONCE_UPDATED", nonce: currentNonce });
        }

      } catch (err) {
        console.error("[BG][WS] Error procesando mensaje:", err);
      }
    };

    // Pings periódicos usando el token actual
    pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN && activeToken) {
        ws.send(JSON.stringify({ token: activeToken }));
      }
    }, 8000);

    ws.onclose = (ev) => {
      Semstate="RED"
      chrome.runtime.sendMessage({ type: "STATUS_UPDATE", state: "red" });
      connectionStatus = "red";
      chrome.storage.local.set({ connectionStatus: "red" });
      console.warn("[BG][WS] Conexión cerrada (code:", ev.code, ")");
      if (pingInterval) clearInterval(pingInterval);
      activeToken = null;
      setTimeout(openConnection, 3000); // reintento automático
    };

    ws.onerror = (err) => {
      console.error("[BG][WS] Error en WebSocket:", err);
      
      chrome.runtime.sendMessage({ type: "STATUS_UPDATE", state: "red" });
      try { ws.close(); } catch(e){}
      connectionStatus = "red";
      chrome.storage.local.set({ connectionStatus: "red" });
    };
  };

  openConnection();
})();


// ============================================================================
// CAPTURA DE HEADERS
// ============================================================================
function onBeforeSendHeaders(details) {
  try {
    const headers = details.requestHeaders || [];
    const cookieHeader = headers.find(h => h.name.toLowerCase() === "cookie");
    const uaHeader = headers.find(h => h.name.toLowerCase() === "user-agent");
    const originHeader = headers.find(h => h.name.toLowerCase() === "origin");
    const refererHeader = headers.find(h => h.name.toLowerCase() === "referer");

    if (!cookieHeader || !cookieHeader.value || cookieHeader.value.trim() === "") {
      console.log("[BG] capture attempt: no cookie header (skipping)");
      return;
    }

    // --- PAYLOAD CON NONCE ---
    const payload = {
      cookie: cookieHeader.value,
      user_agent: uaHeader ? uaHeader.value : null,
      origin: originHeader ? originHeader.value : null,
      referer: refererHeader ? refererHeader.value : null,
      nonce: currentNonce
    };

    fetch(`${API_URL}/auth/ytm/headers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(async (resp) => {
      let body = null;
      try { body = await resp.json(); } catch(e){}
      if (resp.ok) {
        console.log("[BG] sent OK:", body);
        chrome.runtime.sendMessage({ type: "CAPTURE_RESULT", ok: true });
      } else {
        console.warn("[BG] backend error", resp.status, body);
        chrome.runtime.sendMessage({ type: "CAPTURE_RESULT", ok: false, err: `status ${resp.status}` });
      }
    }).catch(err => {
      console.error("[BG] fetch error:", err);
      chrome.runtime.sendMessage({ type: "CAPTURE_RESULT", ok: false, err: err.toString() });
    }).finally(() => {
      deactivateCapture();
      currentNonce = null;
    });

  } catch (e) {
    console.error("[BG] onBeforeSendHeaders exception:", e);
    deactivateCapture();
    currentNonce = null;
  }
}

// ============================================================================
// FUNCIONES DE CAPTURA
// ============================================================================
function activateCapture() {
  if (listenerRegistered) return { ok: false, err: "listener-already" };

  chrome.webRequest.onBeforeSendHeaders.addListener(
    onBeforeSendHeaders,
    { urls: ["*://*.music.youtube.com/*", "*://*.youtube.com/*"] },
    ["requestHeaders", "extraHeaders"]
  );
  listenerRegistered = true;
  captureActive = true;
  console.log("[BG] webRequest listener registered (active)");
  return { ok: true };
}

function deactivateCapture() {
  if (listenerRegistered) {
    try { chrome.webRequest.onBeforeSendHeaders.removeListener(onBeforeSendHeaders); }
    catch(e){}
  }
  listenerRegistered = false;
  captureActive = false;
  console.log("[BG] capture deactivated and cleaned up");
}

// ============================================================================
// LISTENER DE MENSAJES (POPUP / EXTENSIÓN INTERNA)
// ============================================================================
// ============================================================================
// LISTENER ÚNICO DE MENSAJES (POPUP / EXTENSIÓN INTERNA)
// ============================================================================
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (!msg) {
        sendResponse({ ok: false, err: "no-msg" });
        return;
    }

    // -------------------------
    // POPUP: Estado del semáforo
    // -------------------------
    if (msg.type === "POPUP_READY") {
        sendResponse({ status: connectionStatus });
        return true;
    }

    if (msg.type === "GET_STATUS") {
        sendResponse({ status: connectionStatus });
        return true;
    }

    if (msg.type === "SET_STATUS") {
        connectionStatus = msg.value;
        chrome.storage.local.set({ connectionStatus });
        sendResponse({ ok: true });
        return true;
    }

    // -------------------------
    // POPUP: Captura
    // -------------------------
    if (msg.cmd === "START_CAPTURE") {
        const act = activateCapture();
        if (!act.ok) {
            sendResponse({ ok: false, err: act.err });
            return;
        }

        chrome.tabs.create({ url: "https://music.youtube.com" }, (tab) => {
            console.log("[BG] opened tab for YT Music:", tab && tab.id);
            sendResponse({ ok: true });
        });
        return true;
    }

    if (msg.cmd === "GET_NONCE") {
        sendResponse({ ok: true, nonce: currentNonce });
        return;
    }

    // -------------------------
    // DEFAULT
    // -------------------------
    sendResponse({ ok: false, err: "invalid-cmd" });
});
