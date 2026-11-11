# TabSignal

**Four AI tabs are cooking. You have one brain cell left to check them all.**

![The tab situation](promo/readme/overwhelmed.jpg)

TabSignal puts a tiny status dot on the favicon for ChatGPT, Gemini, DeepSeek,
and Grok. Keep doing literally anything else while the bots cook.

## The dot lore

- **Blinking grey:** the AI is still generating. Let him cook.
- **Blue:** it finished while you were away. Your answer has entered the chat.
- **No dot:** idle, or you came back and saw the update. We are so back.

The dot sits over the existing favicon without resizing the logo. When you
return to the tab, the blue “ready” state clears. Refreshing the page clears it
too.

![The cat has reviewed the workflow](promo/readme/cat-approval.jpg)

## Install it locally

No build step. No account. No “connect your wallet” side quest.

1. Download or clone this repository.
2. In Chrome or Brave, open `chrome://extensions` (or `brave://extensions`),
   turn on **Developer mode**, then choose **Load unpacked** and select this
   folder.
3. In Firefox, open `about:debugging`, choose **This Firefox**, then **Load
   Temporary Add-on** and select this folder's `manifest.json`.
4. Reload your open AI tabs. The dots are now in the cinematic universe.

Firefox temporary add-ons are removed when Firefox closes. A signed Firefox
release is required for an installation that persists between sessions.

After changing the extension files, press **Reload** on the extensions page,
then reload your AI tabs. Opening a new tab by itself does not reload the
extension.

## The control panel

Click the TabSignal toolbar icon to toggle the master switch or each supported
service separately. Changes apply right away and are saved in your browser's
local extension storage. The master switch pauses every site; turning it back
on restores your individual choices.

## Privacy, no plot twist

TabSignal runs on `chatgpt.com`, `gemini.google.com`, `chat.deepseek.com`, and
`grok.com`. It checks each page's response-generation control and the current
page state to decide which favicon dot to show. It also notices when you stop a
response or return to the tab. This is processed locally in your browser.

It does **not** read prompts, conversation text, or answers, and it does not
send page data or settings to a server. The only declared extension permission
is `storage`, used for your on-device preferences. Host access is limited to
the four supported sites.

Read the [full privacy policy](website/privacy-policy/index.html).

## Known limits, the season finale

- A site redesign can move or rename its Stop control, which may need a selector
  update in `content.js`.
- Blue means the generation stopped while you were away. It cannot tell whether
  the response succeeded or errored.
- A page reload clears the unread state. Closed or sleeping tabs cannot be
  monitored while they are not running.

