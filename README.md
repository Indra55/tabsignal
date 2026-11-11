# TabSignal

**Four AI tabs are cooking. You have one brain cell left to check them all.**

![The tab situation](promo/assets/overwhelmed.png)

TabSignal puts a tiny status dot on the favicon for ChatGPT, Gemini, DeepSeek,
and Grok. Keep doing literally anything else while the bots cook.

## The dot lore

- **Blinking grey:** the AI is still generating. Let him cook.
- **Blue:** it finished while you were away. Your answer has entered the chat.
- **No dot:** idle, or you came back and saw the update. We are so back.

The dot sits over the existing favicon without resizing the logo. When you
return to the tab, the blue “ready” state clears. Refreshing the page clears it
too.

![The cat has reviewed the workflow](promo/assets/cat-approval.png)

## Install it locally

No build step. No account. No “connect your wallet” side quest.

1. Download or clone this repository.
2. Open `chrome://extensions` (or `brave://extensions`).
3. Turn on **Developer mode**.
4. Choose **Load unpacked** and select this folder.
5. Reload your open AI tabs. The dots are now in the cinematic universe.

After changing the extension files, press **Reload** on the extensions page,
then reload your AI tabs. Opening a new tab by itself does not reload the
extension.

## The control panel

Click the TabSignal toolbar icon to toggle the master switch or each supported
service separately. Changes apply right away and are saved in Chrome's local
extension storage. The master switch pauses every site; turning it back on
restores your individual choices.

## Privacy, no plot twist

TabSignal runs on `chatgpt.com`, `gemini.google.com`, `chat.deepseek.com`, and
`grok.com`. It checks each page's response-generation control and the current
page state to decide which favicon dot to show. It also notices when you stop a
response or return to the tab. This is processed locally in your browser.

It does **not** read prompts, conversation text, or answers, and it does not
send page data or settings to a server. The only declared extension permission
is `storage`, used for your on-device preferences. Host access is limited to
the four supported sites.

## Known limits, the season finale

- A site redesign can move or rename its Stop control, which may need a selector
  update in `content.js`.
- Blue means the generation stopped while you were away. It cannot tell whether
  the response succeeded or errored.
- A page reload clears the unread state. Closed or sleeping tabs cannot be
  monitored while they are not running.

## Chrome Web Store files

The `store/` folder contains the listing draft, screenshots, and package helper.
Build the upload ZIP from the project root with:

```sh
python3 store/build_package.py
```

The privacy policy draft still needs the publisher name and support contact
filled in and hosted at a public URL before store submission.
