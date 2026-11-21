#!/usr/bin/env bash
# Exports slides/agent_as_a_judge.pptx to slides/agent_as_a_judge.pdf using Microsoft PowerPoint (macOS),
# then sets the PDF metadata (title, author) from the PRESENTER value in build_deck.py.
# No PowerPoint? Open the .pptx in Keynote, PowerPoint or LibreOffice and use File > Export as PDF.
# Run from the repo root:  bash slides/export_pdf.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PPTX="$ROOT/slides/agent_as_a_judge.pptx"
PDF="$ROOT/slides/agent_as_a_judge.pdf"
rm -f "$PDF"
osascript <<EOF
tell application "Microsoft PowerPoint"
  open POSIX file "$PPTX"
  set p to active presentation
  save p in POSIX file "$PDF" as save as PDF
  close p saving no
end tell
EOF
"$ROOT/.venv/bin/python" - <<EOF
import re
from pypdf import PdfReader, PdfWriter
src = open("$ROOT/slides/build_deck.py").read()
presenter = re.search(r'^PRESENTER = "(.*)"', src, re.M).group(1)
r = PdfReader("$PDF")
w = PdfWriter()
for page in r.pages:
    w.add_page(page)
w.add_metadata({"/Title": "A Survey on Agent-as-a-Judge", "/Author": presenter, "/Producer": presenter, "/Creator": presenter})
with open("$PDF", "wb") as f:
    w.write(f)
print("wrote slides/agent_as_a_judge.pdf, pages:", len(r.pages), "author:", presenter)
EOF
