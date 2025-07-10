document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("read");

  if (!btn) return;

  btn.addEventListener("click", () => {
    if (!chrome.runtime || !chrome.runtime.connectNative) {
      document.getElementById("output").textContent =
        "Native messaging API unavailable.";
      return;
    }

    const port = chrome.runtime.connectNative("hr.toiletdoc.signer");

    port.onMessage.addListener((msg) => {
      document.getElementById("output").textContent = JSON.stringify(msg, null, 2);
    });

    port.onDisconnect.addListener(() => {
      const err = chrome.runtime.lastError;
      document.getElementById("output").textContent =
        "Connection interrupted: " + (err ? err.message : "erm... no error?");
    });

    port.postMessage({ action: "get_atr" });
  });
});
