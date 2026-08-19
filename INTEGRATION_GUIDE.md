# How to Use This Repository in Your Japanese Learning App

This guide explains how to add the downloaded JLPT N5 resources to your app.

## Download the Repository

Clone it anywhere on your computer:

```bash
git clone https://github.com/HosnainRafi/jlpt-n5-resources.git
```

Or simply download the ZIP from the GitHub page: https://github.com/HosnainRafi/jlpt-n5-resources

## Folder Layout

| Folder | Contents |
|---|---|
| `listening/` | 43 listening exercises: audio (`.mp3`), question images (`.jpg`), transcript PDFs, answer keys, vocabulary |
| `grammar/` | 26 grammar exercises: questions with 4 options, answer key with explanations, vocabulary |
| `kanji/` | 19 kanji exercises: same structure as grammar |
| `reading/` | 14 reading exercises: passages, questions, answer keys, vocabulary, passage images |
| `vocabulary/` | 24 vocabulary exercises: sentence questions, answers, vocabulary |
| `lists/` | Reference lists: full N5 vocabulary list (JSON/CSV/Markdown), grammar list, kanji list, printable grammar PDF and infographic images |
| `master_vocabulary.csv` | One file with all 1,874 unique vocabulary words from every exercise |

## The Simple Rule: One JSON Per Exercise

Every exercise folder contains an `exercise.json` file. This is the file your app should read — it has everything:

```json
{
  "title": "JLPT N5 – Listening Exercise 01",
  "audios": ["https://...mp3"],
  "images": ["https://...jpg"],
  "answers": [
    { "question": 1, "answer": "2", "explanation": "..." }
  ],
  "vocabulary": [
    { "jp": "図書館", "romaji": "toshokan", "en": "library" }
  ]
}
```

For grammar, kanji, reading, and vocabulary tests, the JSON also contains a `questions` array, each with `text` (the question) and `options` (the four answer choices).

## Naming Convention (Easy to Load in Bulk)

Files inside each exercise folder are named consistently:

- `question_1_audio.mp3` ... `question_5_audio.mp3` — audio clips (listening tests only)
- `question_1.jpg` ... `question_5.jpg` — the question image shown for each question
- `reading_image_1.jpg` — images inside reading passages
- `n5-listening-N.pdf` — official transcript PDF (listening tests only)

So in your app, playing audio for question 3 of exercise 12 is just loading:
`listening/exercise_12/question_3_audio.mp3`

## The index.json Files

Each category folder has an `index.json` that summarizes all its exercises (title, question count, vocab count, file names, source URL). Use it to build exercise selection screens without parsing every folder.

## Quick Workflow for Adding Listening Practice

1. User picks "Listening Exercise N" from your list (read from `listening/index.json`).
2. Show `listening/exercise_NN/question_1.jpg` and play `question_1_audio.mp3`.
3. Collect the user's answer; check against `exercise.json` → `answers` → `answer` field.
4. On "Check" / "Read More", reveal the answer and the `vocabulary` array as the new words list.
5. Optionally link the transcript: `n5-listening-N.pdf`.

## Credits

All content comes from [japanesetest4you.com](https://japanesetest4you.com/). If you publish the app, credit the original site and review its terms of use.
