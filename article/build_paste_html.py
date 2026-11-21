"""Builds article/medium_article_paste.html from medium_article.md.

Image paths are rewritten to absolute GitHub raw URLs so the page can be opened in a
browser, selected, copied and pasted into Medium's editor (Medium then fetches the images).

Usage (from the repo root):
    python article/build_paste_html.py [raw_base_url]
Default base URL points at the main branch of the public repo.
"""
import pathlib
import re
import sys

import markdown

ROOT = pathlib.Path(__file__).resolve().parent
BASE = (sys.argv[1] if len(sys.argv) > 1 else
        "https://raw.githubusercontent.com/pratham-rajesh/A-survey-on-agent-as-a-judge/main/article/images").rstrip("/")

md = (ROOT / "medium_article.md").read_text(encoding="utf-8")
md = re.sub(r"\]\(images/", "](" + BASE + "/", md)
body = markdown.markdown(md, extensions=["extra", "sane_lists"])
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Who Judges the Judge? A Field Guide to Agent-as-a-Judge</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{{max-width:700px;margin:2rem auto;padding:0 16px;font:18px/1.6 Georgia,serif;color:#222}}
img{{max-width:100%;height:auto}}</style></head>
<body>
{body}
</body></html>
"""
out = ROOT / "medium_article_paste.html"
out.write_text(html, encoding="utf-8")
print("wrote", out.name, "images:", html.count(BASE))
