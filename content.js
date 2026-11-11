(() => {
  const site = {
    "chatgpt.com": "chatgpt",
    "gemini.google.com": "gemini",
    "chat.deepseek.com": "deepseek",
    "grok.com": "grok"
  }[location.hostname];
  if (!site) return;
  const settingKey = `${site}Enabled`;
  const stopSelectors = {
    gemini: [
      '.send-button.stop',
      '[data-test-id="send-button-container"].stop',
      'button[aria-label="Stop response" i]',
      'gem-icon-button[aria-label="Stop response" i]',
      'gem-icon-button.send-button:has(mat-icon[data-mat-icon-name="stop_circle"])',
      'gem-icon-button.send-button:has(mat-icon[data-mat-icon-name="stop"])'
    ],
    deepseek: [
      '[role="button"][aria-label="Stop" i]',
      '[role="button"][aria-label="Stop generating" i]',
      '[role="button"][aria-label="停止生成"]',
      'button[aria-label="Stop" i]',
      'button[aria-label="Stop generating" i]',
      // DeepSeek's composer Stop control has no accessible label in some layouts.
      ':is(button, [role="button"]):has(svg path[d^="M2 4.88C2 3.68009"])'
    ],
    grok: [
      'button[aria-label="Stop model response" i]',
      'button[aria-label="Stop response" i]',
      'button[aria-label="Stop generating" i]',
      'form button[aria-label="Stop" i]'
    ],
    chatgpt: [
      'button[data-testid="stop-button"]',
      'button[data-testid="stop-streaming-button"]',
      'button[data-testid="stop-task-button"]',
      'button[data-testid="stop-run-button"]',
      'button[aria-label="Stop generating" i]',
      'button[aria-label="Stop streaming" i]',
      'form button[aria-label="Stop" i]',
      '[data-type="unified-composer"] button[aria-label="Stop" i]',
      // Newer composers identify their unlabeled Stop control by its square icon.
      'form[data-chatgpt-composer] button[type="button"].size-token-button-composer:has(svg.icon-primary-action > path[d="M4.5 5.75C4.5 5.05964 5.05964 4.5 5.75 4.5H14.25C14.9404 4.5 15.5 5.05964 15.5 5.75V14.25C15.5 14.9404 14.9404 15.5 14.25 15.5H5.75C5.05964 15.5 4.5 14.9404 4.5 14.25V5.75Z"])'
    ]
  };
  const stopSelector = stopSelectors[site].join(",");
  const generatingSelector = site === "grok" ? `${stopSelector}, [data-streaming="true"]` : stopSelector;
  const iconSelector = 'link[rel~="icon"]';
  const originals = new Map();
  const fallback = document.createElement("link");
  fallback.rel = "icon";

  const iconCache = new Map();
  const appliedIcons = new Set();

  function iconsFor(href) {
    if (!iconCache.has(href)) {
      iconCache.set(href, new Promise(resolve => {
        const image = new Image();
        image.crossOrigin = "anonymous";
        image.onerror = () => resolve(null);
        image.onload = () => {
          try {
            const canvas = document.createElement("canvas");
            canvas.width = canvas.height = 64;
            const context = canvas.getContext("2d");
            const icons = ["#9ca3af", null, "#3b82f6"].map(color => {
              context.clearRect(0, 0, 64, 64);
              context.drawImage(image, 0, 0, 64, 64);
              if (color) {
                context.globalCompositeOperation = "destination-out";
                context.beginPath();
                context.arc(52, 52, 12, 0, Math.PI * 2);
                context.fill();
                context.globalCompositeOperation = "source-over";
                context.fillStyle = color;
                context.beginPath();
                context.arc(52, 52, 10, 0, Math.PI * 2);
                context.fill();
              }
              const url = canvas.toDataURL("image/png");
              appliedIcons.add(url);
              return url;
            });
            resolve(icons);
          } catch {
            resolve(null);
          }
        };
        image.src = href;
      }));
    }
    return iconCache.get(href);
  }

  let state = "idle";
  let route = location.pathname;
  let finishTimer;
  let queued = false;
  let cancelled = false;
  let blinkTimer;
  let dotVisible = true;
  let renderVersion = 0;
  let enabled = false;
  let masterEnabled = false;

  function viewed() {
    return document.visibilityState === "visible" && document.hasFocus();
  }

  async function render() {
    const version = ++renderVersion;
    if (state === "working" && blinkTimer === undefined) {
      dotVisible = true;
      blinkTimer = setInterval(() => {
        dotVisible = !dotVisible;
        render();
      }, 650);
    } else if (state !== "working") {
      clearInterval(blinkTimer);
      blinkTimer = undefined;
    }

    if (state === "idle") {
      for (const [link, attrs] of originals) {
        // Leave a newer favicon supplied by the site intact.
        if (appliedIcons.has(link.getAttribute("href"))) {
          for (const [name, value] of Object.entries(attrs)) {
            if (value === null) link.removeAttribute(name);
            else link.setAttribute(name, value);
          }
        }
      }
      originals.clear();
      fallback.remove();
      return;
    }

    const links = [...document.querySelectorAll(iconSelector)].filter(link => link !== fallback);
    const candidates = links.filter(link => !link.media || matchMedia(link.media).matches);
    // Grok's SVG contains an HTML blur layer; use its PNG for canvas drawing.
    const preferredType = site === "grok" ? "image/png" : "image/svg+xml";
    const native = candidates.find(link => (originals.get(link)?.type ?? link.getAttribute("type")) === preferredType) || candidates.at(-1);
    const href = (native && (originals.get(native)?.href ?? native.getAttribute("href"))) || "/favicon.ico";
    const icons = await iconsFor(href);
    // An image may finish loading after the tab was read or generation restarted.
    if (!icons || version !== renderVersion) return;
    const icon = state === "done" ? icons[2] : icons[dotVisible ? 0 : 1];
    for (const link of links) {
      if (!link.isConnected || link.getAttribute("href") === icon) continue;
      if (!appliedIcons.has(link.getAttribute("href"))) {
        originals.set(link, Object.fromEntries(
          ["href", "type", "sizes"].map(name => [name, link.getAttribute(name)])
        ));
      }
      link.setAttribute("href", icon);
      link.setAttribute("type", "image/png");
      link.setAttribute("sizes", "any");
    }
    if (!links.length) {
      if (fallback.getAttribute("href") !== icon) fallback.href = icon;
      if (!fallback.isConnected) document.head.append(fallback);
    } else {
      fallback.remove();
    }
  }

  function check() {
    queued = false;
    if (!enabled || !masterEnabled) {
      clearTimeout(finishTimer);
      finishTimer = undefined;
      state = "idle";
      cancelled = false;
      render();
      return;
    }
    const generating = [...document.querySelectorAll(generatingSelector)].some(
      button => button.getClientRects().length > 0 && getComputedStyle(button).visibility !== "hidden"
    );

    if (route !== location.pathname) {
      route = location.pathname;
      // A new chat gets its URL after generation starts.
      if (!(state === "working" && generating)) {
        clearTimeout(finishTimer);
        finishTimer = undefined;
        state = "idle";
        cancelled = false;
      }
    }

    if (generating) {
      clearTimeout(finishTimer);
      finishTimer = undefined;
      if (state !== "working") cancelled = false;
      state = "working";
    } else if (state === "working" && finishTimer === undefined) {
      // Ignore brief control swaps during thinking or tool use.
      finishTimer = setTimeout(() => {
        state = cancelled || viewed() ? "idle" : "done";
        finishTimer = undefined;
        render();
      }, 800);
    } else if (state === "done" && viewed()) {
      state = "idle";
    }
    render();
  }

  function schedule() {
    if (queued) return;
    queued = true;
    setTimeout(check, 60);
  }

  document.addEventListener("click", event => {
    if (event.target instanceof Element && event.target.closest(stopSelector)) cancelled = true;
  }, true);
  document.addEventListener("visibilitychange", check);
  window.addEventListener("focus", check);
  window.addEventListener("popstate", check);
  new MutationObserver(schedule).observe(document.documentElement, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ["data-testid", "data-test-id", "data-mat-icon-name", "data-streaming", "aria-label", "class", "style", "hidden", "href", "rel", "d"]
  });
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== "local" || !(changes[settingKey] || changes.masterEnabled)) return;
    if (changes[settingKey]) enabled = changes[settingKey].newValue !== false;
    if (changes.masterEnabled) masterEnabled = changes.masterEnabled.newValue !== false;
    check();
  });
  chrome.storage.local.get({ enabled: true, masterEnabled: true, [settingKey]: null }).then(settings => {
    // Keep the old switch setting for existing ChatGPT users.
    enabled = settings[settingKey] ?? (site === "chatgpt" ? settings.enabled !== false : true);
    masterEnabled = settings.masterEnabled !== false;
    check();
  });
  setInterval(check, 1000);
})();
