"""Buduje statyczną stronę z potwierdzonych przepisów."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
from html import escape
import hashlib
from pathlib import Path
import re
import shutil

import markdown
import yaml

from home import render_home

ROOT = Path(__file__).resolve().parent
VERSION = hashlib.md5((ROOT / "style.css").read_bytes()).hexdigest()[:8]
SOURCE = ROOT / "przepisy"
TRANSCRIPTION = "## Transkrypcja (dokładnie jak na kartce)"
NOTES = "## Uwagi"


def text(value: object) -> str:
    return escape(str(value), quote=True)


def page(title: str, body: str, *, recipe: bool = False, top: str | None = None, bottom: str | None = None) -> str:
    home = "../../index.html" if recipe else "index.html"
    css = "../../style.css" if recipe else "style.css"
    return f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Rodzinne przepisy Babci Marysi">
  <title>{text(title)} — Przepisy Babci Marysi</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;600;700&amp;family=Lora:ital,wght@0,400;0,500;0,600;1,400&amp;display=swap&amp;subset=latin-ext" rel="stylesheet">
  <link rel="stylesheet" href="{css}?v={VERSION}">
</head>
<body class="{'recipe-page' if recipe else 'home-page'}">
  {top or f'<header class="site-header"><nav><a href="{home}">Przepisy Babci Marysi</a></nav></header>'}
  <main>{body}</main>
  {bottom or '<footer>Rodzinne przepisy Babci Marysi</footer>'}
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
    parts = [f'<article><h1 class="recipe-title">{text(title)}</h1>']
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
        parts.append(f'<figure class="pinned-photo"><a href="{text(filename)}" aria-label="Otwórz zdjęcie: {text(caption)}"><img src="{text(filename)}" alt="{text(caption)}" loading="lazy"></a><figcaption>{text(caption)}</figcaption></figure>')
    parts.append('<div class="lined-paper"><section><h2>Składniki</h2><ul class="ingredients">')
    parts.extend(f"<li>{text(item)}</li>" for item in data["skladniki"])
    parts.append("</ul></section><section><h2>Przygotowanie</h2><ol>")
    parts.extend(f"<li>{text(step)}</li>" for step in data["kroki"])
    parts.append("</ol></section><section><h2>Oryginalny zapis</h2>")
    parts.append(f'<pre class="transcription">{text(transcription)}</pre>')
    parts.append("</section></div>")
    if notes:
        parts.append(f'<aside class="sticky-note"><h2>Uwagi</h2>{markdown.markdown(escape(notes))}</aside>')
    uncertain = data.get("niepewne_fragmenty") or []
    if uncertain:
        parts.append('<aside class="sticky-note uncertain"><h2>Niepewne fragmenty</h2><ul>')
        parts.extend(f"<li>{text(item)}</li>" for item in uncertain)
        parts.append("</ul></aside>")
    parts.append('</article><p class="back-link"><a href="../../index.html">← Wszystkie przepisy</a></p>')
    (dest / "index.html").write_text(page(title, "\n".join(parts), recipe=True), encoding="utf-8")


def build(output: Path) -> None:
    if output.resolve() == ROOT or output.resolve() == SOURCE.resolve() or SOURCE.resolve() in output.resolve().parents or output.resolve() in ROOT.parents:
        raise ValueError("Katalog wynikowy nie może nadpisać źródeł")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copyfile(ROOT / "style.css", output / "style.css")
    groups: dict[str, list[tuple[str, str, str | None, str | None]]] = defaultdict(list)
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
        photos = data.get("zdjecia") or []
        thumb = data.get("miniatura") or (photos[0]["plik"] if photos else None)
        if data.get("miniatura"):
            shutil.copyfile(folder / data["miniatura"], destination / data["miniatura"])
        note_date = data.get("data_notatki")
        formatted_date = f'{date.fromisoformat(str(note_date)):%d.%m.%Y}' if note_date else None
        groups[str(data["kategoria"])].append((str(data["tytul"]), slug, thumb, formatted_date))
    render_home(groups, output, ROOT, page)
    (output / ".nojekyll").touch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Buduje stronę przepisów")
    parser.add_argument("--output", type=Path, default=ROOT / "docs")
    build(parser.parse_args().output)
