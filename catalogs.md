# N5 URL catalogs (all verified from category pages 2026-08-19)

Base: https://japanesetest4you.com

## Listening (43) — already scraped with scrape2.py (cloudscraper)
- Ex 1-29: /japanese-language-proficiency-test-jlpt-n5-listening-exercise-N/
- Ex 30-43: /jlpt-n5-listening-test-N/
- urls in urls_listening.txt. Status: run2 (ex1-43) then run3 (ex6-43 fixed parse). Check urls_listening_results.json.

## Grammar (26)
- Ex 1-20,22-26: /japanese-language-proficiency-test-jlpt-n5-grammar-exercise-N/
- Ex 21: /japanese-language-proficiency-test-jlpt-n5-grammar-exercise-21/
- Ex 11-20 (listed page1) + 21-26 page2. NOTE ex11 URL is ...-grammar-exercise-11/ (page1 bottom).
- Grammar 2 pages: .../jlpt-n5-grammar-test/ page/1 and page/2
URLs (26):
https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-grammar-exercise-1/
...-2/ ...-3/ ...-4/ ...-5/ ...-6/ ...-7/ ...-8/ ...-9/ ...-10/ ...-11/ ...-12/ ...-13/ ...-14/ ...-15/ ...-16/ ...-17/ ...-18/ ...-19/ ...-20/ ...-21/ ...-22/ ...-23/ ...-24/ ...-25/ ...-26/

## Kanji (19)
https://japanesetest4you.com/japanese-language-proficiency-test-jlpt-n5-kanji-exercise-N/ for N=1..19

## Reading (14)
- N=1,2,3: /japanese-language-proficiency-test-jlpt-n5-reading-exercise-N/ (01/02/03 slugs use -1/-2/-3)
- N=4..11: /japanese-language-proficiency-test-jlpt-n5-reading-exercise-0N/ (04..11)
- N=12,13: /jlpt-n5-reading-12/, /jlpt-n5-reading-13/
- N=14: /japanese-language-proficiency-test-jlpt-n5-reading-exercise-14/

## Vocabulary (24)
- N=1..20: /japanese-language-proficiency-test-jlpt-n5-vocabulary-exercise-N/
- N=21..24: page 2: /japanese-language-proficiency-test-jlpt-n5-vocabulary-exercise-21/ ... -24/ (2 pages total, 20 on p1, 4 on p2)
URLs (24): above pattern for N=1..24.

## Lists pages (need extraction, URLs TBD via search):
- JLPT N5 vocabulary list, grammar list, kanji list (sidebar links on main page)

## Key technical facts
- curl/requests blocked by Cloudflare (403). cloudscraper WORKS for HTML pages.
- Media files (mp3/jpg/gif/pdf) downloadable via plain curl.
- Media URL schemes: audio <audio src="...">; images /image/... or /images/listening/....
- Parse HTML: <audio src>, <img src> for /image/|/images/; pdf: /pdf/*.pdf link; answers "Answer Key:"; vocab "New words:".
- scrape2.py handles parse+download; usage: python3 scrape2.py <name> [start end]
- Results JSON: urls_<name>_results.json
- Listening page structure notes in notes.md + plan2.md.

## Output structure per exercise: exercises/exercise_NN/{exercise.json, exercise.md, question_k_audio.mp3, question_k.ext, transcript pdf}

## LISTS (extracted 2026-08-19)
- N5 Vocabulary List page: https://japanesetest4you.com/jlpt-n5-vocabulary-list/ — contains ~350+ words as lines "jp (romaji): en" (some linked to flashcards). Saved partial markdown at /home/ubuntu/upload/japanesetest4you.com_jlpt-n5-vocabulary-list__1787168565276.md (truncated at 12k chars; full page 51k). Need cloudscraper fetch to get full page.
- N5 Grammar List page: https://japanesetest4you.com/jlpt-n5-grammar-list/ — contains grammar points "[jp] : meaning" + 2 infographic images: /wp-content/uploads/2015/06/grammar-list-n5.jpg and /wp-content/uploads/2015/06/infographic-jlpt-n5-grammar.jpg, /wp-content/uploads/2015/06/infographic-jlpt-n5-grammar-2.jpg. Also PDF: /pdf/jlpt-n5-grammar-list.pdf
- N5 kanji list: check https://japanesetest4you.com/jlpt-n5-kanji-list/ (guessed; verify)
- N5 Grammar eBook: https://japanesetest4you.com/ebook-jlpt-n5-grammar/

## Status summary
- exercises/ (listening 43): COMPLETE - all audio/img/pdf/answers/vocab (55MB)
- grammar/ (26): done via enhance.py (questions+answers+vocab)
- kanji/ (19): done
- reading/ (14): done (passages+questions+answers+vocab+images)
- vocabulary/ (24): done (all fixed, ex17 ok)
- TODO: lists (vocab/grammar/kanji), repo creation, push to GitHub
