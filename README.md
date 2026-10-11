# LawCodex — Italia (Italy)

Italian state legislation as plain Markdown, one file per act, generated from the consolidated
texts ("testo vigente") of **Normattiva**, the official database of Italian legislation run by
the Istituto Poligrafico e Zecca dello Stato for the Presidenza del Consiglio dei Ministri.

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as Markdown in git.

- Jurisdiction: Italy (`it`), language: Italian
- Source: Normattiva open data API — <https://dati.normattiva.it> (texts as on <https://www.normattiva.it>)
- Retrieved: 2026-10-11 (text in force — *vigente* — on that date)
- Total: **76,894** acts

## Coverage

Every act of the types below that Normattiva does **not** mark as repealed, in its consolidated
version in force on the retrieval date (all amendments applied, as published by Normattiva).

<!-- counts -->
| Directory | Category | Files |
|---|---|---:|
| `costituzione/` | Costituzione della Repubblica Italiana (1947) | 1 |
| `codici/` | Codici (from the Normattiva "Codici" collection) | 37 |
| `leggi-costituzionali/` | Leggi costituzionali | 50 |
| `leggi/` | Leggi | 13,721 |
| `decreti-legislativi/` | Decreti legislativi | 2,416 |
| `decreti-legge/` | Decreti-legge (in force, not lapsed) | 1,641 |
| `dpr/` | Decreti del Presidente della Repubblica | 46,671 |
| `regi-decreti-legge/` | Regi decreti-legge (1861-1946) | 312 |
| `regi-decreti-legislativi/` | Regi decreti legislativi | 40 |
| `decreti-legislativi-luogotenenziali/` | Decreti legislativi luogotenenziali (1944-1946) | 193 |
| `decreti-legge-luogotenenziali/` | Decreti-legge luogotenenziali (1915-1919, 1944-1946) | 20 |
| `decreti-legislativi-cps/` | Decreti legislativi del Capo provvisorio dello Stato (1946-1948) | 526 |
| `decreti-legislativi-presidenziali/` | Decreti legislativi presidenziali (1946) | 57 |
| `regi-decreti/` | Regi decreti (1861-1946) | 11,209 |
| | **Total** | **76,894** |
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
- [DECRETO LEGISLATIVO 03 aprile 2006, n. 152 — Norme in materia ambientale.](codici/codice-ambiente.md)
- [DECRETO LEGISLATIVO 07 marzo 2005, n. 82 — Codice dell'amministrazione digitale.](codici/codice-amministrazione-digitale.md)
- [DECRETO LEGISLATIVO 06 settembre 2011, n. 159 — Codice delle leggi antimafia e delle misure di prevenzione, nonche' nuove disposizioni in materia di documentazione antimafia, a norma degli articoli 1 e 2 della legge 13 agosto 2010, n. 136.](codici/codice-antimafia.md)
- [DECRETO LEGISLATIVO 07 settembre 2005, n. 209 — Codice delle assicurazioni private.](codici/codice-assicurazioni-private.md)
- [DECRETO LEGISLATIVO 22 gennaio 2004, n. 42 — Codice dei beni culturali e del paesaggio, ai sensi dell'articolo 10 della legge 6 luglio 2002, n. 137.](codici/codice-beni-culturali-e-paesaggio.md)
- [REGIO DECRETO 16 marzo 1942, n. 262 — Approvazione del testo del Codice civile.](codici/codice-civile.md)
- [DECRETO LEGISLATIVO 01 agosto 2003, n. 259 — Codice delle comunicazioni elettroniche.](codici/codice-comunicazioni-elettroniche.md)
- [DECRETO LEGISLATIVO 31 marzo 2023, n. 36 — Codice dei contratti pubblici in attuazione dell'articolo 1 della legge 21 giugno 2022, n. 78, recante delega al Governo in materia di contratti pubblici.](codici/codice-contratti-pubblici.md)
- [DECRETO LEGISLATIVO 12 gennaio 2019, n. 14 — Codice della crisi d'impresa e dell'insolvenza in attuazione della legge 19 ottobre 2017, n. 155.](codici/codice-crisi-impresa-e-insolvenza.md)
- [DECRETO LEGISLATIVO 06 settembre 2005, n. 206 — Codice del consumo, a norma dell'articolo 7 della legge 29 luglio 2003, n. 229.](codici/codice-del-consumo.md)
- [DECRETO LEGISLATIVO 30 aprile 1992, n. 285 — Nuovo codice della strada.](codici/codice-della-strada.md)
- [DECRETO LEGISLATIVO 26 agosto 2016, n. 174 — Codice di giustizia contabile, adottato ai sensi dell'articolo 20 della legge 7 agosto 2015, n. 124.](codici/codice-giustizia-contabile.md)
- [DECRETO LEGISLATIVO 27 novembre 2025, n. 184 — Codice degli incentivi, in attuazione dell'articolo 3, commi 1 e 2, lettera b), della legge 27 ottobre 2023, n. 160.](codici/codice-incentivi.md)
- [DECRETO LEGISLATIVO 18 luglio 2005, n. 171 — Codice della nautica da diporto ed attuazione della direttiva 2003/44/CE, a norma dell'articolo 6 della legge 8 luglio 2003, n. 172.](codici/codice-nautica-da-diporto.md)
- [REGIO DECRETO 30 marzo 1942, n. 327 — Approvazione del testo definitivo del Codice della navigazione.](codici/codice-navigazione.md)
- [DECRETO LEGISLATIVO 15 marzo 2010, n. 66 — Codice dell'ordinamento militare.](codici/codice-ordinamento-militare.md)
- [DECRETO LEGISLATIVO 11 aprile 2006, n. 198 — Codice delle pari opportunita' tra uomo e donna, a norma dell'articolo 6 della legge 28 novembre 2005, n. 246.](codici/codice-pari-opportunita.md)
- [REGIO DECRETO 19 ottobre 1930, n. 1398 — Approvazione del testo definitivo del Codice Penale.](codici/codice-penale.md)
- [DECRETO DEL PRESIDENTE DELLA REPUBBLICA 29 marzo 1973, n. 156 — Approvazione del testo unico delle disposizioni legislative in materia postale, di bancoposta e di telecomunicazioni.](codici/codice-postale-e-telecomunicazioni.md)
- [REGIO DECRETO 28 ottobre 1940, n. 1443 — Codice di procedura civile.](codici/codice-procedura-civile.md)
- [DECRETO DEL PRESIDENTE DELLA REPUBBLICA 22 settembre 1988, n. 447 — Approvazione del codice di procedura penale.](codici/codice-procedura-penale.md)
- [DECRETO LEGISLATIVO 02 luglio 2010, n. 104 — Attuazione dell'articolo 44 della legge 18 giugno 2009, n. 69, recante delega al governo per il riordino del processo amministrativo.](codici/codice-processo-amministrativo.md)
- [DECRETO LEGISLATIVO 10 febbraio 2005, n. 30 — Codice della proprieta' industriale, a norma dell'articolo 15 della legge 12 dicembre 2002, n. 273.](codici/codice-proprieta-industriale.md)
- [DECRETO LEGISLATIVO 02 gennaio 2018, n. 1 (Raccolta 2018) — Codice della protezione civile.](codici/codice-protezione-civile.md)
- [DECRETO LEGISLATIVO 30 giugno 2003, n. 196 — Codice in materia di protezione dei dati personali ((, recante disposizioni per l'adeguamento dell'ordinamento nazionale al regolamento (UE) n. 2016/679 del Parlamento europeo e del Consiglio, del 27 aprile 2016, relativo alla protezione delle persone fisiche con riguardo al trattamento dei dati personali, nonche' alla libera circolazione di tali dati e che abroga la direttiva 95/46/CE)).](codici/codice-protezione-dati-personali.md)
- [DECRETO LEGISLATIVO 03 luglio 2017, n. 117 — Codice del Terzo settore, a norma dell'articolo 1, comma 2, lettera b), della legge 6 giugno 2016, n. 106.](codici/codice-terzo-settore.md)
- [DECRETO LEGISLATIVO 23 maggio 2011, n. 79 — Codice della normativa statale in tema di ordinamento e mercato del turismo, a norma dell'articolo 14 della legge 28 novembre 2005, n. 246, nonche' attuazione della direttiva 2008/122/CE, relativa ai contratti di multiproprieta', contratti relativi ai prodotti per le vacanze di lungo termine, contratti di rivendita e di scambio.](codici/codice-turismo.md)
- [REGIO DECRETO 20 febbraio 1941, n. 303 — Codici penali militari di pace e di guerra](codici/codici-penali-militari-di-pace-e-di-guerra.md)
- [REGIO DECRETO 30 marzo 1942, n. 318 — Disposizioni per l'attuazione del Codice civile e disposizioni transitorie.](codici/disposizioni-attuazione-codice-civile.md)
- [REGIO DECRETO 18 dicembre 1941, n. 1368 — Disposizioni per l'attuazione del Codice di procedura civile e disposizioni transitorie.](codici/disposizioni-attuazione-codice-procedura-civile.md)
- [REGIO DECRETO 09 settembre 1941, n. 1023 — Disposizioni di coordinamento, transitorie e di attuazione dei Codici penali militari di pace e di guerra.](codici/disposizioni-attuazione-codici-penali-militari.md)
- [DECRETO LEGISLATIVO 28 luglio 1989, n. 271 — Norme di attuazione, di coordinamento e transitorie del codice di procedura penale.](codici/norme-attuazione-codice-procedura-penale.md)
- [DECRETO DEL PRESIDENTE DELLA REPUBBLICA 05 ottobre 2010, n. 207 — Regolamento di esecuzione ed attuazione del decreto legislativo 12 aprile 2006, n. 163, recante «Codice dei contratti pubblici relativi a lavori, servizi e forniture in attuazione delle direttive 2004/17/CE e 2004/18/CE».](codici/regolamento-codice-contratti-pubblici-2006.md)
- [DECRETO DEL PRESIDENTE DELLA REPUBBLICA 16 dicembre 1992, n. 495 — Regolamento di esecuzione e di attuazione del nuovo codice della strada.](codici/regolamento-codice-della-strada.md)
- [DECRETO DEL PRESIDENTE DELLA REPUBBLICA 15 febbraio 1952, n. 328 — Approvazione del Regolamento per l'esecuzione del Codice della navigazione (Navigazione marittima).](codici/regolamento-codice-navigazione-marittima.md)
- [DECRETO 30 settembre 1989, n. 334 — Regolamento per l'esecuzione del codice di procedura penale.](codici/regolamento-codice-procedura-penale.md)
- [DECRETO 13 gennaio 2010, n. 33 — Regolamento di attuazione del Codice della proprieta' industriale, adottato con decreto legislativo 10 febbraio 2005, n. 30.](codici/regolamento-codice-proprieta-industriale.md)
<!-- /codes -->

## Not covered

- **Repealed acts** (Normattiva class 3 "abrogato", ~124,000 acts, mostly Regi decreti and
  pre-1990 laws) and **lapsed decree-laws** (DL decaduti): skipped.
- **Historical versions** (*multivigente*): only the text in force on the retrieval date is kept.
- **Acts not yet in force** on the retrieval date (published in the Gazzetta Ufficiale but still
  in their *vacatio legis*, e.g. a few laws of late September / October 2026): Normattiva's
  "vigente" export does not contain them yet; they will appear on the next refresh.
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
dpr/<year>/[<MM>/ or <MM-DD>/]                   Decreti del Presidente della Repubblica
regi-decreti-legge/<year>/                       Regi decreti-legge
regi-decreti-legislativi/<year>/                 Regi decreti legislativi
decreti-legislativi-luogotenenziali/<year>/      Decreti legislativi luogotenenziali
decreti-legge-luogotenenziali/<year>/            Decreti-legge luogotenenziali
decreti-legislativi-cps/<year>/                  D.Lgs. del Capo provvisorio dello Stato
decreti-legislativi-presidenziali/<year>/        Decreti legislativi presidenziali
regi-decreti/<year>/[<month>/]                   Regi decreti
```

`<year>` is the year of the act (date of enactment). Years with more than 900 acts are split
into month sub-directories (`01` … `12`), years with more than 3,000 acts (DPR 1952) into day sub-directories (`MM-DD`). File names are
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
