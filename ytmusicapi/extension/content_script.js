// content_script.js
console.log("[CS] content script loaded on", location.href);

// auto-trigger when on music.youtube.com (document_start + also run check)
(function tryAutoTrigger() {
  try {
    if (location.hostname.includes("music.youtube.com")) {
      console.log("[CS] on music.youtube.com — sending EXPORT_TO_EXTENSION event to background");
      // Generate a simple nonce for debug (in prod, fetch nonce from local API)
      const debugNonce = "debug-" + Date.now();
      // send as window message so original code path still valid
      window.postMessage({ type: "EXPORT_TO_EXTENSION", nonce: debugNonce }, "*");
    } else {
      console.log("[CS] not music.youtube.com, skipping auto trigger");
    }
  } catch (e) {
    console.error("[CS] auto trigger error", e);
  }
})();

// Listen for page -> script messages (existing flow)
window.addEventListener("message", (ev) => {
  if (!ev.data) return;
  const msg = ev.data;
  if (msg.type === "EXPORT_TO_EXTENSION" && msg.nonce) {
    console.log("[CS] window message received, nonce:", msg.nonce);
    chrome.runtime.sendMessage({ cmd: "EXPORT", nonce: msg.nonce }, (resp) => {
      console.log("[CS] response from background:", resp);
      window.postMessage({ type: "EXPORT_RESULT", result: resp }, "*");
    });
  }
});
