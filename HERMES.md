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

## Wygląd strony — własny stary rodzinny zeszyt

- Zachowaj oryginalny charakter strony; nie kopiuj projektu Chef_Vittel.
- Papier: ciepły krem `#f5ecd7`, delikatne ziarno z CSS lub osadzonego SVG
  (bez zewnętrznych obrazów) i nieco ciemniejsze brzegi. Atrament tytułów
  `#2c3e7a`, tekst `#3b2f24`, drobne akcenty `#c0584a`.
- Google Fonts z polskimi znakami: Caveat (tytuł strony, przepisy, nagłówki,
  oryginalny zapis; awaryjnie cursive) i Lora (tekst; awaryjnie Georgia, serif).
- Strona główna: tytuł „Przepisy Babci Marysi”, kursywny podtytuł
  „Rodzinne przepisy spisane ręką Babci Marysi”, grupowanie po kategorii
  z odręcznymi nagłówkami. Bez zdjęć na stronie głównej: tekstowy spis
  treści na kartce starego zeszytu, numerowane pozycje z tytułem Caveat
  i datą notatki, jeśli istnieje. Zdjęcia pozostają na stronach przepisów.
- Strona przepisu: oryginalne zdjęcie w białej ramce z cieniem, lekkim
  pochyleniem i taśmą w rogach, klikalne do pełnego rozmiaru. Składniki,
  Przygotowanie i Oryginalny zapis na papierze z jasnoniebieskimi liniami
  oraz cienkim czerwonym marginesem; zachowaj dokładnie końce linii zapisu.
  Uwagi na żółtawej samoprzylepnej kartce; data jako drobny kursywny podpis
  „Notatka z dnia DD.MM.RRRR”.
- Maksymalna szerokość około 900 px. Na telefonie 375 px jedna kolumna wpisów
  i brak poziomego przewijania. Wyłącz pochylenia i animacje dla
  `prefers-reduced-motion`; zachowaj czytelny kontrast.
- Cały interfejs po polsku. Nie zmieniaj treści przepisów ani plików w
  `przepisy/` lub `szablon/` przy zmianach wyglądu. Buduj komplet strony
  w `docs/` (HTML, CSS i kopie zdjęć), z pustym `docs/.nojekyll` oraz
  względnymi odnośnikami działającymi pod ścieżką projektu GitHub Pages.
