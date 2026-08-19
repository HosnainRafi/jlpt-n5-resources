#!/usr/bin/env python3
"""Scrape all 43 JLPT N5 listening exercises from japanesetest4you.com.

Downloads audio, question images, transcript PDFs, and extracts
answer keys and new vocabulary into structured JSON + markdown files.
"""
import json
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}

BASE = "/home/ubuntu/n5_listening/exercises"
with open("/home/ubuntu/n5_listening/urls.txt") as f:
    URLS = [l.strip() for l in f if l.strip()]

session = requests.Session()
session.headers.update(HEADERS)


def get(url, retries=3):
    for i in range(retries):
        try:
            r = session.get(url, timeout=30)
            if r.status_code == 200:
                return r
            print(f"  [warn] HTTP {r.status_code} for {url}")
        except Exception as e:
            print(f"  [warn] request error ({e}), retry {i+1}/{retries}")
        time.sleep(2)
    return None


def extract_page(url):
    r = get(url)
    if r is None:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    entry = soup.select_one(".entry-content") or soup.body
    title_el = soup.select_one("h1.entry-title") or soup.find("h1")
    title = title_el.get_text(strip=True) if title_el else ""

    # Audio files
    audios = [a["src"] for a in entry.find_all("audio") if a.get("src")]

    # Question images (in entry, exclude logo/ads; images under /image/)
    imgs = [img["src"] for img in entry.find_all("img") if img.get("src")]
    imgs = [i for i in imgs if "/image/" in i]

    # Transcript PDF
    pdf_link = None
    for a in entry.find_all("a", href=True):
        if a["href"].endswith(".pdf"):
            pdf_link = a["href"]
            break

    # Answer key & new words: use full text of page (hidden 'more' content
    # included in raw HTML)
    text = soup.get_text("\n")

    answers = []
    m = re.search(r"Answer Key\s*:(.*?)(?=New words|JLPT N5 Kanji|\\n\\n\n)", text, re.S)
    if m:
        for line in m.group(1).strip().splitlines():
            line = line.strip()
            mm = re.match(r"Question\s+(\d+)\s*:\s*(.+)", line)
            if mm:
                answers.append({"question": int(mm.group(1)),
                                "answer": mm.group(2).strip()})

    vocab = []
    m = re.search(r"New words\s*:?(.*?)(?=View transcript|Learn JLPT|contact me)", text, re.S)
    if m:
        block = m.group(1).strip()
        for line in block.splitlines():
            line = line.strip()
            if not line or line in ("New words", "New words:"):
                continue
            # pattern: 日本語 (romaji): english
            mm = re.match(r"^(.+?)\s*\((.+?)\)\s*:\s*(.+)$", line)
            if mm:
                vocab.append({"jp": mm.group(1).strip(),
                              "romaji": mm.group(2).strip(),
                              "en": mm.group(3).strip()})
            else:
                vocab.append({"jp": line, "romaji": "", "en": ""})

    return {
        "url": url,
        "title": title,
        "audios": audios,
        "images": imgs,
        "transcript_pdf": pdf_link,
        "answers": answers,
        "vocabulary": vocab,
    }


def save(url, data):
    num = int(re.search(r"-(\d+)/?$", url.rstrip("/")).group(1))
    d = os.path.join(BASE, f"exercise_{num:02d}")
    os.makedirs(d, exist_ok=True)
    failures = []

    # metadata
    with open(os.path.join(d, "exercise.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    def download(path_url, filename):
        try:
            r = get(path_url)
            if r is None:
                failures.append((filename, "http_error"))
                return
            with open(os.path.join(d, filename), "wb") as f:
                f.write(r.content)
            return True
        except Exception as e:
            failures.append((filename, str(e)))
            return False

    for i, a in enumerate(data["audios"], start=1):
        ext = os.path.splitext(a.split("?")[0])[1] or ".mp3"
        download(a, f"question_{i}_audio{ext}")
        time.sleep(0.3)

    for i, img in enumerate(data["images"], start=1):
        ext = os.path.splitext(img.split("?")[0])[1] or ".jpg"
        download(img, f"question_{i}{ext}")
        time.sleep(0.3)

    if data["transcript_pdf"]:
        name = os.path.basename(data["transcript_pdf"])
        download(data["transcript_pdf"], name)
        time.sleep(0.3)

    # readme.md with full text content
    lines = [f"# {data['title']}", "", f"Source: {data['url']}", ""]
    if data["answers"]:
        lines.append("## Answer Key")
        for ans in data["answers"]:
            lines.append(f"- Question {ans['question']}: {ans['answer']}")
        lines.append("")
    if data["vocabulary"]:
        lines.append("## New Words")
        lines.append("| Japanese | Romaji | English |")
        lines.append("|---|---|---|")
        for v in data["vocabulary"]:
            lines.append(f"| {v['jp']} | {v['romaji']} | {v['en']} |")
        lines.append("")
    with open(os.path.join(d, "exercise.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

    return failures


def main():
    os.makedirs(BASE, exist_ok=True)
    all_results = []
    for idx, url in enumerate(URLS, start=1):
        num = int(re.search(r"-(\d+)/?$", url.rstrip("/")).group(1))
        print(f"[{idx}/{len(URLS)}] Extracting exercise {num} ...")
        data = extract_page(url)
        if data is None:
            all_results.append({"num": num, "status": "page_failed"})
            print("  !! page extraction failed")
            continue
        failures = save(url, data)
        status = "ok" if not failures else "partial"
        all_results.append({
            "num": num,
            "status": status,
            "title": data["title"],
            "audios": len(data["audios"]),
            "images": len(data["images"]),
            "transcript_pdf": bool(data["transcript_pdf"]),
            "answers": len(data["answers"]),
            "vocab": len(data["vocabulary"]),
            "download_failures": failures,
        })
        print(f"  -> {status}: {len(data['audios'])} audio, {len(data['images'])} imgs, "
              f"pdf={bool(data['transcript_pdf'])}, answers={len(data['answers'])}, "
              f"vocab={len(data['vocabulary'])}")
        if failures:
            print(f"  !! failures: {failures}")
        time.sleep(0.5)

    with open("/home/ubuntu/n5_listening/results.json", "w") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print("\nDone. Results saved to /home/ubuntu/n5_listening/results.json")


if __name__ == "__main__":
    main()
