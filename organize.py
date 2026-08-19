#!/usr/bin/env python3
"""Final organization: per-category index.json, master datasets, READMEs."""
import csv
import json
import os
import re

BASE = "/home/ubuntu/n5_listening"
CATS = {
    "listening": {"ex_dir": "exercises", "n": 43, "title": "JLPT N5 Listening Tests"},
    "grammar": {"n": 26, "title": "JLPT N5 Grammar Tests"},
    "kanji": {"n": 19, "title": "JLPT N5 Kanji Tests"},
    "reading": {"n": 14, "title": "JLPT N5 Reading Tests"},
    "vocabulary": {"n": 24, "title": "JLPT N5 Vocabulary Tests"},
}

SOURCE = "https://japanesetest4you.com"


def index_for(cat, cfg):
    exdir = cfg.get("ex_dir", "listening")
    items = []
    for n in range(1, cfg["n"] + 1):
        d = os.path.join(BASE, exdir, f"exercise_{n:02d}")
        if not os.path.isdir(d):
            continue
        data = json.load(open(f"{d}/exercise.json"))
        files = {
            "json": "exercise.json",
            "markdown": "exercise.md",
        }
        local_audios, local_imgs, local_pdf = [], [], []
        for f in sorted(os.listdir(d)):
            if f.endswith("_audio.mp3"):
                local_audios.append(f)
            elif re.match(r"question_\d+\.\w+$", f):
                local_imgs.append(f)
            elif f.endswith(".pdf"):
                local_pdf.append(f)
            elif re.match(r"reading_image_\d+", f):
                local_imgs.append(f)
        item = {
            "number": n,
            "title": data.get("title", ""),
            "source_url": data.get("source_url", f"{SOURCE}#{n}"),
            "question_count": len(data.get("questions", data.get("answers", []))),
            "answer_count": len(data.get("answers", [])),
            "vocabulary_count": len(data.get("vocabulary", [])),
            "audio_files": local_audios,
            "image_files": local_imgs,
            "transcript_pdf": local_pdf[0] if local_pdf else None,
        }
        items.append(item)
    out = {"category": cat, "title": cfg["title"], "exercise_count": len(items),
           "exercises": items}
    outdir = os.path.join(BASE, exdir)
    json.dump(out, open(f"{outdir}/index.json", "w"), ensure_ascii=False, indent=2)
    print(f"{cat}: {len(items)} exercises indexed")
    return items


def master_vocabulary():
    rows = []
    for cat in CATS:
        exdir = CATS[cat].get("ex_dir", "listening")
        for n in range(1, CATS[cat]["n"] + 1):
            d = os.path.join(BASE, exdir, f"exercise_{n:02d}")
            if not os.path.isdir(d):
                continue
            data = json.load(open(f"{d}/exercise.json"))
            for v in data.get("vocabulary", []):
                rows.append({
                    "japanese": v.get("jp", v.get("jp", "")),
                    "romaji": v.get("romaji", ""),
                    "english": v.get("en", v.get("meaning", "")),
                    "source_category": cat,
                    "source_exercise": n,
                })
    # dedupe by (jp, english)
    seen, uniq = set(), []
    for r in rows:
        key = (r["japanese"], r["english"])
        if key not in seen:
            seen.add(key)
            uniq.append(r)
    with open(f"{BASE}/master_vocabulary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["japanese", "romaji", "english", "source_category", "source_exercise"])
        w.writeheader()
        w.writerows(uniq)
    print("master_vocabulary.csv:", len(uniq), "unique words")


# set source_url fields from URL patterns
def patch_urls():
    for cat, cfg in CATS.items():
        exdir = cfg.get("ex_dir", "listening")
        for n in range(1, cfg["n"] + 1):
            p = os.path.join(BASE, exdir, f"exercise_{n:02d}/exercise.json")
            if not os.path.exists(p):
                continue
            data = json.load(open(p))
            if cat == "listening":
                url = f"{SOURCE}/japanese-language-proficiency-test-jlpt-n5-listening-exercise-{n}/" if n <= 29 else f"{SOURCE}/jlpt-n5-listening-test-{n}/"
            elif cat == "grammar":
                url = f"{SOURCE}/japanese-language-proficiency-test-jlpt-n5-grammar-exercise-{n}/"
            elif cat == "kanji":
                url = f"{SOURCE}/japanese-language-proficiency-test-jlpt-n5-kanji-exercise-{n}/"
            elif cat == "reading":
                url = f"{SOURCE}/japanese-language-proficiency-test-jlpt-n5-reading-exercise-{n}/"
                if n == 4:
                    url = f"{SOURCE}/japanese-language-proficiency-test-jlpt-n5-reading-exercise-0{n}/"
                elif n <= 11:
                    url = f"{SOURCE}/japanese-language-proficiency-test-jlpt-n5-reading-exercise-{n:02d}/"
                elif n in (12, 13):
                    url = f"{SOURCE}/jlpt-n5-reading-{n}/"
            else:
                url = f"{SOURCE}/japanese-language-proficiency-test-jlpt-n5-vocabulary-exercise-{n}/"
            data["source_url"] = url
            json.dump(data, open(p, "w"), ensure_ascii=False, indent=2)


patch_urls()
for cat, cfg in CATS.items():
    index_for(cat, cfg)
master_vocabulary()
