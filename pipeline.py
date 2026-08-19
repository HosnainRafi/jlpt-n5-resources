#!/usr/bin/env python3
"""Pipeline: parse saved webpage-extraction markdowns + download media via curl."""
import json
import os
import re
import subprocess
import sys

BASE = "/home/ubuntu/n5_listening/exercises"


def parse_markdown(md_path, expected_num):
    with open(md_path) as f:
        md = f.read()
    title_m = re.match(r"^# (.+?)\s*$", md, re.M)
    title = title_m.group(1).strip() if title_m else ""

    # images: ![](url) or ![](url "alt")
    imgs = [m.group(1) for m in re.finditer(r"!\[[^\]]*\]\((https?://japanesetest4you\.com/image/[^\s\"')]+)", md)]
    # dedupe preserving order
    seen, imgs = set(), [i for i in imgs if not (i in seen or seen.add(i))]

    # pdf link
    pdf = None
    m = re.search(r"\[View transcript\]\((https?://japanesetest4you\.com/pdf/[^\s\"')]+)", md)
    if m:
        pdf = m.group(1)

    # answer key
    answers = []
    ans_part = ""
    m = re.search(r"Answer Key\s*[:\n](.*?)(?=JLPT N5 Kanji|New words|\Z)", md, re.S | re.I)
    if m:
        ans_part = m.group(1)
        for line in ans_part.splitlines():
            mm = re.match(r"\s*Question\s+(\d+)\s*:\s*(.+)", line)
            if mm:
                answers.append({"question": int(mm.group(1)), "answer": mm.group(2).strip()})

    # vocabulary
    vocab = []
    m = re.search(r"New words\s*:?\s*\n(.*?)(?=View transcript|Learn JLPT|Grammar Audio|Vocabulary Audio|Infographics|contact me|\Z)", md, re.S | re.I)
    if m:
        block = m.group(1)
        for line in block.splitlines():
            line = line.strip().strip("*_")
            if not line or re.match(r"^New words", line, re.I):
                continue
            mm = re.match(r"^(.+?)\s*\((.+?)\)\s*:\s*(.+)$", line)
            if mm:
                vocab.append({"jp": mm.group(1).strip(), "romaji": mm.group(2).strip(), "en": mm.group(3).strip()})
            else:
                vocab.append({"jp": line, "romaji": "", "en": ""})

    return {"title": title, "images": imgs, "transcript_pdf": pdf, "answers": answers, "vocabulary": vocab}


def dl(url, outpath):
    if os.path.exists(outpath) and os.path.getsize(outpath) > 100:
        return True
    r = subprocess.run(["curl", "-s", "-L", "-f", "-o", outpath, "-A",
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", url],
                       capture_output=True)
    return r.returncode == 0


def save_files(num, data, audio_urls):
    d = os.path.join(BASE, f"exercise_{num:02d}")
    os.makedirs(d, exist_ok=True)
    data["audios"] = audio_urls
    with open(os.path.join(d, "exercise.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    ok_a, fail_a = 0, []
    for i, a in enumerate(audio_urls, 1):
        ext = os.path.splitext(a.split("?")[0])[1] or ".mp3"
        if dl(a, os.path.join(d, f"question_{i}_audio{ext}")):
            ok_a += 1
        else:
            fail_a.append(a)
    ok_i, fail_i = 0, []
    for i, img in enumerate(data["images"], 1):
        ext = os.path.splitext(img.split("?")[0])[1] or ".jpg"
        if dl(img, os.path.join(d, f"question_{i}{ext}")):
            ok_i += 1
        else:
            fail_i.append(img)
    ok_p = False
    if data["transcript_pdf"]:
        ok_p = dl(data["transcript_pdf"], os.path.join(d, os.path.basename(data["transcript_pdf"])))

    lines = [f"# {data['title']}", "", f"Source: https://japanesetest4you.com", ""]
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
    return ok_a, fail_a, ok_i, fail_i, ok_p


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "listen":
        # audio pattern: ex1-29: /choukai/0002/n5_1_{5*(n-1)+k}.mp3 ; ex30-43: /choukai/0010/listening-n5-{n}-0{k}.mp3
        def audio_url(n, q):
            if n <= 29:
                return f"https://japanesetest4you.com/choukai/0002/n5_1_{5*(n-1)+q}.mp3"
            return f"https://japanesetest4you.com/choukai/0010/listening-n5-{n}-0{q}.mp3"
        results = []
        for n in range(1, 44):
            f = f"/home/ubuntu/page_texts/japanesetest4you.com_{'japanese-language-proficiency-test-jlpt-n5-listening-exercise-'+str(n) if n<=29 else 'jlpt-n5-listening-test-'+str(n)}_.md"
            if not os.path.exists(f):
                # normalize filename may differ
                cands = [p for p in os.listdir("/home/ubuntu/page_texts") if f"listening-exercise-{n}_" in p or f"listening-test-{n}_" in p]
                if not cands:
                    print(f"!! missing markdown for ex {n}")
                    continue
                f = os.path.join("/home/ubuntu/page_texts", cands[0])
            data = parse_markdown(f, n)
            urls = [audio_url(n, q) for q in range(1, 6)]
            a, fa, i, fi, p = save_files(n, data, urls)
            results.append({"num": n, "title": data["title"], "audios": a, "images": i, "pdf": p, "fail_audio": fa, "fail_img": fi, "answers": len(data["answers"]), "vocab": len(data["vocabulary"])})
            print(f"ex{n}: audio={a} img={i} pdf={p} ans={len(data['answers'])} voc={len(data['vocabulary'])} failA={fa} failI={fi}")
        with open("/home/ubuntu/n5_listening/results.json", "w") as f:
            json.dump(results, f, indent=2)
    elif mode == "parse":
        # generic: parse a given markdown file path and url base
        f = sys.argv[2]
        data = parse_markdown(f, 0)
        print(json.dumps(data, ensure_ascii=False, indent=1)[:2000])
