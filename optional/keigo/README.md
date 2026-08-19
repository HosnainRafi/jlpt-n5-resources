# Keigo (敬語) — Polite Speech — *Optional Content*

> **This section is OPTIONAL.** It is kept separate from the JLPT N5 content so you can include or exclude it from your app freely.

## Source

Content was extracted from [learn-japanese.org — Keigo](https://learn-japanese.org/en/keigo) (Respectful, humble, and polite language), targeted at N3–N1 learners.

## Files

| File | Description |
| --- | --- |
| `keigo.json` | All content in a single structured JSON file |

## What's inside `keigo.json`

The JSON file contains three parts:

1. **`sections.when_to_use`** — Explanations of the three keigo types (尊敬語 Sonkeigo, 謙譲語 Kenjougo, 丁寧語 Teineigo) plus the N1 construction patterns.
2. **`sections.verb_table`** — The master table of 12 common verbs with their plain, sonkeigo, kenjougo, and teineigo forms, each with English meaning and usage context. Every entry includes romaji for the plain form.
3. **`quiz`** — 20 practice questions (10 sonkeigo + 10 kenjougo) generated from the verb table, each with 4 options, the correct answer, and an explanation line.

## Audio note

The source website does not provide downloadable audio files for keigo; its pronunciation buttons use the browser's built-in **SpeechSynthesis API** with a `ja-JP` voice. In your app you can reproduce the same effect, for example in JavaScript:

```js
const u = new SpeechSynthesisUtterance('おっしゃる');
u.lang = 'ja-JP';
u.rate = 0.85;
speechSynthesis.speak(u);
```

Alternatively, any TTS service or recorded audio can be attached to the same words.
