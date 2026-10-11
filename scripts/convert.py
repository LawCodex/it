#!/usr/bin/env python3
"""Convert Normattiva JSON exports (consolidated "vigente" text) to LawCodex Markdown.

Usage: python scripts/convert.py [--raw DIR] [--out DIR] [--types PLE,...]

Reads RAW/zips/<CODE>/<year>.zip and RAW/zips/CODICI/*.zip (produced by fetch.py export),
RAW/index/*.json, RAW/abrogati.txt, RAW/dl-decaduti.txt, RAW/codici.txt and writes one
Markdown file per act in force. Acts flagged `abrogato: si`, listed in the "Atti normativi
abrogati" or "DL decaduti" collections, or whose every article is an abrogation marker,
are skipped. A manifest of written files is stored in RAW/manifest.json.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
import unicodedata
import zipfile

from common import DEFAULT_RAW, REPO, TYPES

RETRIEVED = dt.date.today().isoformat()

MESI = {"gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5, "giugno": 6,
        "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12}

# Slugs for the codes of the Normattiva "Codici" collection (keyed by codiceRedazionale).
CODE_SLUGS = {
    "042U0262": "codice-civile",
    "042U0318": "disposizioni-attuazione-codice-civile",
    "030U1398": "codice-penale",
    "040U1443": "codice-procedura-civile",
    "041U1368": "disposizioni-attuazione-codice-procedura-civile",
    "088G0492": "codice-procedura-penale",
    "089G0340": "norme-attuazione-codice-procedura-penale",
    "042U0327": "codice-navigazione",
    "092G0306": "codice-della-strada",
    "092G0531": "regolamento-codice-della-strada",
    "041U0303": "codici-penali-militari-di-pace-e-di-guerra",
    "041U1023": "disposizioni-attuazione-codici-penali-militari",
    "005G0232": "codice-del-consumo",
    "003G0218": "codice-protezione-dati-personali",
    "004G0066": "codice-beni-culturali-e-paesaggio",
    "006G0171": "codice-ambiente",
    "005G0104": "codice-amministrazione-digitale",
    "005G0055": "codice-proprieta-industriale",
    "005G0233": "codice-assicurazioni-private",
    "010G0089": "codice-ordinamento-militare",
    "010G0127": "codice-processo-amministrativo",
    "011G0201": "codice-antimafia",
    "18G00011": "codice-protezione-civile",
    "19G00007": "codice-crisi-impresa-e-insolvenza",
    "23G00044": "codice-contratti-pubblici",
    "003G0280": "codice-comunicazioni-elettroniche",
    "006G0216": "codice-pari-opportunita",
    "17G00128": "codice-terzo-settore",
    "011G0123": "codice-turismo",
    "073U0156": "codice-postale-e-telecomunicazioni",
    "052U0328": "regolamento-codice-navigazione-marittima",
    "093G0007": "codice-processo-tributario",
    "010G0226": "regolamento-codice-contratti-pubblici-2006",
    "089G0411": "regolamento-codice-procedura-penale",
    "010G0044": "regolamento-codice-proprieta-industriale",
    "005G0200": "codice-nautica-da-diporto",
    "16G00187": "codice-giustizia-contabile",
    "25G00192": "codice-incentivi",
}


def slugify(s, maxlen=70):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if len(s) > maxlen:
        s = s[:maxlen].rsplit("-", 1)[0]
    return s or "atto"


def clean_title(t):
    t = (t or "").strip()
    if t.startswith("[") and t.endswith("]"):
        t = t[1:-1]
    t = re.sub(r"\(\s*[0-9]{2,3}[A-Z][0-9A-Z]{4,6}\s*\)\s*$", "", t.strip())
    return " ".join(t.split()).strip()


def yaml_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


# ---------------------------------------------------------------- text rendering

TABLE_RE = re.compile(r"(\|.*\|)|(^\s*\+[-=+ ]{4,})|([-=_]{8,})|(^\s*\|)")
ART_RE = re.compile(r"^\s*(\(\(\s*)?(Art\.|ART\.|Articolo|ARTICOLO|Art\b)\s*[^\s]*", re.U)


def md_escape(line):
    line = line.replace("\\", "\\\\").replace("*", "\\*").replace("_", "\\_")
    line = line.replace("<", "\\<").replace("`", "\\`")
    line = re.sub(r"^(#+|>|[-+=]\s|[-+=]$)", lambda m: "\\" + m.group(1), line)
    line = re.sub(r"^(\d+)([.)])(\s|$)", r"\1\\\2\3", line)
    line = re.sub(r"^\[", r"\\[", line)
    return line


def render_lines(text):
    """Plain Normattiva text (lines separated by \\n) -> list of Markdown blocks."""
    if not text:
        return []
    raw = text.replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ").split("\n")
    blocks = []
    i = 0
    n = len(raw)
    while i < n:
        line = raw[i]
        if TABLE_RE.search(line):
            j = i
            buf = []
            # take a run of table-ish lines (allowing single non-table lines inside the box)
            while j < n and (TABLE_RE.search(raw[j]) or
                             (raw[j].strip() and j + 1 < n and TABLE_RE.search(raw[j + 1])
                              and buf)):
                buf.append(raw[j].rstrip())
                j += 1
            if len(buf) >= 2 or "|" in line:
                fence = "```"
                while fence in "\n".join(buf):
                    fence += "`"
                blocks.append(fence + "text\n" + "\n".join(buf) + "\n" + fence)
                i = j
                continue
        s = " ".join(line.split())
        if s:
            blocks.append(md_escape(s))
        i += 1
    return blocks


def split_article(text):
    """Return (preamble_text, label, rubric, body_text) from an article's text."""
    lines = (text or "").replace("\r", "").split("\n")
    idx = None
    for k, l in enumerate(lines[:80]):
        if ART_RE.match(l) and len(l.strip()) < 40:
            idx = k
            break
    if idx is None:
        return "", None, None, text
    label = " ".join(lines[idx].split()).rstrip(".").strip()
    if label.startswith("((") and not label.endswith("))"):
        return "", None, None, text
    pre = "\n".join(lines[:idx])
    rest = lines[idx + 1:]
    rubric = None
    k = 0
    while k < len(rest) and not rest[k].strip():
        k += 1
    if k < len(rest):
        r = " ".join(rest[k].split())
        if (r.startswith("(") and not r.startswith("((") and
                (r.endswith(")") or r.endswith(").")) and r.count("(") == r.count(")")):
            rubric = r.rstrip(".")
            if rubric.startswith("(") and rubric.endswith(")"):
                rubric = rubric[1:-1].strip()
            rest = rest[k + 1:]
    return pre, label, rubric, "\n".join(rest)


DIV_KINDS = [("PARTE", 0), ("LIBRO", 1), ("TITOLO", 2), ("CAPO", 3), ("CAPITOLO", 3),
             ("SEZIONE", 4), ("SOTTOSEZIONE", 5), ("PARAGRAFO", 6), ("§", 6)]
DIV_RE = re.compile(r"^[(\s]*(PARTE|LIBRO|TITOLO|CAPO|CAPITOLO|SEZIONE|SOTTOSEZIONE|PARAGRAFO|§)"
                    r"(?=$|[\s\-.,:;)IVXLCDM0-9])", re.I)
NUM_RE = re.compile(r"^[(\s]*([IVXLCDM]+|\d+|[A-Z])([\s.\-]*(BIS|TER|QUATER|QUINQUIES|SEXIES)?)"
                    r"[)\s.]*$", re.I)


def div_kind(seg):
    if len(seg) > 60:
        return None
    m = DIV_RE.match(seg)
    if not m:
        return None
    return dict(DIV_KINDS)[m.group(1).upper()]


def group_headings(numnir):
    """Normattiva group label -> [(division rank or None, heading text)].

    The label lists the divisions that start at this point, '*'-separated, e.g.
    '-*-*LIBRO PRIMO*DELLE PERSONE E DELLA FAMIGLIA*TITOLO I*DELLE PERSONE FISICHE*' or
    'Capo III**Gestione della prevenzione**Sezione*I**MISURE DI TUTELA**' ('-' = unchanged).
    Each division keyword (Parte, Libro, Titolo, Capo, Sezione, §) starts a heading, the
    following segments are its title; segments before any keyword are a standalone heading."""
    if not numnir:
        return []
    segs = [" ".join(p.split()) for p in numnir.replace("\n", " ").split("*")]
    segs = [p for p in segs if p and p != "-"]
    out = []  # [kind, label, [titles]]
    for seg in segs:
        k = div_kind(seg)
        if k is not None:
            out.append([k, seg, []])
        elif out and out[-1][0] is not None and not out[-1][2] and NUM_RE.match(seg) \
                and not NUM_RE.match(out[-1][1].split()[-1] if len(out[-1][1].split()) > 1 else ""):
            out[-1][1] += " " + seg            # 'Sezione' + 'I'
        elif out:
            out[-1][2].append(seg)
        else:
            out.append([None, seg, []])
    res = []
    for k, label, titles in out:
        txt = label
        if titles:
            txt += " - " + " ".join(titles)
        res.append((k, txt))
    return res


class Renderer:
    def __init__(self):
        self.out = []

    def heading(self, level, text):
        text = md_escape(" ".join(text.split())).replace("\\#", "#")
        if level <= 6:
            self.out.append("#" * level + " " + text)
        else:
            self.out.append("**" + text + "**")

    def para(self, blocks):
        self.out.extend(blocks)


def collect_positions(elems, acc):
    for x in elems or []:
        if x.get("nomeNir") not in ("articolo", "allegato") and x.get("numNir"):
            for p, _ in group_headings(x["numNir"]):
                if p is not None:
                    acc.add(p)
        collect_positions(x.get("elementi"), acc)


def first_leaf(elems):
    for x in elems or []:
        if x.get("nomeNir") in ("articolo", "allegato") or (x.get("testo") and not x.get("elementi")):
            return x
        y = first_leaf(x.get("elementi"))
        if y is not None:
            return y
    return None


def render_elements(r, elems, rank, art_level, first):
    for x in elems or []:
        kind = x.get("nomeNir")
        if kind in ("articolo", "allegato") or (x.get("testo") and not x.get("elementi")):
            pre, label, rubric, body = split_article(x.get("testo") or "")
            if x.get("_pre_done"):
                pre = ""
            if label is None:
                num = (x.get("numNir") or "").strip()
                if kind == "allegato" and num:
                    label = num.split("-", 1)[-1].strip() if "-" in num else num
                elif num:
                    label = ("Art. " + num) if kind == "articolo" else num
                else:
                    label = "Allegato" if kind == "allegato" else "Articolo"
                rubric = None
            if pre.strip():
                r.para(render_lines(pre))
            r.heading(art_level, label + (" - " + rubric if rubric else ""))
            r.para(render_lines(body))
            note = (x.get("noteArt") or "").strip()
            if note:
                r.para(["> " + b.replace("\n", "\n> ") for b in render_lines(note)])
            if x.get("elementi"):
                render_elements(r, x["elementi"], rank, art_level, False)
        else:
            for p, txt in group_headings(x.get("numNir")):
                lvl = 2 + (rank[p] if p is not None else 0)
                if lvl >= art_level and art_level == 6:
                    lvl = 7  # rendered in bold, articles stay the deepest heading level
                r.heading(lvl, txt)
            render_elements(r, x.get("elementi"), rank, art_level, False)


def all_abrogated(d):
    """True when every article/annex text is only an abrogation/soppression marker."""
    texts = []

    def walk(elems):
        for x in elems or []:
            if x.get("testo"):
                pre, label, rubric, body = split_article(x["testo"])
                texts.append(" ".join(body.split()))
            walk(x.get("elementi"))
    walk((d.get("articolato") or {}).get("elementi"))
    if not texts:
        return False
    pat = re.compile(r"^(\(\((.*?)(ABROGAT|SOPPRESS|CONFERMATO L'ABROGAZIONE)(.*?)\)\)\.?\s*)+$",
                     re.S)
    return all(pat.match(t) for t in texts if t) and any(texts)


def render_doc(d):
    md = d.get("metadati") or {}
    head = d.get("intestazione") or {}
    r = Renderer()
    art = (d.get("articolato") or {}).get("elementi") or []
    ann = (d.get("annessi") or {}).get("elementi") or []
    pos = set()
    collect_positions(art, pos)
    collect_positions(ann, pos)
    rank = {p: i for i, p in enumerate(sorted(pos))}
    art_level = min(2 + len(rank), 6)
    note = (md.get("noteDoc") or "").strip()
    if note:
        r.para(["*" + b + "*" for b in render_lines(note)])
    # the preamble (enacting formula) is part of the first article's text: put it before
    # the first structural heading
    fl = first_leaf(art)
    if fl is not None:
        pre = split_article(fl.get("testo") or "")[0]
        if pre.strip():
            r.para(render_lines(pre))
            fl["_pre_done"] = True
    render_elements(r, art, rank, art_level, True)
    if ann:
        if not group_headings(ann[0].get("numNir")):
            r.heading(2, "Allegati")
        render_elements(r, ann, rank, art_level, False)
    return "\n\n".join(r.out).strip() + "\n"


# ---------------------------------------------------------------- driver

def doc_date(d):
    md = d.get("metadati") or {}
    s = md.get("dataDoc") or ""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s) and not s.startswith("0000"):
        return s
    return None


def heading_title(d, code):
    md = d.get("metadati") or {}
    head = d.get("intestazione") or {}
    if code == "COS":
        return "Costituzione della Repubblica Italiana"
    tipo = (head.get("tipoDoc") or md.get("tipoDoc") or "").strip()
    data = ((head.get("dataDoc") or {}).get("testo") or "").strip()
    num = (head.get("numDoc") or md.get("numDoc") or "").strip()
    s = tipo
    if data:
        s += " " + data
    if num and num != "0":
        s += ", n. " + num
    return s


def last_amended(md):
    m = re.search(r"/CONSOLIDATED/(\d{4})(\d{2})(\d{2})", md.get("eli") or "")
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


def front_matter(d, code, key, ftype):
    md = d.get("metadati") or {}
    title = clean_title(md.get("titoloDoc") or (d.get("intestazione") or {}).get("titoloDoc"))
    htitle = heading_title(d, code)
    urn = md.get("urn") or ""
    fm = ["---"]
    fm.append("title: " + yaml_str(htitle + (" — " + title if title and code != "COS" else "")))
    fm.append("identifier: " + yaml_str(urn or key))
    if md.get("eli"):
        fm.append("eli: " + yaml_str("https://www.normattiva.it/" + md["eli"]))
    fm.append("type: " + ftype)
    fm.append("jurisdiction: it")
    fm.append("language: it")
    date = doc_date(d)
    if code == "COS":
        date = "1947-12-27"
    if date:
        fm.append("date: " + date)
    la = last_amended(md)
    if la:
        fm.append("last_amended: " + la)
    fm.append("status: in_force")
    if md.get("dataPubblicazione"):
        gu = f"Gazzetta Ufficiale n. {md.get('numeroPubblicazione')} del {md['dataPubblicazione']}"
        fm.append("gazzetta_ufficiale: " + yaml_str(gu))
    fm.append("codice_redazionale: " + yaml_str(md.get("redazione") or key.split("_", 1)[1]))
    src = ("https://www.normattiva.it/uri-res/N2Ls?" + urn) if urn else "https://www.normattiva.it/"
    fm.append("source: " + yaml_str(src))
    fm.append("retrieved: " + RETRIEVED)
    fm.append("---")
    return "\n".join(fm), htitle, title


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=DEFAULT_RAW)
    ap.add_argument("--out", default=REPO)
    ap.add_argument("--types", default=",".join(list(TYPES) + ["CODICI"]))
    a = ap.parse_args()

    def readset(name):
        p = os.path.join(a.raw, name)
        return set(open(p).read().split()) if os.path.exists(p) else set()
    abrogati = readset("abrogati.txt")
    decaduti = readset("dl-decaduti.txt")
    codici = {k.split("_", 1)[1]: k for k in readset("codici.txt")}

    big_years = {}
    for p in glob.glob(os.path.join(a.raw, "index", "*.classes.json")):
        code = os.path.basename(p).split(".")[0]
        yc = {}
        for cl, years in json.load(open(p)).items():
            for y, n in years.items():
                yc[y] = yc.get(y, 0) + n
        big_years[code] = yc

    man_path = os.path.join(a.raw, "manifest.json")
    manifest = json.load(open(man_path)) if os.path.exists(man_path) else {}
    stats = {}
    done_keys = set()
    for code in [t for t in a.types.split(",") if t]:
        zips = sorted(glob.glob(os.path.join(a.raw, "zips", code, "*.zip")))
        for zp in zips:
            try:
                z = zipfile.ZipFile(zp)
            except zipfile.BadZipFile:
                print(f"bad zip {zp}", file=sys.stderr)
                continue
            for name in z.namelist():
                if not name.endswith(".json"):
                    continue
                d = json.loads(z.read(name))
                md = d.get("metadati") or {}
                key = f"{md.get('dataPubblicazione')}_{md.get('redazione')}"
                if key in done_keys:
                    continue
                done_keys.add(key)
                tcode = code
                if code == "CODICI":
                    tcode = "CODICI"
                st = stats.setdefault(tcode, {"in_force": 0, "abrogated": 0, "decaduti": 0})
                if (md.get("abrogato") or "").lower() in ("si", "sì", "s", "true") \
                        or key in abrogati:
                    st["abrogated"] += 1
                    continue
                if key in decaduti:
                    st["decaduti"] += 1
                    continue
                if all_abrogated(d):
                    st["abrogated"] += 1
                    continue
                red = md.get("redazione") or ""
                is_code = red in codici and codici[red] == key
                if code == "CODICI" and not is_code:
                    continue
                if code == "COS":
                    rel = "costituzione/costituzione.md"
                    ftype = "constitution"
                elif is_code:
                    slug = CODE_SLUGS.get(red) or slugify(clean_title(md.get("titoloDoc")), 60)
                    rel = f"codici/{slug}.md"
                    ftype = "code"
                else:
                    tdir, ftype = TYPES[code]
                    date = doc_date(d) or md.get("dataPubblicazione") or "0000-00-00"
                    year = date[:4]
                    num = slugify(str(md.get("numDoc") or "0"), 20)
                    slug = slugify(clean_title(md.get("titoloDoc")), 60)
                    sub = year
                    ny = big_years.get(code, {}).get(year, 0)
                    if ny > 3000:
                        sub = f"{year}/{date[5:10]}"   # one directory per day
                    elif ny > 900:
                        sub = f"{year}/{date[5:7]}"    # one directory per month
                    rel = f"{tdir}/{sub}/{date}-n-{num}-{slug}.md"
                fm, htitle, title = front_matter(d, code, key, ftype)
                body = render_doc(d)
                h1 = "# " + htitle
                parts = [fm, "", h1, ""]
                if title and code != "COS":
                    parts += ["**" + md_escape(title) + "**", ""]
                text = "\n".join(parts) + "\n" + body
                # avoid collisions between distinct acts
                prev = manifest.get(rel)
                if prev and prev != key:
                    base = rel[:-3]
                    rel = f"{base}-{red.lower()}.md"
                manifest[rel] = key
                path = os.path.join(a.out, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                st["in_force"] += 1
        print(code, stats.get(code), file=sys.stderr)
    with open(man_path, "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=0)
    with open(os.path.join(a.raw, "stats.json"), "w") as f:
        json.dump(stats, f, indent=1)


if __name__ == "__main__":
    main()
