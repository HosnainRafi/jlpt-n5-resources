#!/usr/bin/env python3
"""Cleanup lists: fix html entities, dedupe images, add missing entries from plain-text lines."""
import glob
import json
import os
import re
import html as htmlmod

BASE = "/home/ubuntu/n5_listening/lists"

# fix grammar jp entities like "で (de)&nbsp;&#8211; 1"
g = json.load(open(f"{BASE}/n5_grammar_list.json"))
for v in g:
    v["jp"] = htmlmod.unescape(v["jp"]).replace("\xa0", " ")
    m = re.search(r"\(([a-zA-Z0-9\-\./ ]{1,40})\)\s*$", v["jp"])
    if m and not v["romaji"]:
        v["romaji"] = m.group(1)
json.dump(g, open(f"{BASE}/n5_grammar_list.json", "w"), ensure_ascii=False, indent=2)
# rewrite md
lines = ["# JLPT N5 Grammar List", "", "| Grammar Point | Romaji | Meaning | Link |", "|---|---|---|---|"]
for v in g:
    lines.append(f"| {v['jp']} | {v['romaji']} | {v['meaning']} | {v['url']} |")
open(f"{BASE}/n5_grammar_list.md", "w").write("\n".join(lines) + "\n")
print("grammar cleaned:", len(g))

# fix kanji jp entities
k = json.load(open(f"{BASE}/n5_kanji_list.json"))
for v in k:
    v["kanji"] = htmlmod.unescape(v["kanji"])
json.dump(k, open(f"{BASE}/n5_kanji_list.json", "w"), ensure_ascii=False, indent=2)
lines = ["# JLPT N5 Kanji List", "", "| Kanji | Reading | Meaning |", "|---|---|---|"]
for v in k:
    lines.append(f"| {v['kanji']} | {v['romaji']} | {v['meaning']} |")
open(f"{BASE}/n5_kanji_list.md", "w").write("\n".join(lines) + "\n")
print("kanji cleaned:", len(k))

# keep only full-size images
for f in glob.glob(f"{BASE}/*-150x150.jpg") + glob.glob(f"{BASE}/*-300x300.jpg") + glob.glob(f"{BASE}/*-s.jpg"):
    os.remove(f)
for f in glob.glob(f"{BASE}/*-1-s.jpg"):
    os.remove(f)
# remove accidental logo/ad
for f in ["logo-jt4u-2.png", "MAINPAGE-AD-small.jpg"]:
    p = f"{BASE}/{f}"
    if os.path.exists(p):
        os.remove(p)
print("images:", os.listdir(f"{BASE}"))
