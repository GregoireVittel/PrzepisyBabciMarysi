"""Buduje statyczną stronę z potwierdzonych przepisów."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
from html import escape
from pathlib import Path
import re
import shutil

import markdown
import yaml

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "przepisy"
TRANSCRIPTION = "## Transkrypcja (dokładnie jak na kartce)"
NOTES = "## Uwagi"


def text(value: object) -> str:
    return escape(str(value), quote=True)


def page(title: str, body: str, *, recipe: bool = False) -> str:
    home = "../../index.html" if recipe else "index.html"
    css = "../../style.css" if recipe else "style.css"
    return f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Rodzinne przepisy Babci Marysi">
  <title>{text(title)} — Przepisy Babci Marysi</title>
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <header><nav><a href="{home}">Przepisy Babci Marysi</a></nav></header>
  <main>{body}</main>
  <footer>Rodzinne przepisy Babci Marysi</footer>
</body>
</html>
"""


def read_recipe(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    match = re.fullmatch(r"---\s*\n(.*?)\n---\s*\n(.*)", raw, re.DOTALL)
    if not match:
        raise ValueError(f"Niepoprawne oznaczenie danych: {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"Niepoprawne dane: {path}")
    return data, match.group(2)


def original_sections(body: str, path: Path) -> tuple[str, str]:
    if body.count(TRANSCRIPTION) != 1:
        raise ValueError(f"Brak jednoznacznej transkrypcji: {path}")
    remainder = body.split(TRANSCRIPTION, 1)[1]
    if NOTES in remainder:
        transcription_part, notes = remainder.split(NOTES, 1)
    else:
        transcription_part, notes = remainder, ""
    match = re.fullmatch(r"\s*```text\r?\n(.*?)\r?\n```\s*", transcription_part, re.DOTALL)
    if not match:
        raise ValueError(f"Niepoprawny blok transkrypcji: {path}")
    return match.group(1), notes.strip()


def render_recipe(data: dict, body: str, folder: Path, dest: Path) -> None:
    title = str(data["tytul"])
    transcription, notes = original_sections(body, folder / "przepis.md")
    parts = [f"<article><h1>{text(title)}</h1>"]
    note_date = data.get("data_notatki")
    if note_date:
        day = date.fromisoformat(str(note_date))
        parts.append(f'<p class="date">Notatka z dnia {day:%d.%m.%Y}</p>')
    for photo in data.get("zdjecia") or []:
        filename = photo["plik"]
        if not isinstance(filename, str) or Path(filename).name != filename or filename in (".", ".."):
            raise ValueError(f"Niepoprawna nazwa zdjęcia: {folder}")
        source = folder / filename
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"Brak zdjęcia: {source}")
        shutil.copyfile(source, dest / filename)
        caption = str(photo.get("opis") or "Oryginalna notatka")
        parts.append(f'<figure><a href="{text(filename)}"><img src="{text(filename)}" alt="{text(caption)}" loading="lazy"></a><figcaption>{text(caption)}</figcaption></figure>')
    parts.append('<h2>Składniki</h2><ul class="ingredients">')
    parts.extend(f"<li>{text(item)}</li>" for item in data["skladniki"])
    parts.append("</ul><h2>Przygotowanie</h2><ol>")
    parts.extend(f"<li>{text(step)}</li>" for step in data["kroki"])
    parts.append("</ol><h2>Oryginalny zapis</h2>")
    parts.append(f'<pre class="transcription">{text(transcription)}</pre>')
    if notes:
        parts.append(f"<h2>Uwagi</h2>{markdown.markdown(escape(notes))}")
    uncertain = data.get("niepewne_fragmenty") or []
    if uncertain:
        parts.append('<aside><h2>Niepewne fragmenty</h2><ul>')
        parts.extend(f"<li>{text(item)}</li>" for item in uncertain)
        parts.append("</ul></aside>")
    parts.append('</article><p><a href="../../index.html">← Wszystkie przepisy</a></p>')
    (dest / "index.html").write_text(page(title, "\n".join(parts), recipe=True), encoding="utf-8")


def build(output: Path) -> None:
    if output.resolve() == ROOT or output.resolve() == SOURCE.resolve() or SOURCE.resolve() in output.resolve().parents or output.resolve() in ROOT.parents:
        raise ValueError("Katalog wynikowy nie może nadpisać źródeł")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copyfile(ROOT / "style.css", output / "style.css")
    groups: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for source in sorted(SOURCE.glob("*/przepis.md")):
        data, body = read_recipe(source)
        if data.get("status") != "zweryfikowany":
            continue
        folder = source.parent
        slug = data["slug"]
        if slug != folder.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError(f"Niepoprawny slug: {source}")
        destination = output / "przepisy" / slug
        destination.mkdir(parents=True)
        render_recipe(data, body, folder, destination)
        groups[str(data["kategoria"])].append((str(data["tytul"]), slug))
    parts = ['<h1>Przepisy Babci Marysi</h1><p>Rodzinne przepisy z oryginalnych notatek.</p>']
    if not groups:
        parts.append("<p>Brak zweryfikowanych przepisów.</p>")
    for category in sorted(groups, key=str.casefold):
        parts.append(f"<section><h2>{text(category)}</h2><ul class=\"recipe-list\">")
        for title, slug in sorted(groups[category], key=lambda entry: entry[0].casefold()):
            parts.append(f'<li><a href="przepisy/{slug}/">{text(title)}</a></li>')
        parts.append("</ul></section>")
    (output / "index.html").write_text(page("Strona główna", "\n".join(parts)), encoding="utf-8")
    (output / ".nojekyll").touch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Buduje stronę przepisów")
    parser.add_argument("--output", type=Path, default=ROOT / "docs")
    build(parser.parse_args().output)
