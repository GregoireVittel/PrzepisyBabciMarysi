"""Strona główna w stylu „zeszytu Babci”."""
from __future__ import annotations

from html import escape
from pathlib import Path
import shutil
import unicodedata

import markdown

# Teksty strony głównej — można je zmieniać tutaj
HERO_LINE1 = "Smaki, które"
HERO_LINE2 = "łączą pokolenia"
HERO_TEXT = ("Tu znajdziesz nasze rodzinne przepisy – spisane z miłością ręką Babci Marysi. "
             "To więcej niż ciasta i desery, to wspomnienia, które zawsze smakują tak samo dobrze.")
NOTE_TEXT = "Najlepsze przepisy zawsze smakują lepiej razem"
QUOTE = "Dobre jedzenie tworzy najpiękniejsze wspomnienia."
SIGNATURE = "Babcia Marysia"

COLORS = {"ciasta": "pink", "masy i kremy": "green", "pączki i faworki": "yellow",
          "serniki": "blue", "torty": "peach", "wypieki": "lilac", "przetwory": "green", "dania i zupy": "yellow"}
CYCLE = ["pink", "green", "yellow", "blue", "peach", "lilac"]

S = 'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "ciasta": f'<svg viewBox="0 0 64 64" {S}><ellipse cx="32" cy="26" rx="22" ry="7"/><path d="M10 26v16c0 4 10 7 22 7s22-3 22-7V26"/><path d="M10 34c0 4 10 7 22 7s22-3 22-7"/><circle cx="32" cy="15" r="4"/><path d="M32 11c1-3 3-4 5-4"/></svg>',
    "masy i kremy": f'<svg viewBox="0 0 64 64" {S}><path d="M8 34h48c0 11-10 18-24 18S8 45 8 34z"/><path d="M14 34c2-6 8-9 14-7 4-5 13-4 16 2 4-1 8 1 9 5"/><path d="M40 30L55 10"/><path d="M50 9c3-3 8-1 7 3-1 3-5 4-7 3"/></svg>',
    "pączki i faworki": f'<svg viewBox="0 0 64 64" {S}><ellipse cx="24" cy="38" rx="16" ry="11"/><ellipse cx="42" cy="30" rx="15" ry="10"/><path d="M18 33h2M26 31h2M22 39h2M38 25h2M46 27h2M42 33h2"/></svg>',
    "serniki": f'<svg viewBox="0 0 64 64" {S}><path d="M8 40L50 22l6 4v14z"/><path d="M8 40v8h48v-8"/><path d="M8 44h48"/><circle cx="44" cy="17" r="4"/><path d="M47 13l3-4"/></svg>',
    "torty": f'<svg viewBox="0 0 64 64" {S}><path d="M10 30h44v20H10z"/><path d="M10 40c5 3 9-3 14 0s9 3 14 0 10-3 16 0"/><path d="M16 30v-6h32v6"/><path d="M24 24v-8M32 24v-8M40 24v-8"/><path d="M24 12c-1 1-1 3 0 3 1 0 1-2 0-3zM32 12c-1 1-1 3 0 3 1 0 1-2 0-3zM40 12c-1 1-1 3 0 3 1 0 1-2 0-3z"/></svg>',
    "przetwory": f'<svg viewBox="0 0 64 64" {S}><path d="M20 14h24v6H20z"/><path d="M22 20c-6 4-8 9-8 16v12c0 4 3 7 7 7h22c4 0 7-3 7-7V36c0-7-2-12-8-16"/><path d="M18 34h28"/><circle cx="27" cy="44" r="4"/><circle cx="38" cy="42" r="4"/><path d="M27 40c0-2 1-3 3-4M38 38c0-2 1-3 3-4"/></svg>',
    "dania i zupy": f'<svg viewBox="0 0 64 64" {S}><path d="M8 30h48c0 12-10 20-24 20S8 42 8 30z"/><path d="M20 50h24"/><path d="M24 22c-2-3 2-5 0-8M32 22c-2-3 2-5 0-8M40 22c-2-3 2-5 0-8"/></svg>',
    "default": f'<svg viewBox="0 0 64 64" {S}><path d="M12 42c4-16 18-26 34-24-8 4-12 10-12 18 0 4 2 8 6 10-10 4-22 2-28-4z"/><path d="M20 38c4-6 9-10 15-12M26 44c3-5 7-8 12-10"/></svg>',
}
HEART = '<svg class="heart" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.3C1 8.4 3.1 5 6.6 5c2.2 0 3.6 1.2 4.4 2.6.8-1.4 2.2-2.6 4.4-2.6 3.5 0 5.6 3.4 4.2 6.7C19.5 16.4 12 21 12 21z" fill="none" stroke="currentColor" stroke-width="2"/></svg>'


def sprig(cls: str) -> str:
    """Oryginalna, prosta gałązka polnych kwiatów (SVG)."""
    flowers = [(30, 22, "#c0584a"), (52, 40, "#6f8cc9"), (22, 58, "#f4efe2"), (60, 70, "#c0584a"), (38, 84, "#e8c45a")]
    out = [f'<svg class="sprig {cls}" viewBox="0 0 90 130" aria-hidden="true">',
           '<path d="M45 128C44 96 40 66 30 22M44 100c4-20 6-40 8-60M42 80c-8-6-14-14-20-22M44 108c6-12 10-24 16-38" fill="none" stroke="#6d8a55" stroke-width="2"/>',
           '<g fill="#88a46c"><ellipse cx="36" cy="60" rx="7" ry="3" transform="rotate(-40 36 60)"/><ellipse cx="50" cy="76" rx="7" ry="3" transform="rotate(35 50 76)"/><ellipse cx="38" cy="98" rx="7" ry="3" transform="rotate(-30 38 98)"/></g>']
    for x, y, c in flowers:
        petals = "".join(f'<ellipse cx="{x}" cy="{y-5}" rx="3" ry="5" transform="rotate({a} {x} {y})" fill="{c}" stroke="#00000018"/>' for a in range(0, 360, 72))
        out.append(petals + f'<circle cx="{x}" cy="{y}" r="2.6" fill="#e3b53c"/>')
    out.append("</svg>")
    return "".join(out)


def norm(value: str) -> str:
    value = value.lower().replace("ł", "l")
    return "".join(c for c in unicodedata.normalize("NFD", value) if unicodedata.category(c) != "Mn")


def anchor(category: str) -> str:
    return "kat-" + "-".join(norm(category).split())


def plural(n: int) -> str:
    if n == 1:
        return "1 przepis"
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return f"{n} przepisy"
    return f"{n} przepisów"


def icon(category: str) -> str:
    return ICONS.get(category.lower(), ICONS["default"])


def color(category: str, index: int) -> str:
    return COLORS.get(category.lower(), CYCLE[index % len(CYCLE)])


def header(about: bool, active: str) -> str:
    links = [("index.html", "Strona główna", "home"), ("index.html#zeszyt", "Przepisy", "recipes")]
    if about:
        links.append(("o-babci.html", "O babci", "about"))
    nav = "".join(f'<a href="{h}"{" class=active" if k == active else ""}>{t}</a>' for h, t, k in links)
    return (f'<header class="home-header">{sprig("left")}<div class="brand"><a href="index.html" class="brand-title">Przepisy Babci Marysi</a>'
            f'<span class="brand-heart">{HEART}</span><span class="brand-sub">Rodzinne przepisy spisane ręką Babci Marysi</span></div>'
            f'<nav class="main-nav">{nav}<a href="index.html#szukaj" class="search-link" aria-label="Szukaj"><svg viewBox="0 0 24 24" {S}><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg></a></nav>{sprig("right")}</header>')


def footer() -> str:
    return (f'<footer class="home-footer">{sprig("left")}<blockquote><p>„{escape(QUOTE)}”</p>{HEART}'
            f'<cite>– {escape(SIGNATURE)}</cite></blockquote>{sprig("right")}</footer>')


def render_home(groups: dict, output: Path, root: Path, page) -> None:
    about = (root / "o-babci.md").exists()
    cats = sorted(groups, key=str.casefold)
    zasoby = root / "zasoby"
    if zasoby.is_dir():
        shutil.copytree(zasoby, output / "zasoby", dirs_exist_ok=True)
    hero = (f'<section class="hero hero-photo"><div class="hero-inner"><div class="hero-text"><h1><span class="h1-serif">{escape(HERO_LINE1)}</span>'
            f'<span class="h1-script">{escape(HERO_LINE2)} {HEART}</span></h1><p>{escape(HERO_TEXT)}</p>'
            f'<form class="search" id="szukaj" role="search" onsubmit="return false"><svg viewBox="0 0 24 24" {S}><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg>'
            f'<input type="search" id="q" placeholder="Znajdź swój ulubiony przepis..." aria-label="Szukaj przepisu" autocomplete="off">'
            f'<button type="submit" id="go">Szukaj</button></form></div>'
            f'<p class="note">{escape(NOTE_TEXT)} {HEART} <span>{escape(SIGNATURE)}</span></p></div></section>')
    def tile(c, i):
        slug = anchor(c)[4:]
        if (root / "zasoby" / "kafelki" / f"{slug}.jpg").exists():
            return (f'<a class="tile tile-photo tile-{slug}" href="#{anchor(c)}" aria-label="{escape(c)} – {plural(len(groups[c]))}">'
                    f'<img src="zasoby/kafelki/{slug}.jpg" alt="" loading="lazy"><span class="tile-badge">{plural(len(groups[c]))}</span></a>')
        return (f'<a class="tile tile-{color(c, i)}" href="#{anchor(c)}"><span class="tile-name">{escape(c)}</span>'
                f'<span class="tile-count">{plural(len(groups[c]))}</span><span class="tile-icon">{icon(c)}</span></a>')
    tiles = "".join(tile(c, i) for i, c in enumerate(cats))
    # Zeszyt: zakładki – jedna kategoria naraz, wpisy w dwóch kolumnach
    SUB_ORDER = ["Zupy", "Pierogi, kluski i placki", "Gołąbki", "Mięsa i drób", "Dodatki"]

    def panel(c, i):
        entries = sorted(groups[c], key=lambda e: e[0].casefold())
        subs = {}
        for e in entries:
            subs.setdefault(e[4], []).append(e)
        order = sorted(subs, key=lambda k: (k == "", SUB_ORDER.index(k) if k in SUB_ORDER else 99, k))
        blocks = []
        for k in order:
            items = "".join(f'<li data-name="{escape(norm(t))}"><span class="num">{n:02d}.</span><a href="przepisy/{s}/">{escape(t)}</a><span class="chev">›</span></li>'
                            for n, (t, s, *_rest) in enumerate(subs[k], 1))
            head = f'<h4 class="nb-sub">{escape(k)}</h4>' if k else ''
            blocks.append(f'<div class="nb-group">{head}<ol>{items}</ol></div>')
        return (f'<section class="nb-cat nb-{color(c, i)}" id="{anchor(c)}" role="tabpanel" aria-label="{escape(c)}">'
                f'<h3><span class="nb-icon">{icon(c)}</span><span class="nb-title">{escape(c)}</span><span class="nb-count">{plural(len(entries))}</span></h3>'
                f'<div class="nb-cols">{"".join(blocks)}</div></section>')

    tabs = "".join(f'<button type="button" class="nb-tab nb-{color(c, i)}" role="tab" data-target="{anchor(c)}">{escape(c)}</button>' for i, c in enumerate(cats))
    panels = "".join(panel(c, i) for i, c in enumerate(cats))
    notebook = (f'<section class="notebook-wrap" id="zeszyt"><h2>Otwórz zeszyt Babci {HEART}</h2><p class="sub">Wybierz kategorię i odkryj nasze sprawdzone, rodzinne przepisy.</p>'
                f'<div class="nb-tabs" role="tablist">{tabs}</div>'
                f'<p class="no-results" hidden>Nie znaleziono przepisu. Spróbuj innego słowa.</p>'
                f'<div class="notebook"><div class="spiral" aria-hidden="true"></div>{panels}</div></section>')
    script = """<script>
(function(){
var root=document.getElementById('zeszyt');if(!root)return;root.classList.add('tabs-on');
var cats=[].slice.call(root.querySelectorAll('.nb-cat')),tabs=[].slice.call(root.querySelectorAll('.nb-tab')),q=document.getElementById('q');
function show(id){if(!document.getElementById(id))id=cats[0].id;cats.forEach(function(c){c.classList.toggle('active',c.id===id);});
tabs.forEach(function(t){var on=t.dataset.target===id;t.classList.toggle('active',on);t.setAttribute('aria-selected',on);});}
function n(s){return s.toLowerCase().replace(/ł/g,'l').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}
function f(){var v=q?n(q.value.trim()):'',any=false;root.classList.toggle('searching',!!v);
cats.forEach(function(c){var vis=0;c.querySelectorAll('li').forEach(function(li){var ok=!v||li.dataset.name.indexOf(v)>-1;li.hidden=!ok;if(ok)vis++;});
c.querySelectorAll('.nb-group').forEach(function(g){g.hidden=!g.querySelector('li:not([hidden])');});
c.classList.toggle('has-hits',!!(v&&vis));if(vis)any=true;});root.querySelector('.no-results').hidden=any;}
tabs.forEach(function(t){t.addEventListener('click',function(){if(q){q.value='';f();}show(t.dataset.target);history.replaceState(null,'','#'+t.dataset.target);});});
function fromHash(){var h=location.hash.slice(1);if(h.indexOf('kat-')===0){show(h);root.scrollIntoView({behavior:'smooth'});}}
window.addEventListener('hashchange',fromHash);show((location.hash.slice(1).indexOf('kat-')===0)?location.hash.slice(1):cats[0].id);
if(q){q.addEventListener('input',f);document.getElementById('szukaj').addEventListener('submit',function(){f();root.scrollIntoView({behavior:'smooth'});});}
})();</script>"""
    body = hero + f'<section class="tiles">{tiles}</section>' + notebook + script
    (output / "index.html").write_text(page("Strona główna", body, top=header(about, "home"), bottom=footer()), encoding="utf-8")
    if about:
        content = markdown.markdown((root / "o-babci.md").read_text(encoding="utf-8"))
        (output / "o-babci.html").write_text(page("O babci", f'<article class="about lined-paper">{content}</article>', top=header(about, "about"), bottom=footer()), encoding="utf-8")
