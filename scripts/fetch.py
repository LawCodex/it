#!/usr/bin/env python3
"""Download Italian state legislation from the Normattiva open-data API.

Usage:
  python scripts/fetch.py index    [--types PLE,PLL,...]   # list every act (sync search API)
  python scripts/fetch.py lists                            # abrogated acts + codes collections
  python scripts/fetch.py export   [--types ...] [--workers 3]
                                                           # consolidated (vigente) JSON exports

API: https://dati.normattiva.it (bff-opendata, documented in
https://dati.normattiva.it/assets/come_fare_per/API_Normattiva_OpenData.pdf).

- `index` uses POST /ricerca/avanzata filtered by act type (codice_tipo_provvedimento) and
  year, 1000 results per page, and writes RAW/index/<CODE>.json.
- `lists` downloads the pre-built collections "Atti normativi abrogati (in originale)" and
  "Codici" in URI format (one ELI per act, named <dataGU>_<codiceRedazionale>) and writes
  RAW/abrogati.txt and RAW/codici.txt.
- `export` runs one asynchronous export per (type, year, classeProvvedimento) for classes
  1 ("atto normativo - senza aggiornamenti") and 2 ("atto normativo - aggiornato"), i.e.
  skipping class 3 ("abrogato"), with richiestaExport=V (text in force on --vigenza, default
  today) and formato=JSON, and downloads the zip to RAW/zips/<CODE>/<year>-c<class>.zip.
  The codes of the "Codici" collection whose act type is not exported are fetched one by one
  into RAW/zips/CODICI/. Existing zips are reused (delete them to refresh).
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import io
import json
import os
import re
import sys
import time
import zipfile

from common import API, DEFAULT_RAW, TYPES, request


def search(body):
    r = request("POST", f"{API}/ricerca/avanzata", json=body)
    return r.json()


def index_type(raw, code):
    out = os.path.join(raw, "index", f"{code}.json")
    if os.path.exists(out):
        return json.load(open(out))
    base = {"filtriMap": {"codice_tipo_provvedimento": code},
            "paginazione": {"paginaCorrente": 1, "numeroElementiPerPagina": 1}}
    d = search(base)
    years = sorted(f["codice"] for f in d["facetMap"]["anno_provvedimento"])
    total = d["numeroAttiTrovati"]
    acts = []
    for y in years:
        page = 1
        while True:
            body = {"annoProvvedimento": y,
                    "filtriMap": {"codice_tipo_provvedimento": code, "anno_provvedimento": y},
                    "paginazione": {"paginaCorrente": page, "numeroElementiPerPagina": 1000}}
            d = search(body)
            lst = d.get("listaAtti") or []
            acts.extend(lst)
            if page >= (d.get("numeroPagine") or 1) or not lst:
                break
            page += 1
        print(f"index {code} {y}: {len(acts)}/{total}", file=sys.stderr)
    seen = {}
    for a in acts:
        seen[(a["dataGU"], a["codiceRedazionale"])] = a
    acts = list(seen.values())
    if len(acts) != total:
        print(f"WARNING {code}: indexed {len(acts)} but search reports {total}", file=sys.stderr)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out + ".tmp", "w", encoding="utf-8") as f:
        json.dump(acts, f, ensure_ascii=False)
    os.replace(out + ".tmp", out)
    return acts


def download_collection(raw, nome, fmt, kind, dest):
    if os.path.exists(dest):
        return dest
    r = request("GET", f"{API}/collections/download/collection-preconfezionata",
                params={"nome": nome, "formato": fmt, "formatoRichiesta": kind},
                timeout=3600)
    data = r.content
    try:
        zipfile.ZipFile(io.BytesIO(data)).testzip()
    except zipfile.BadZipFile:
        print(f"WARNING: {nome} zip is truncated ({len(data)} bytes); using local headers",
              file=sys.stderr)
    with open(dest + ".tmp", "wb") as f:
        f.write(data)
    os.replace(dest + ".tmp", dest)
    return dest


NAME_RE = re.compile(r"/(\d{4}-\d{2}-\d{2})_([0-9A-Z]+)_")


def collection_keys(path):
    """Act keys (<dataGU>_<codiceRedazionale>) in a collection zip.

    Large collection downloads are sometimes cut off before the zip central directory, so
    the entry names are read from the local file headers instead."""
    import struct
    data = open(path, "rb").read()
    keys = set()
    for m in re.finditer(rb"PK\x03\x04", data):
        j = m.start()
        fl, el = struct.unpack("<HH", data[j + 26:j + 30])
        name = data[j + 30:j + 30 + fl].decode("utf-8", "replace")
        mm = NAME_RE.search(name)
        if mm:
            keys.add(f"{mm.group(1)}_{mm.group(2)}")
    return sorted(keys)


def cmd_lists(raw):
    os.makedirs(os.path.join(raw, "collections"), exist_ok=True)
    for nome, fn in (("Atti normativi abrogati (in originale)", "abrogati"),
                     ("DL decaduti", "dl-decaduti"),
                     ("Codici", "codici")):
        z = download_collection(raw, nome, "URI", "O",
                                os.path.join(raw, "collections", f"{fn}-uri.zip"))
        keys = collection_keys(z)
        with open(os.path.join(raw, f"{fn}.txt"), "w") as f:
            f.write("\n".join(keys) + "\n")
        print(f"{fn}: {len(keys)}", file=sys.stderr)


def run_export(code, year, n_expected, dest, number, cls, vigenza):
    body = {"formato": "JSON", "tipoRicerca": "A", "modalita": "C", "richiestaExport": "V",
            "dataVigenza": vigenza,
            "parametriRicerca": {"annoProvvedimento": int(year),
                                 "filtriMap": {"codice_tipo_provvedimento": code,
                                               "anno_provvedimento": str(year)}}}
    if number:
        body["parametriRicerca"]["numeroProvvedimento"] = int(number)
    if cls:
        body["parametriRicerca"]["classeProvvedimento"] = cls
    for attempt in range(6):
        r = request("POST", f"{API}/ricerca-asincrona/nuova-ricerca", json=body, ok=(200, 202))
        token = r.text.strip().strip('"')
        r = request("PUT", f"{API}/ricerca-asincrona/conferma-ricerca", json={"token": token},
                    ok=(200, 202, 204, 503))
        st = r.json() if r.content else {}
        if st.get("stato") == 5 or r.status_code == 503:
            print(f"export {code} {year}: server overloaded, waiting", file=sys.stderr)
            time.sleep(120 * (attempt + 1))
            continue
        loc = None
        t0 = time.time()
        while time.time() - t0 < 6 * 3600:
            time.sleep(10)
            r = request("GET", f"{API}/ricerca-asincrona/check-status/{token}",
                        ok=(200, 303), allow_redirects=False)
            if r.status_code == 303:
                loc = r.headers.get("x-ipzs-location")
                break
            st = r.json()
            if st.get("stato") in (4, 5):
                print(f"export {code} {year}: stato {st}", file=sys.stderr)
                break
        if not loc:
            time.sleep(60)
            continue
        for dl in range(5):
            r = request("GET", loc, timeout=7200)
            try:
                z = zipfile.ZipFile(io.BytesIO(r.content))
                bad = z.testzip()
                if bad is None:
                    break
            except zipfile.BadZipFile:
                pass
            print(f"export {code} {year}: bad zip, retrying download", file=sys.stderr)
            time.sleep(30)
        else:
            continue
        n = sum(1 for i in z.namelist() if i.endswith(".xml"))
        with open(dest + ".tmp", "wb") as f:
            f.write(r.content)
        os.replace(dest + ".tmp", dest)
        print(f"export {code} {year} c{cls}: {n}/{n_expected} acts, {len(r.content)//1024} KiB",
              file=sys.stderr)
        return n
    raise RuntimeError(f"export {code} {year} failed")


TIPO_CODE = {"REGIO DECRETO": "PRD", "DECRETO LEGISLATIVO": "PLL", "DECRETO": "DCT",
             "DECRETO DEL PRESIDENTE DELLA REPUBBLICA": "PPR", "LEGGE": "PLE"}


def codici_jobs(raw, types):
    """One export per code of the "Codici" collection whose act type is not exported anyway."""
    jobs = []
    z = os.path.join(raw, "collections", "codici-uri.zip")
    d = os.path.join(raw, "zips", "CODICI")
    os.makedirs(d, exist_ok=True)
    import struct
    data = open(z, "rb").read()
    for m in re.finditer(rb"PK\x03\x04", data):
        j = m.start()
        fl, = struct.unpack("<H", data[j + 26:j + 28])
        name = data[j + 30:j + 30 + fl].decode("utf-8", "replace")
        mm = re.match(r"(.+)_(\d{4})(\d{4})_(\w+)/(\d{4}-\d{2}-\d{2})_([0-9A-Z]+)_", name)
        if not mm:
            continue
        code = TIPO_CODE.get(mm.group(1))
        if code is None or code in types:
            continue
        dest = os.path.join(d, f"{mm.group(5)}_{mm.group(6)}.zip")
        if not os.path.exists(dest):
            jobs.append((code, mm.group(2), 1, dest, mm.group(4), None))
    return jobs


def class_year_counts(raw, code):
    """{class: {year: n}} for classeProvvedimento 1 (never amended) and 2 (amended), i.e.
    the acts not marked as abrogated (class 3)."""
    out = os.path.join(raw, "index", f"{code}.classes.json")
    if os.path.exists(out):
        return json.load(open(out))
    res = {}
    for cl in ("1", "2"):
        d = search({"classeProvvedimento": cl,
                    "filtriMap": {"codice_tipo_provvedimento": code},
                    "paginazione": {"paginaCorrente": 1, "numeroElementiPerPagina": 1}})
        res[cl] = {f["codice"]: f["valore"] for f in d["facetMap"].get("anno_provvedimento") or []}
        if sum(res[cl].values()) != d["numeroAttiTrovati"]:
            print(f"WARNING {code} class {cl}: year facets sum {sum(res[cl].values())} "
                  f"!= {d['numeroAttiTrovati']}", file=sys.stderr)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, "w"))
    return res


def cmd_export(raw, types, workers, vigenza):
    jobs = codici_jobs(raw, types)
    for code in types:
        counts = class_year_counts(raw, code)
        d = os.path.join(raw, "zips", code)
        os.makedirs(d, exist_ok=True)
        for cl, years in counts.items():
            for y, n in sorted(years.items()):
                dest = os.path.join(d, f"{y}-c{cl}.zip")
                if not os.path.exists(dest):
                    jobs.append((code, y, n, dest, None, cl))
    print(f"{len(jobs)} exports to run", file=sys.stderr)
    with cf.ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(run_export, *j, vigenza): j for j in jobs}
        for f in cf.as_completed(futs):
            try:
                f.result()
            except Exception as e:
                print(f"FAILED {futs[f][:3]}: {e}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["index", "lists", "export"])
    ap.add_argument("--raw", default=DEFAULT_RAW)
    ap.add_argument("--types", default=",".join(TYPES))
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--vigenza", default=dt.date.today().isoformat())
    a = ap.parse_args()
    os.makedirs(a.raw, exist_ok=True)
    types = [t for t in a.types.split(",") if t]
    if a.cmd == "index":
        for t in types:
            print(t, len(index_type(a.raw, t)), file=sys.stderr)
    elif a.cmd == "lists":
        cmd_lists(a.raw)
    else:
        cmd_export(a.raw, types, a.workers, a.vigenza)


if __name__ == "__main__":
    main()
