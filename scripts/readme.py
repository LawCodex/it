#!/usr/bin/env python3
"""Regenerate README.md (counts per directory) from the Markdown files in the repository."""
import datetime as dt
import os
import re

from common import REPO, TYPES

LABELS = {
    "costituzione": "Costituzione della Repubblica Italiana (1947)",
    "codici": "Codici (from the Normattiva \"Codici\" collection)",
    "leggi-costituzionali": "Leggi costituzionali",
    "leggi": "Leggi",
    "decreti-legislativi": "Decreti legislativi",
    "decreti-legge": "Decreti-legge (in force, not lapsed)",
    "dpr": "Decreti del Presidente della Repubblica",
    "regi-decreti-legge": "Regi decreti-legge (1861-1946)",
    "regi-decreti-legislativi": "Regi decreti legislativi",
    "decreti-legislativi-luogotenenziali": "Decreti legislativi luogotenenziali (1944-1946)",
    "decreti-legge-luogotenenziali": "Decreti-legge luogotenenziali (1915-1919, 1944-1946)",
    "decreti-legislativi-cps": "Decreti legislativi del Capo provvisorio dello Stato (1946-1948)",
    "decreti-legislativi-presidenziali": "Decreti legislativi presidenziali (1946)",
    "regi-decreti": "Regi decreti (1861-1946)",
}
ORDER = ["costituzione", "codici", "leggi-costituzionali", "leggi", "decreti-legislativi",
         "decreti-legge", "dpr", "regi-decreti-legge", "regi-decreti-legislativi",
         "decreti-legislativi-luogotenenziali", "decreti-legge-luogotenenziali",
         "decreti-legislativi-cps", "decreti-legislativi-presidenziali", "regi-decreti"]


def count(d):
    n = 0
    for root, _, files in os.walk(os.path.join(REPO, d)):
        n += sum(1 for f in files if f.endswith(".md"))
    return n


def code_list():
    out = []
    d = os.path.join(REPO, "codici")
    if not os.path.isdir(d):
        return out
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"):
            continue
        title = ""
        with open(os.path.join(d, f), encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("title: "):
                    title = line[7:].strip().strip('"').replace('\\"', '"')
                    break
        out.append(f"- [{title}](codici/{f})")
    return out


def main():
    readme = os.path.join(REPO, "README.md")
    text = open(readme, encoding="utf-8").read()
    rows = []
    total = 0
    for d in ORDER:
        n = count(d)
        if not n:
            continue
        total += n
        rows.append(f"| `{d}/` | {LABELS[d]} | {n:,} |")
    table = ("| Directory | Category | Files |\n|---|---|---:|\n" + "\n".join(rows) +
             f"\n| | **Total** | **{total:,}** |")
    text = re.sub(r"<!-- counts -->.*?<!-- /counts -->",
                  "<!-- counts -->\n" + table + "\n<!-- /counts -->", text, flags=re.S)
    text = re.sub(r"<!-- codes -->.*?<!-- /codes -->",
                  "<!-- codes -->\n" + "\n".join(code_list()) + "\n<!-- /codes -->", text,
                  flags=re.S)
    text = re.sub(r"Total: \*\*[\d,]+\*\*", f"Total: **{total:,}**", text)
    with open(readme, "w", encoding="utf-8") as f:
        f.write(text)
    print(total)


if __name__ == "__main__":
    main()
