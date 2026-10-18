# Instructions for Hermes — PrzepisyBabciMarysi

Goal: build and maintain a static recipe website (GitHub Pages) from the
recipe folders in `przepisy/`. All visible website content must be in Polish.

## Input — one folder per recipe

`przepisy/<slug>/przepis.md` has YAML front matter plus a Markdown body.

Front matter fields:
- `tytul` — recipe title (page heading)
- `slug` — URL slug, equals the folder name
- `kategoria` — category used for grouping on the index page
- `zdjecia` — list of photos (`plik` = file in the same folder, `opis` = caption)
- `data_notatki` — date of the original note (may be empty)
- `status` — `zweryfikowany` (publish) or `do-weryfikacji` (do NOT publish)
- `niepewne_fragmenty` — list of uncertain readings (show as a note if non-empty)
- `skladniki` — ingredient lines, exactly as they should be displayed
- `kroki` — preparation steps, in order

Body sections:
- `## Transkrypcja (dokładnie jak na kartce)` — verbatim transcription in a
  ```text block. Display it as-is, preserving line breaks.
- `## Uwagi` — optional notes, display as-is.

## Hard rules

1. NEVER edit, correct, modernise or "improve" any recipe text — not the
   transcription, ingredients, steps or notes. No added quantities,
   temperatures, times or conversions.
2. Never transcribe photos yourself. Text comes only from `przepis.md`.
3. Skip recipes with `status: "do-weryfikacji"`.
4. Do not rename or recompress the photo files; copy them as-is.
5. All UI text (navigation, headings, labels, footer) in Polish.

## Site requirements

- Home page: title „Przepisy Babci Marysi”, recipes grouped by `kategoria`,
  sorted alphabetically by `tytul`.
- Recipe page: title → photo(s) of the original note (click to enlarge) →
  „Składniki” → „Przygotowanie” (numbered) → „Oryginalny zapis” (transcription)
  → „Uwagi” (if present). If `data_notatki` is set, show
  „Notatka z dnia DD.MM.RRRR”.
- Must work on phones (most visitors will read while cooking).
- Prefer Jekyll (native GitHub Pages) or plain generated HTML via a Python
  build script — no heavy frameworks.
- Adding a new recipe must only require adding a new folder; the site
  rebuilds without manual edits to other files.
- Po każdej zmianie w `przepisy/` uruchom `build.py` i zatwierdź zaktualizowany
  folder `docs/` w tym samym commicie.
