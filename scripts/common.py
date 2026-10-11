"""Shared helpers for the Normattiva (Italy) LawCodex scripts."""
import os
import sys
import time

import requests

API = "https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1"
UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
DEFAULT_RAW = os.path.abspath(os.path.join(REPO, "..", "_raw", "it"))

# Normattiva "codice_tipo_provvedimento" codes that are collected (primary legislation,
# plus DPR which include the many testi unici / regolamenti with force of law).
# code -> (output directory, front-matter type)
TYPES = {
    "COS": ("costituzione", "constitution"),
    "PLC": ("leggi-costituzionali", "constitutional_law"),
    "PLE": ("leggi", "act"),
    "PLL": ("decreti-legislativi", "legislative_decree"),
    "PDL": ("decreti-legge", "decree_law"),
    "PPR": ("dpr", "presidential_decree"),
    # pre-republican acts having force of law
    "PRL": ("regi-decreti-legge", "royal_decree_law"),
    "RDL": ("regi-decreti-legislativi", "royal_legislative_decree"),
    "PLG": ("decreti-legislativi-luogotenenziali", "lieutenancy_legislative_decree"),
    "DLL": ("decreti-legge-luogotenenziali", "lieutenancy_decree_law"),
    "DCS": ("decreti-legislativi-cps", "legislative_decree"),
    "PZP": ("decreti-legislativi-presidenziali", "legislative_decree"),
    "PRD": ("regi-decreti", "royal_decree"),
}

session = requests.Session()
session.headers["User-Agent"] = UA


def request(method, url, retries=8, ok=(200,), **kw):
    delay = 5
    kw.setdefault("timeout", 600)
    for attempt in range(retries):
        try:
            r = session.request(method, url, **kw)
            if r.status_code in ok:
                return r
            print(f"HTTP {r.status_code} {method} {url}: {r.text[:300]}", file=sys.stderr)
            if r.status_code in (400, 404) and attempt >= 1:
                return r
        except requests.RequestException as e:
            print(f"error {e} for {url}", file=sys.stderr)
        time.sleep(delay)
        delay = min(delay * 2, 300)
    raise RuntimeError(f"giving up on {method} {url}")
