# JLPT N5 Practice Resources

A complete, organized collection of JLPT N5 practice resources from [japanesetest4you.com](https://japanesetest4you.com/). This repository contains **43 listening tests, 26 grammar tests, 19 kanji tests, 14 reading tests, and 24 vocabulary tests** — 126 exercises in total — plus reference lists and consolidated datasets. Everything is structured for easy integration into a learning app.

> Content source: japanesetest4you.com — free JLPT practice tests. Please credit the original site and comply with its terms of use when redistributing.

## Repository Structure

```
jlpt-n5-resources/
├── README.md
├── master_vocabulary.csv        # All 1,874 unique vocab words from every exercise
├── listening/                   # 43 listening exercises
│   ├── index.json
│   └── exercise_01 … exercise_43/
│       ├── exercise.json        # Structured data (audio URLs, answer key, vocab)
│       ├── exercise.md          # Human-readable version
│       ├── question_N_audio.mp3 # Audio for each question
│       ├── question_N.jpg       # Question image for each question
│       └── n5-listening-N.pdf   # Official transcript PDF
├── grammar/                     # 26 grammar exercises
├── kanji/                       # 19 kanji exercises
├── reading/                     # 14 reading exercises (includes reading_image_N.jpg)
├── vocabulary/                  # 24 vocabulary exercises
└── lists/                       # Reference lists
    ├── n5_vocabulary_list.csv   # Full N5 vocabulary list (549 words)
    ├── n5_vocabulary_list.md / .json
    ├── n5_grammar_list.md / .json
    ├── n5_kanji_list.md / .json
    ├── jlpt-n5-grammar-list.pdf # Printable grammar list
    ├── grammar-list-n5.jpg
    └── infographic-jlpt-n5-grammar.jpg / -2.jpg
```

## How Each Exercise Folder Works

Every exercise folder follows the same convention, so your app can load them uniformly:

| File | Purpose |
|---|---|
| `exercise.json` | All structured data for the exercise |
| `exercise.md` | Human-readable version (questions, answer key, vocab table) |
| `question_N_audio.mp3` | Audio clip for question N (listening only) |
| `question_N.jpg` | The question image shown for question N |
| `reading_image_N.jpg` | Images used in reading comprehension (reading only) |
| `n5-listening-N.pdf` | Official transcript PDF (listening only) |

The `index.json` file in each category folder gives a quick overview of every exercise (title, question count, file names, source URL) without having to parse each folder individually.

## Key Fields in `exercise.json`

```json
{
  "title": "JLPT N5 – Listening Exercise 01",
  "source_url": "https://japanesetest4you.com/...",
  "audios": [  ],   // original online audio URLs
  "images": [  ],   // original online image URLs
  "transcript_pdf": "https://.../n5-listening-1.pdf",
  "questions": [    // grammar/kanji/reading/vocab only
    { "question": 1, "text": "...", "options": ["...","...","...","..."] }
  ],
  "answers": [      // all categories
    { "question": 1, "answer": "2", "explanation": "..." }
  ],
  "vocabulary": [   // "New words" section from each exercise
    { "jp": "食べる", "romaji": "taberu", "en": "to eat" }
  ]
}
```

## Stats at a Glance

| Category | Exercises | Questions | Vocab Words | Media |
|---|---|---|---|---|
| Listening | 43 | ~228 | 1,269 | 223 audio clips, 228 images, 43 PDFs |
| Grammar | 26 | 260 | ~590 | text-based |
| Kanji | 19 | 190 | ~370 | text-based |
| Reading | 14 | ~75 | ~620 | 46 reading images |
| Vocabulary | 24 | 240 | ~900 | text-based |
| **Total** | **126** | **~993** | **1,874 unique** | **~550 files** |

## Notes for App Integration

1. **Listening exercises** pair each `question_N_audio.mp3` with `question_N.jpg` and an answer in `exercise.json` `answers[question-1]`.
2. **Multiple-choice** answers are option numbers 1–4; `explanation` repeats the correct sentence (listening/reading) or the corrected sentence (grammar/vocab).
3. Use `master_vocabulary.csv` as a unified word bank, or per-exercise `vocabulary` arrays for contextual study.
4. Audio file naming is consistent (`question_N_audio.mp3`), so playback can be mapped directly to question index.
