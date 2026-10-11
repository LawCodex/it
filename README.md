# LawCodex — Italia (Italy)

Italian state legislation as plain Markdown, one file per act, generated from the consolidated
texts ("testo vigente") of **Normattiva**, the official database of Italian legislation run by
the Istituto Poligrafico e Zecca dello Stato for the Presidenza del Consiglio dei Ministri.

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as Markdown in git.

- Jurisdiction: Italy (`it`), language: Italian
- Source: Normattiva open data API — <https://dati.normattiva.it> (texts as on <https://www.normattiva.it>)
- Retrieved: 2026-10-11 (text in force — *vigente* — on that date)
- Total: **0** acts

## Coverage

Every act of the types below that Normattiva does **not** mark as repealed, in its consolidated
version in force on the retrieval date (all amendments applied, as published by Normattiva).

<!-- counts -->
<!-- /counts -->

"In force" means: Normattiva *classe provvedimento* 1 ("atto normativo – senza aggiornamenti")
or 2 ("atto normativo – aggiornato"), metadata flag `abrogato: no`, not listed in the Normattiva
collections "Atti normativi abrogati" or "DL decaduti" (decree-laws not converted into law),
and not consisting only of abrogation notices.

### Codici

The codes listed in Normattiva's "Codici" collection that are in force are stored in `codici/`
(not in their type directory). Most classic codes are formally the annex of an approving decree
(e.g. the *Codice civile* is annexed to Regio decreto 16 marzo 1942, n. 262): the file contains
the approving decree followed by the code, with the code's own structure (Libro / Titolo / Capo /
Sezione / §) as headings.

<!-- codes -->
<!-- /codes -->

## Not covered

- **Repealed acts** (Normattiva class 3 "abrogato", ~124,000 acts, mostly Regi decreti and
  pre-1990 laws) and **lapsed decree-laws** (DL decaduti): skipped.
- **Historical versions** (*multivigente*): only the text in force on the retrieval date is kept.
- **Secondary legislation of other authorities**: decreti ministeriali, DPCM, decreti luogotenenziali
  (non-legislative), decrees of the Capo provvisorio dello Stato and other minor pre-republican
  decree types present in Normattiva (~4,000 in force in total) are not included.
- **Regional and provincial legislation** (leggi regionali): not in Normattiva.
- **EU law**: see the `eu` repository.
- **Graphics**: parts of acts that Normattiva only has as images are rendered as the notice
  "Parte di provvedimento in formato grafico" (as on normattiva.it).
- Many DPRs and Regi decreti, especially before 1988, are individual administrative acts
  (recognition of legal persons, changes to statutes of universities, municipal boundaries...)
  that Normattiva includes in its numbered collection and does not mark as repealed: they are
  included as published by Normattiva, since no reliable criterion separates them from normative
  DPRs (regolamenti, testi unici, decrees having force of law).

## Structure

```
costituzione/costituzione.md                     Costituzione della Repubblica Italiana
codici/<code>.md                                 Codici (civile, penale, procedura...)
leggi-costituzionali/<year>/                     Leggi costituzionali
leggi/<year>/                                    Leggi
decreti-legislativi/<year>/                      Decreti legislativi
decreti-legge/<year>/                            Decreti-legge (text as converted/amended)
dpr/<year>/[<month>/]                            Decreti del Presidente della Repubblica
regi-decreti-legge/<year>/                       Regi decreti-legge
regi-decreti-legislativi/<year>/                 Regi decreti legislativi
decreti-legislativi-luogotenenziali/<year>/      Decreti legislativi luogotenenziali
decreti-legge-luogotenenziali/<year>/            Decreti-legge luogotenenziali
decreti-legislativi-cps/<year>/                  D.Lgs. del Capo provvisorio dello Stato
decreti-legislativi-presidenziali/<year>/        Decreti legislativi presidenziali
regi-decreti/<year>/[<month>/]                   Regi decreti
```

`<year>` is the year of the act (date of enactment). Years with more than 900 acts are split
into month sub-directories (`01` … `12`). File names are
`<date>-n-<number>-<slug-of-title>.md`, e.g.
`leggi/1990/1990-08-07-n-241-nuove-norme-in-materia-di-procedimento-amministrativo-e-di.md`.

Each file has YAML front matter:

```yaml
title: "LEGGE 7 agosto 1990, n. 241 — Nuove norme in materia di procedimento amministrativo..."
identifier: "urn:nir:stato:legge:1990-08-07;241"      # URN:NIR
eli: "https://www.normattiva.it/eli/id/1990/08/18/090G0294/CONSOLIDATED/20250101"
type: act        # constitution | code | constitutional_law | act | legislative_decree | decree_law | presidential_decree | royal_decree | royal_decree_law | ...
jurisdiction: it
language: it
date: 1990-08-07                 # date of the act
last_amended: 2025-01-01         # date of the consolidated version (from the ELI), if amended
status: in_force
gazzetta_ufficiale: "Gazzetta Ufficiale n. 192 del 1990-08-18"
codice_redazionale: "090G0294"   # Normattiva / GU editorial code
source: "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:1990-08-07;241"
retrieved: 2026-10-11
```

The body follows Normattiva's text: the act's structural divisions (Parte / Libro / Titolo /
Capo / Sezione / §) become `##`… headings (only the levels used by an act are allocated, beyond
`######` they are **bold**), articles and annexes (Allegati) are the deepest heading level
(`Art. N - rubrica`). The text of each article is reproduced line by line as published by
Normattiva, including its editorial conventions: text inserted or replaced by amendments is
between double parentheses `(( ... ))`, numbers such as `((19))` refer to the "AGGIORNAMENTO"
notes that follow the article, and repealed provisions are replaced by notices such as
`((ARTICOLO ABROGATO DAL ...))`. Fixed-width tables are kept as fenced text blocks. Normattiva's
notes attached to an article are kept as `>` blockquotes.

## Licence

Legislative texts and official acts of the State are not protected by copyright in Italy
(art. 5, legge 22 aprile 1941, n. 633). The Normattiva open data are released by the Istituto
Poligrafico e Zecca dello Stato under the
[Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
licence (since 1 January 2026; see <https://dati.normattiva.it>, "Dati disponibili").
Attribution: Normattiva — Istituto Poligrafico e Zecca dello Stato, <https://www.normattiva.it>.
This repository is **not** an official publication; only the texts published in the
*Gazzetta Ufficiale* have legal value.

## Regenerating

```sh
pip install -r scripts/requirements.txt
python scripts/fetch.py index          # list of acts per type (sync search API) -> ../_raw/it/index
python scripts/fetch.py lists          # "abrogati", "DL decaduti" and "Codici" collections
python scripts/fetch.py export         # async JSON exports per type/year/class -> ../_raw/it/zips
python scripts/convert.py              # JSON -> Markdown in this repository
python scripts/readme.py               # refresh the counts in this README
```

`fetch.py export` options: `--types PLE,PLL,...` (Normattiva act-type codes, see
`scripts/common.py`), `--workers N` (parallel export jobs, default 3), `--vigenza YYYY-MM-DD`
(date of the text in force, default today), `--raw DIR`. The exports are produced server-side by
Normattiva's asynchronous search API (`/ricerca-asincrona`), one job per act type, year and class,
then downloaded as zip files of JSON documents.
