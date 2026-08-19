# Site structure findings (japanesetest4you.com)

- Category has 43 JLPT N5 listening exercises. URLs in /home/ubuntu/n5_listening/urls.txt
- Exercises 1-29: URL pattern /japanese-language-proficiency-test-jlpt-n5-listening-exercise-N/
- Exercises 30-43: URL pattern /jlpt-n5-listening-test-N/

## Page structure per exercise
- 5 questions, each with an <audio> mp3 in https://japanesetest4you.com/choukai/0002/n5_{id}_{q}.mp3 (id is the exercise number)
  - NOTE: verify id pattern for exercises 30-43 (may use 2-digit like n5_30_1.mp3?)
- Question images: /image/*.jpg (e.g. /image/2007_04_listen_quiz1.jpg ... quiz5.jpg)
- "View transcript" link -> /pdf/n5-listening-{id}.pdf
- Answer key text: present in HTML body ("Answer Key: Question 1: 2 ...")
- "New words:" vocabulary list present in HTML body (japanese (romaji): english)
- Full content (answers + vocab) is in the HTML, visible in markdown extraction via webpage_extract
- Also has "more-{postid}" hidden span (Read More) - but content appears fully available in raw HTML

## Download plan
- Use python requests + BeautifulSoup for all 43 pages
- Parse: audio srcs (5 per page), question images, transcript pdf link, answer key, new words
- Directory structure: exercise_N/ with audio.mp3 (5), images, plus data.json / content.md
