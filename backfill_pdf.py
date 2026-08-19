#!/usr/bin/env python3
"""Backfill transcript PDFs for listening exercises, and re-parse audio/imgs
since scrape2 was edited. Uses cloudscraper."""
import json
import os
import re
import time

import cloudscraper

session = cloudscraper.create_scraper()
BASE = "/home/ubuntu/n5_listening/exercises"


def url_of(n):
    if n <= 29:
        return f"https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-listening-exercise-{n}/"
    return f"https://japanesetest4you.com/jlpt-n5-listening-test-{n}/"


def get(url):
    for _ in range(3):
        try:
            r = session.get(url, timeout=30)
            if r.status_code == 200:
                return r
        except Exception:
            time.sleep(3)
    return None


for n in range(1, 44):
    d = os.path.join(BASE, f"exercise_{n:02d}")
    jpath = os.path.join(d, "exercise.json")
    with open(jpath) as f:
        data = json.load(f)
    missing_pdf = not data.get("transcript_pdf")
    existing_pdf = bool(re.search(r"n5-listening-\d+\.pdf$", os.path.join(d, "")))
    need_page = missing_pdf
    if not need_page:
        continue
    r = get(url_of(n))
    if not r:
        print(f"ex{n}: page failed")
        continue
    html, text = r.text, re.sub(r"<[^>]+>", "\n", r.text)
    # re-parse audios/images with fixed regex (only if missing)
    audios = data.get("audios") or []
    imgs = data.get("images") or []
    if not audios:
        audios = list(dict.fromkeys(re.findall(r'<audio[^>]+src="(https://japanesetest4you\.com/[^"]+\.mp3)"', html)))
    if not imgs:
        imgs = list(dict.fromkeys(re.findall(r'<img[^>]+src="(https://japanesetest4you\.com/(?:image|images)/[^"]+)"', html)))
    pdf_m = re.search(r"https://japanesetest4you\.com/pdf/[^\s<>\"')\]]+\.pdf", html)
    pdf = pdf_m.group(0) if pdf_m else None

    # download media not yet on disk
    have_audio = [f for f in os.listdir(d) if "_audio" in f]
    for i, a in enumerate(audios, 1):
        if not any(f"question_{i}_audio" in f for f in os.listdir(d)):
            ext = os.path.splitext(a.split("?")[0])[1] or ".mp3"
            r2 = get(a)
            if r2:
                open(os.path.join(d, f"question_{i}_audio{ext}"), "wb").write(r2.content)
            time.sleep(0.15)
    have_img = [f for f in os.listdir(d) if not f.endswith((".json", ".md", ".pdf")) and "_audio" not in f]
    for i, img in enumerate(imgs, 1):
        if not any(f"question_{i}" == os.path.splitext(f)[0] for f in have_img):
            ext = os.path.splitext(img.split("?")[0])[1] or ".jpg"
            r2 = get(img)
            if r2:
                open(os.path.join(d, f"question_{i}{ext}"), "wb").write(r2.content)
            time.sleep(0.15)

    data["audios"] = audios
    data["images"] = imgs
    data["transcript_pdf"] = pdf
    with open(jpath, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    if pdf:
        name = os.path.basename(pdf)
        r2 = get(pdf)
        if r2:
            open(os.path.join(d, name), "wb").write(r2.content)
        time.sleep(0.15)
    # rewrite exercise.md
    lines = [f"# {data.get('title','')}", "", "Source: https://japanesetest4you.com", "", "## Answer Key"]
    for ans in data.get("answers", []):
        lines.append(f"- Question {ans['question']}: {ans['answer']}")
    lines.append("")
    if data.get("vocabulary"):
        lines += ["## New Words", "| Japanese | Romaji | English |", "|---|---|---|"]
        for v in data["vocabulary"]:
            lines.append(f"| {v['jp']} | {v['romaji']} | {v['en']} |")
        lines.append("")
    with open(os.path.join(d, "exercise.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"ex{n}: pdf={bool(pdf)} audios={len(audios)} imgs={len(imgs)}")
    time.sleep(0.2)
print("backfill done")
