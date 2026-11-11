const toggles = [...document.querySelectorAll("input[data-setting]")];
const master = document.getElementById("master-enabled");
const siteToggles = toggles.filter(toggle => toggle !== master);

function statusFor(toggle) {
  return document.getElementById(toggle.getAttribute("aria-describedby"));
}

function render() {
  statusFor(master).textContent = master.checked ? "AI tab status" : "All indicators paused";
  document.documentElement.dataset.enabled = String(master.checked && siteToggles.some(toggle => toggle.checked));
  document.documentElement.dataset.paused = String(!master.checked);
}

const defaults = { enabled: true, masterEnabled: true, chatgptEnabled: null, geminiEnabled: true, deepseekEnabled: true, grokEnabled: true };
chrome.storage.local.get(defaults).then(settings => {
  for (const toggle of toggles) {
    toggle.checked = settings[toggle.dataset.setting] ?? (settings.enabled !== false);
    toggle.disabled = false;
  }
  render();
}).catch(() => {
  master.disabled = true;
  for (const toggle of toggles) toggle.disabled = true;
});

for (const toggle of toggles) toggle.addEventListener("change", async () => {
  const enabled = toggle.checked;
  toggle.disabled = true;
  try {
    await chrome.storage.local.set({ [toggle.dataset.setting]: enabled });
    toggle.checked = enabled;
    render();
  } catch {
    toggle.checked = !enabled;
    render();
    statusFor(master).textContent = "Couldn't save. Try again.";
  } finally {
    toggle.disabled = false;
  }
});

chrome.storage.onChanged.addListener((changes, area) => {
  if (area !== "local") return;
  for (const toggle of toggles) {
    const change = changes[toggle.dataset.setting];
    if (change) toggle.checked = change.newValue !== false;
  }
  render();
});
