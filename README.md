# Khushi's Scrapbook
Static site. Host with GitHub Pages (Settings > Pages > Deploy from branch > main / root).
- `explore.py` parses `_chat.txt`, then `analyze.py` writes `data.js` (all numbers come from the chat only). Re-run: `python3 explore.py && python3 analyze.py`
- `cute.py` (run after `explore.py`) writes `cute.js`: real quotes and little facts shown under each page's charts. Every quote is looked up in the chat.
- `diary.py` (run after `explore.py`) writes `diary.json`: every day of the chat for the in-site diary and "On this day".
- `index.html` unlocks one page per day at 12:00 am IST (4 Oct to 26 Oct 2026), birthday page on 27 Oct.
- Preview any day: `index.html?day=2026-10-15`
- Edit `MILESTONES`, `LETTER` and page texts at the top of `index.html`.
