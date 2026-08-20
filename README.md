# JLPT Practice Resources (N5 + N4–N1)

A complete, organized collection of JLPT practice resources from [japanesetest4you.com](https://japanesetest4you.com/). This repository contains **all JLPT N5–N1 practice content** — 748 exercises in total, plus reference vocabulary/grammar/kanji lists for every level and consolidated datasets. The N4, N3, N2, and N1 content is stored **separately** from the N5 content in its own top-level folders. Everything is structured for easy integration into a learning app.

> Content source: japanesetest4you.com — free JLPT practice tests. Please credit the original site and comply with its terms of use when redistributing.

## Repository Structure

```
jlpt-n5-resources/
├── README.md
├── index_nx.json                # Consolidated index for all N4–N1 content
├── master_vocabulary.csv        # All 1,874 unique N5 vocab words from every exercise
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
├── n1/ … n4/                    # JLPT N1–N4 content (stored separately, see below)
├── lists/                       # N5 reference lists
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

## Optional Content

The `optional/` directory contains content that is **not required** for the JLPT N5 experience and can be excluded from your app entirely. Currently it holds one section:

| Section | Description |
|---|---|
| `optional/keigo/` | Keigo (敬語) polite speech lesson — verb table (plain/sonkeigo/kenjougo/teineigo), usage explanations, N1 patterns, and a 20-question practice quiz ([learn-japanese.org/en/keigo](https://learn-japanese.org/en/keigo)) |

## Notes for App Integration

1. **Listening exercises** pair each `question_N_audio.mp3` with `question_N.jpg` and an answer in `exercise.json` `answers[question-1]`.
2. **Multiple-choice** answers are option numbers 1–4; `explanation` repeats the correct sentence (listening/reading) or the corrected sentence (grammar/vocab).
3. Use `master_vocabulary.csv` as a unified word bank, or per-exercise `vocabulary` arrays for contextual study.
4. Audio file naming is consistent (`question_N_audio.mp3`), so playback can be mapped directly to question index.

## JLPT N4–N1 (Stored Separately)

The higher levels are stored in their own top-level folders (`n1/`, `n2/`, `n3/`, `n4/`) so you can include or exclude any level independently. Each level has the same structure as the N5 content, plus a per-level `README.md` and consolidated reference lists in `lists/<level>/`.

```text
jlpt-n5-resources/
├── n1/          # JLPT N1 (165 exercises) + lists/n1/ (vocab, grammar, PDFs)
├── n2/          # JLPT N2 (161 exercises) + lists/n2/
├── n3/          # JLPT N3 (132 exercises) + lists/n3/
├── n4/          # JLPT N4 (168 exercises) + lists/n4/
└── index_nx.json   # Full machine-readable index of every N4–N1 exercise
```

Each exercise folder (`n4/grammar/exercise_01/` etc.) contains `exercise.json` (questions, options, answer key, vocabulary, media URLs), `exercise.md`, and the media files (`question_N_audio.mp3`, `question_N.jpg`, transcript PDFs for listening).

| Level | Listening | Grammar | Kanji | Reading | Vocabulary | Total | Reference Lists |
|---|---|---|---|---|---|---|---|
| N4 | 54 | 35 | 22 | 21 | 36 | **168** | vocab (533), grammar (98), kanji (167), grammar PDF |
| N3 | 22 | 34 | 34 | 16 | 26 | **132** | vocab (1,696), grammar (117), kanji (370), grammar PDF |
| N2 | 35 | 30 | 24 | 41 | 31 | **161** | vocab (1,545), grammar (199), grammar PDF |
| N1 | 28 | 31 | 24 | 55 | 27 | **165** | vocab (436), grammar (214), grammar PDF |
| **Total** | **139** | **130** | **104** | **133** | **120** | **622** | |

The reference lists in `lists/<level>/` are fully structured JSON (`vocabulary.json`, `grammar.json`, `kanji.json` where available) with romaji and English meanings for every entry, plus the official printable grammar PDFs and vocabulary infographics.

> Note: The website does not host separate N2/N1 kanji list pages, so kanji reference lists exist only for N3–N5. All N4–N1 listening exercises include real audio (`.mp3`), question images, and transcript PDFs, identical to the N5 structure.
