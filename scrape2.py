#!/usr/bin/env python3
"""Full scraper for japanesetest4you.com N5 resources using cloudscraper
(which passes Cloudflare JS challenge)."""
import json
import os
import re
import sys
import time

import cloudscraper

session = cloudscraper.create_scraper()
import sys as _sys; _cat = _sys.argv[2] if len(_sys.argv)>2 else "exercises"; BASE = f"/home/ubuntu/n5_listening/{_cat}"


def get(url, retries=3):
    for i in range(retries):
        try:
            r = session.get(url, timeout=30)
            if r.status_code == 200:
                return r
            print(f"  [warn] HTTP {r.status_code} for {url}")
        except Exception as e:
            print(f"  [warn] error ({e}), retry {i+1}/{retries}")
        time.sleep(3)
    return None


def parse(html, text):
    audios = re.findall(r'<audio[^>]+src="(https://japanesetest4you\.com/[^"]+\.mp3)"', html)
    audios = list(dict.fromkeys(audios))  # preserve order, dedupe
    imgs = re.findall(r'<img[^>]+src="(https://japanesetest4you\.com/(?:image|images)/[^"]+)"', html)
    imgs = list(dict.fromkeys(imgs))

    pdf_m = re.search(r"https://japanesetest4you\.com/pdf/[^\s\"')\]]+", text)
    pdf = pdf_m.group(0) if pdf_m else None

    answers = []
    m = re.search(r"Answer Key\s*[:\n](.*?)(?=JLPT N5 Kanji|New words|\Z)", text, re.S | re.I)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"\s*Question\s+(\d+)\s*:\s*(.+)", line.strip())
            if mm:
                answers.append({"question": int(mm.group(1)), "answer": mm.group(2).strip()})

    vocab = []
    m = re.search(r"New words\s*:?\s*\n(.*?)(?=View transcript|Learn JLPT|Grammar Audio|Vocabulary Audio|Infographics|contact me|\Z)", text, re.S | re.I)
    if m:
        for line in m.group(1).splitlines():
            line = line.strip().strip("*_")
            if not line or re.match(r"^New words", line, re.I):
                continue
            mm = re.match(r"^(.+?)\s*\((.+?)\)\s*:\s*(.+)$", line)
            if mm:
                vocab.append({"jp": mm.group(1).strip(), "romaji": mm.group(2).strip(), "en": mm.group(3).strip()})
            else:
                vocab.append({"jp": line, "romaji": "", "en": ""})
    return audios, imgs, pdf, answers, vocab


def save(num, title, audios, imgs, pdf, answers, vocab, prefix="exercise"):
    d = os.path.join(BASE, f"{prefix}_{num:02d}")
    os.makedirs(d, exist_ok=True)
    data = {"title": title, "audios": audios, "images": imgs,
            "transcript_pdf": pdf, "answers": answers, "vocabulary": vocab}
    with open(os.path.join(d, "exercise.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    fa, fi, fp = [], [], False
    for i, a in enumerate(audios, 1):
        ext = os.path.splitext(a.split("?")[0])[1] or ".mp3"
        out = os.path.join(d, f"question_{i}_audio{ext}")
        r = get(a)
        if r:
            with open(out, "wb") as f:
                f.write(r.content)
        else:
            fa.append(a)
        time.sleep(0.2)
    for i, img in enumerate(imgs, 1):
        ext = os.path.splitext(img.split("?")[0])[1] or ".jpg"
        out = os.path.join(d, f"question_{i}{ext}")
        r = get(img)
        if r:
            with open(out, "wb") as f:
                f.write(r.content)
        else:
            fi.append(img)
        time.sleep(0.2)
    if pdf:
        name = os.path.basename(pdf)
        r = get(pdf)
        if r:
            with open(os.path.join(d, name), "wb") as f:
                f.write(r.content)
            fp = True
        time.sleep(0.2)

    lines = [f"# {title}", "", "Source: https://japanesetest4you.com", "",
             "## Answer Key"]
    for ans in answers:
        lines.append(f"- Question {ans['question']}: {ans['answer']}")
    lines.append("")
    if vocab:
        lines += ["## New Words", "| Japanese | Romaji | English |", "|---|---|---|"]
        for v in vocab:
            lines.append(f"| {v['jp']} | {v['romaji']} | {v['en']} |")
        lines.append("")
    with open(os.path.join(d, "exercise.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    return len(audios) - len(fa), fa, len(imgs) - len(fi), fi, fp


def main(urls_file, start=1, end=999):
    os.makedirs(BASE, exist_ok=True)
    with open(urls_file) as f:
        urls = [l.strip() for l in f if l.strip()]
    results = []
    for n, url in enumerate(urls, 1):
        if not (start <= n <= end):
            continue
        r = get(url)
        if not r:
            results.append({"num": n, "status": "page_failed"})
            continue
        text = r.text
        plain = re.sub(r"<[^>]+>", "\n", text)
        audios, imgs, pdf, answers, vocab = parse(text, plain)
        title_m = re.search(r"<title>(.+?)</title>", text)
        title = title_m.group(1).replace("– Japanesetest4you.com", "").strip() if title_m else ""
        prefix = "exercise" if which != "lists" else "list"
        a, fa, i, fi, p = save(n, title, audios, imgs, pdf, answers, vocab, prefix)
        results.append({"num": n, "title": title, "audios": a, "images": i,
                        "pdf": p, "fail_audio": fa, "fail_img": fi,
                        "answers": len(answers), "vocab": len(vocab)})
        print(f"ex{n}: aud={a} img={i} pdf={p} ans={len(answers)} voc={len(vocab)} failA={fa} failI={fi}")
        time.sleep(0.4)
    with open(urls_file.replace(".txt", "_results.json"), "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    which = sys.argv[1]
    start, end = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1, 999)
    main(f"/home/ubuntu/n5_listening/urls_{which}.txt", start, end)
