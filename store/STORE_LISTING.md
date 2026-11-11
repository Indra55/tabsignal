# Chrome Web Store listing: TabSignal

Copy-ready metadata for the Chrome Web Store Developer Dashboard.

## Listing fields

- **Name:** TabSignal
- **Summary (132-character limit):** Know when a ChatGPT, Gemini, DeepSeek or Grok response is still working or ready in another tab.
- **Category:** Productivity
- **Language:** English
- **Single purpose:** Show a favicon indicator for response generation on supported AI chat tabs and mark completed responses until the user returns.
- **Homepage URL:** Optional. Add a project page if you have one.
- **Support URL:** Add a support page or issue tracker before publication.
- **Privacy policy URL:** Publish `PRIVACY_POLICY.html` at a stable public URL and enter that URL here before publication.

## Detailed description

Know when to come back to an AI response without keeping its tab in front.

TabSignal adds a small status dot to supported ChatGPT, Gemini, DeepSeek and Grok tabs:

- A blinking grey dot means the response is generating.
- A blue dot means generation stopped while you were away. It clears when you return to the tab.
- The toolbar popup lets you toggle each service or pause all indicators.

TabSignal checks the response-control state in the supported page interface to detect generation. It processes that state locally, does not read conversation text, and does not send page data to a server. Preferences are saved in Chrome's local extension storage.

TabSignal is an independent extension and is not affiliated with or endorsed by OpenAI, Google, DeepSeek, or xAI.

## Privacy practices tab

- **Single purpose:** Use the statement above.
- **Permission: `storage`:** Stores the master and per-service indicator preferences in `chrome.storage.local` so they persist between browser sessions.
- **Supported-site access:** The content script runs only on `chatgpt.com`, `gemini.google.com`, `chat.deepseek.com`, and `grok.com`. It checks the page's response-control state to determine whether generation is active; it does not read message text.
- **Remote code:** No. All extension logic is packaged in the upload ZIP.
- **Data-use disclosure:** Disclose local processing of supported-page interface state and the supported site/domain context as necessary for the extension's single purpose. State that no page data is transmitted or shared and that preferences remain in local extension storage. Match the exact dashboard checkboxes to these disclosures.
- **Limited Use certification:** Certify only after reviewing the actual dashboard statements and confirming the listing and hosted policy match the shipped code.

## Listing assets

Upload these from `assets/`:

1. `store-icon-128.png` as the 128×128 store icon.
2. `screenshot-01-working.png`
3. `screenshot-02-controls.png`
4. `screenshot-03-ready.png`
5. `promo-small-440x280.png` as the small promo tile.
6. `promo-marquee-1400x560.png` as the optional marquee tile.

The screenshot panels are designed showcase images based on the shipped popup and behavior. The launch video is not a YouTube-hosted listing video, so it cannot be entered into the YouTube video field as-is.

## Before submitting

- Replace the publisher and support-contact placeholders in `PRIVACY_POLICY.html`.
- Publish the policy on a stable public URL and enter that URL in the dashboard.
- Add a real support URL and verify the publisher account contact email.
- Review the dashboard's data-use checkboxes against the explanation above. The extension reads supported-page interface state locally, even though it does not read conversation text or transmit page data.
- Upload `TabSignal-1.4.0.zip` from `package/`.
- Complete distribution settings, then review the final listing preview.
