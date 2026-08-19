#!/usr/bin/env python3
"""Diagnose failed pages: check what the fetched HTML contains."""
import re
import sys

import cloudscraper

session = cloudscraper.create_scraper()

for num in sys.argv[1:]:
    num = int(num)
    if num <= 29:
        url = f"https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-listening-exercise-{num}/"
    else:
        url = f"https://japanesetest4you.com/jlpt-n5-listening-test-{num}/"
    r = session.get(url, timeout=30)
    html = r.text
    imgs = re.findall(r"https://japanesetest4you\.com/image/[^\s\"')]+", html)
    audios = re.findall(r"https://japanesetest4you\.com/choukai/[^\s\"']+", html)
    print(f"ex{num}: status={r.status_code} len={len(html)} imgs={len(imgs)} audios={len(audios)}")
    print("  imgs:", imgs[:3] if imgs else None)
    print("  audios:", audios[:3] if audios else None)
    if "choukai" not in html and "/image/" not in html:
        # maybe iframe or other container
        iframes = re.findall(r'<iframe[^>]+src="([^"]+)"', html)
        print("  iframes:", iframes[:3])
        # check for audio tags without src (data attribute)
        data_attrs = re.findall(r'data-[a-z]+="[^"]*"', html)
        sample = [d for d in data_attrs if "mp3" in d or "image" in d][:5]
        print("  data attrs with media:", sample)
