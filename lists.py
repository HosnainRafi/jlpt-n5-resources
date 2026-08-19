#!/usr/bin/env python3
"""Extract N5 reference lists: vocabulary, grammar, kanji (if exists)."""
import json
import os
import re
import time

import cloudscraper

session = cloudscraper.create_scraper()
BASE = "/home/ubuntu/n5_listening/lists"
os.makedirs(BASE, exist_ok=True)


def get(url):
    for _ in range(3):
        try:
            r = session.get(url, timeout=30)
            if r.status_code == 200:
                return r
        except Exception:
            time.sleep(3)
    return None


def save_json(name, data):
    with open(os.path.join(BASE, name), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    n = len(data.get("items", data)) if isinstance(data, dict) else len(data)
    print(f"saved {name} ({n} items)")


def dl(url, dest):
    r = get(url)
    if r:
        open(os.path.join(BASE, dest), "wb").write(r.content)
        print(f"downloaded {dest}")
    else:
        print(f"FAILED {dest}")


# ---------- Vocabulary list ----------
r = get("https://japanesetest4you.com/jlpt-n5-vocabulary-list/")
voc = []
if r:
    html = r.text
    # plain-text word entries: "jp (romaji): en" lines anywhere (some inside links)
    for m in re.finditer(r"([\u3040-\u30FF\u4E00-\u9FFF][^\n<>]{0,40})\s*\(([\w\-\./ ]+?)\)\s*:\s*([^\n<]+)", html):
        jp, rom, en = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if en and jp and not jp.startswith("http") and len(jp) < 30:
            voc.append({"jp": jp, "romaji": rom, "en": en})
    # dedupe preserving order
    seen, uniq = set(), []
    for v in voc:
        key = (v["jp"], v["en"])
        if key not in seen:
            seen.add(key)
            uniq.append(v)
    voc = uniq
    save_json("n5_vocabulary_list.json", voc)
    # md + csv
    lines = ["# JLPT N5 Vocabulary List", "", "| Japanese | Romaji | English |", "|---|---|---|"]
    for v in voc:
        lines.append(f"| {v['jp']} | {v['romaji']} | {v['en']} |")
    open(os.path.join(BASE, "n5_vocabulary_list.md"), "w").write("\n".join(lines) + "\n")
    import csv
    with open(os.path.join(BASE, "n5_vocabulary_list.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["japanese", "romaji", "english"])
        for v in voc:
            w.writerow([v["jp"], v["romaji"], v["en"]])

# ---------- Grammar list ----------
r = get("https://japanesetest4you.com/jlpt-n5-grammar-list/")
gram = []
if r:
    html = r.text
    # HTML: <a href="flashcard/...">jp (romaji)</a>: meaning
    for m in re.finditer(r'<a href="(https://japanesetest4you\.com/flashcard/[^"]+)"[^>]*>([\u3040-\u30FF\u4E00-\u9FFF][^<]{0,40})</a>:\s*([^<\n]{2,80})', html):
        url, jp, en = m.group(1), m.group(2).strip(), m.group(3).strip()
        mm = re.search(r"\(([a-zA-Z0-9\-\./ ]{1,40})\)\s*$", jp)
        rom = mm.group(1) if mm else ""
        jp_clean = re.sub(r"\s*\([^)]*\)\s*$", "", jp).strip()
        jp_clean = jp_clean.replace("\u00a0", " ")
        if jp_clean:
            gram.append({"jp": jp_clean, "romaji": rom, "meaning": en, "url": url})
    seen, uniq = set(), []
    for v in gram:
        if v["jp"] not in seen:
            seen.add(v["jp"])
            uniq.append(v)
    save_json("n5_grammar_list.json", uniq)
    lines = ["# JLPT N5 Grammar List", "", "| Grammar Point | Romaji | Meaning | Link |", "|---|---|---|---|"]
    for v in uniq:
        lines.append(f"| {v['jp']} | {v['romaji']} | {v['meaning']} | {v['url']} |")
    open(os.path.join(BASE, "n5_grammar_list.md"), "w").write("\n".join(lines) + "\n")
    # infographic images
    for img in re.findall(r'https://japanesetest4you\.com/wp-content/uploads/[^\s"\']+\.(?:jpg|jpeg|png)', html):
        name = os.path.basename(img.split("?")[0])
        dl(img, name)
    dl("https://japanesetest4you.com/pdf/jlpt-n5-grammar-list.pdf", "jlpt-n5-grammar-list.pdf")

# ---------- Kanji list (guessed URL) ----------
r = get("https://japanesetest4you.com/jlpt-n5-kanji-list/")
if r and r.status_code == 200 and len(r.text) > 5000:
    kan = []
    html = r.text
    for m in re.finditer(r"([\u4E00-\u9FFF]{1,4})\s*\(([\w\-\./ ]+?)\)\s*:\s*([^\n<]{2,80})", html):
        jp, rom, en = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if en and len(jp) <= 4:
            kan.append({"kanji": jp, "romaji": rom, "meaning": en})
    seen, uniq = set(), []
    for v in kan:
        if v["kanji"] not in seen:
            seen.add(v["kanji"])
            uniq.append(v)
    save_json("n5_kanji_list.json", uniq)
    lines = ["# JLPT N5 Kanji List", "", "| Kanji | Reading | Meaning |", "|---|---|---|"]
    for v in uniq:
        lines.append(f"| {v['kanji']} | {v['romaji']} | {v['meaning']} |")
    open(os.path.join(BASE, "n5_kanji_list.md"), "w").write("\n".join(lines) + "\n")
else:
    print("no kanji list page found at guessed URL")

print("lists done")
