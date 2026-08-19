#!/usr/bin/env python3
"""Enhanced extraction for grammar/kanji/reading/vocabulary exercises:
- full question text with options (1-4)
- answer key with explanations
- vocabulary
Uses cloudscraper + BeautifulSoup."""
import json
import os
import re
import sys
import time

import cloudscraper
from bs4 import BeautifulSoup

CATS = {
    "grammar": 26,
    "kanji": 19,
    "reading": 14,
    "vocabulary": 24,
}


def url_of(cat, n):
    if cat == "grammar":
        return f"https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-grammar-exercise-{n}/"
    if cat == "kanji":
        return f"https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-kanji-exercise-{n}/"
    if cat == "reading":
        if n in (1, 2, 3):
            return f"https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-reading-exercise-{n}/"
        if n in (12, 13):
            return f"https://japanesetest4you.com/jlpt-n5-reading-{n}/"
        if n == 4:
            return f"https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-reading-exercise-0{n}/"
        if n <= 11:
            return f"https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-reading-exercise-{n:02d}/"
        return f"https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-reading-exercise-{n}/"
    return f"https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-vocabulary-exercise-{n}/"


session = cloudscraper.create_scraper()


def get(url):
    for _ in range(3):
        try:
            r = session.get(url, timeout=30)
            if r.status_code == 200:
                return r
        except Exception:
            time.sleep(3)
    return None


def extract(entry):
    """Parse entry element: questions (numbered paras), answers, vocab."""
    questions = []
    answers = []
    vocab = []
    text = entry.get_text("\n")

    # questions: paragraphs matching '^\d+\.' then following option paragraphs
    for p in entry.find_all("p"):
        t = p.get_text(" ", strip=True)
        m = re.match(r"^(\d+)\.\s+(.+)$", t)
        if m:
            num = int(m.group(1))
            # collect option lines: siblings until next numbered q or answer key
            opts = []
            sib = p.find_next_sibling()
            while sib is not None:
                if sib.name == "p":
                    st = sib.get_text(" ", strip=True)
                    if re.match(r"^\d+\.", st):
                        break
                    if re.match(r"^(Answer|Answer Key|\*\*Answer|\[Read)", st, re.I):
                        break
                    if re.match(r"^Read more", st, re.I):
                        break
                    opts.append(st)
                elif sib.name in ("h2", "h3", "strong", "hr"):
                    break
                sib = sib.find_next_sibling()
            # radio options within question para itself
            radios = p.find_all("input", {"type": "radio"})
            if radios:
                for rb in radios:
                    label = rb.find_next_sibling(string=True) or ""
                    opts = [str(o) for o in p.strings] if not opts else opts
            questions.append({"question": num, "text": m.group(2).strip(), "options": opts})

    # reading style: question paragraphs like "「１」には、なにをいれますか。"
    # followed by sibling option paragraphs, and passages introduced by 'Reading Passage N'
    if not questions and re.search(r"Reading Passage", text, re.I):
        num = 0
        for p in entry.find_all("p"):
            t = p.get_text(" ", strip=True)
            if re.match(r"^Reading Passage", t, re.I):
                continue
            if re.search(r"しつもん", t) or (re.search(r"[「\"']\d+[」\"']", t) and re.search(r"(なに|何|どれ|いくつ|だれ|どこ|どう|いつ|なぜ|え)", t)):
                num += 1
                opts = []
                sib = p.find_next_sibling()
                while sib is not None:
                    if sib.name == "p":
                        st = sib.get_text(" ", strip=True)
                        if re.match(r"^\d+\.", st) or re.match(r"^Reading Passage", st, re.I):
                            break
                        if re.match(r"^(Answer|Answer Key|\*\*Answer)", st, re.I):
                            break
                        if re.search(r"[「\"']\d+[」\"']", st) and re.search(r"(しつもん|なに|何|どれ)", st):
                            break
                        if st and st not in ("１", "２", "３", "４", "1", "2", "3", "4"):
                            opts.append(st)
                        else:
                            opts.append(st)
                    elif sib.name in ("h2", "h3", "hr"):
                        break
                    sib = sib.find_next_sibling()
                questions.append({"question": num, "text": t, "options": opts})

    # answer key with explanations
    m = re.search(r"Answer key:?(?:\n|\s*)(.*)", text, re.S | re.I)
    if m:
        block = m.group(1)
        for line in block.split("\n"):
            line = line.strip()
            mm = re.match(r"Question\s+(\d+)\s*:\s*(.+)", line)
            if mm:
                ans = mm.group(2).strip()
                # split answer number from explanation
                am = re.match(r"^(\d+)\s*(\(.*\))?\s*$", ans)
                expl = ""
                if am:
                    expl = am.group(2) or ""
                    ans_num = am.group(1)
                else:
                    ans_num = ans.split()[0] if ans else ""
                    expl = ans
                answers.append({"question": int(mm.group(1)), "answer": ans_num,
                                "explanation": expl.strip("()") if expl else ""})

    # vocabulary
    m = re.search(r"New words:?\n(.*)", text, re.S)
    if m:
        block = m.group(1)
        for line in block.split("\n"):
            line = line.strip().strip("*_")
            if not line or re.match(r"^New words", line, re.I) or line.startswith("http"):
                continue
            if "View transcript" in line or "Learn JLPT" in line:
                break
            mm = re.match(r"^(.+?)\s*\((.+?)\)\s*:\s*(.+)$", line)
            if mm:
                vocab.append({"jp": mm.group(1).strip(), "romaji": mm.group(2).strip(), "en": mm.group(3).strip()})
            else:
                vocab.append({"jp": line, "romaji": "", "en": ""})
    return questions, answers, vocab


def clean(text):
    return re.sub(r"\s+", " ", text).strip()


def main():
    cat = sys.argv[1]
    n_pages = CATS[cat]
    base = f"/home/ubuntu/n5_listening/{cat}"
    os.makedirs(base, exist_ok=True)
    results = []
    for n in range(1, n_pages + 1):
        d = os.path.join(base, f"exercise_{n:02d}")
        os.makedirs(d, exist_ok=True)
        r = get(url_of(cat, n))
        if not r:
            results.append({"num": n, "status": "page_failed"})
            print(f"{cat} ex{n}: page failed")
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        entry = soup.find(class_="entry-content") or soup.find(class_="entry")
        if not entry:
            results.append({"num": n, "status": "no_entry"})
            print(f"{cat} ex{n}: no entry")
            continue
        title_el = soup.find("title")
        title = clean(title_el.get_text()) if title_el else ""
        title = re.sub(r"\s*–\s*Japanesetest4you\.com", "", title)

        questions, answers, vocab = extract(entry)

        # images present on page (e.g. reading)
        imgs = list(dict.fromkeys(
            img.get("src") for img in entry.find_all("img")
            if img.get("src") and ("/image/" in img["src"] or "/images/" in img["src"])
        ))
        for i, img in enumerate(imgs, 1):
            out = os.path.join(d, f"reading_image_{i}{os.path.splitext(img.split('?')[0])[1] or '.jpg'}")
            if not os.path.exists(out):
                r2 = get(img)
                if r2:
                    open(out, "wb").write(r2.content)
                time.sleep(0.15)

        data = {"title": title, "questions": questions, "answers": answers,
                "vocabulary": vocab, "images": imgs}
        with open(os.path.join(d, "exercise.json"), "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        lines = [f"# {title}", "", "Source: https://japanesetest4you.com", "",
                 "## Questions"]
        for q in questions:
            lines.append(f"### Question {q['question']}")
            lines.append(q["text"])
            for o in q["options"]:
                lines.append(f"- {o}")
            lines.append("")
        lines.append("## Answer Key")
        for a in answers:
            line = f"- Question {a['question']}: {a['answer']}"
            if a.get("explanation"):
                line += f" ({a['explanation']})"
            lines.append(line)
        lines.append("")
        if vocab:
            lines += ["## New Words", "| Japanese | Romaji | English |", "|---|---|---|"]
            for v in vocab:
                lines.append(f"| {v['jp']} | {v['romaji']} | {v['en']} |")
            lines.append("")
        with open(os.path.join(d, "exercise.md"), "w") as f:
            f.write("\n".join(lines) + "\n")
        results.append({"num": n, "title": title, "questions": len(questions),
                        "answers": len(answers), "vocab": len(vocab), "images": len(imgs)})
        print(f"{cat} ex{n}: q={len(questions)} ans={len(answers)} voc={len(vocab)} img={len(imgs)}")
        time.sleep(0.2)
    with open(f"/home/ubuntu/n5_listening/urls_{cat}_results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
