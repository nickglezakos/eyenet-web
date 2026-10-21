#!/usr/bin/env python3
"""Build the English EyeNet Investor Primer wiki (value-wiki UX, EN only)."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "eyenet-investor-primer.html"
ASSET_V = "20261021q"

PAGE_ORDER = [
    "",
    "the-bet",
    "what-changes",
    "where-it-pays",
    "how-it-is-sold",
    "seed-ladder",
    "footprint",
    "addendum-a",
    "addendum-b",
]

# Primer section id → wiki slug + titles
SECTIONS = [
    {
        "id": "page-1",
        "slug": "the-bet",
        "num": "01",
        "nav": "The bet",
        "title": "The bet",
        "card": "Incumbents sell cloud storage; EyeNet sells sovereignty and operational action.",
    },
    {
        "id": "page-2",
        "slug": "what-changes",
        "num": "02",
        "nav": "What changes",
        "title": "What changes",
        "card": "Edge, action, and hardware-bound scale — not another camera cloud.",
    },
    {
        "id": "page-3",
        "slug": "where-it-pays",
        "num": "03",
        "nav": "Where it pays",
        "title": "Where it pays",
        "card": "Highest-value wedges across care, HR, signage, family, security, and shipping.",
    },
    {
        "id": "page-4",
        "slug": "how-it-is-sold",
        "num": "04",
        "nav": "How it is sold",
        "title": "How it is sold",
        "card": "B2C Light, B2B, and Enterprise motions with cite-backed pockets.",
    },
    {
        "id": "page-5",
        "slug": "seed-ladder",
        "num": "05",
        "nav": "Seed ladder",
        "title": "Seed scenarios — from burn up",
        "card": "$0.5M → $1M → $2.5M ladder with staged outcomes.",
    },
    {
        "id": "page-6",
        "slug": "footprint",
        "num": "06",
        "nav": "Footprint",
        "title": "Footprint steps by scenario",
        "card": "What each seed step funds: product, GTM, and footprint.",
    },
    {
        "id": "page-7",
        "slug": "addendum-a",
        "num": "07",
        "nav": "Project status",
        "title": "Addendum A — Project status",
        "card": "Readiness, partners, and growth path.",
        "group": "addenda",
    },
    {
        "id": "page-8",
        "slug": "addendum-b",
        "num": "08",
        "nav": "Market sources",
        "title": "Addendum B — Market sources",
        "card": "Public URLs behind commercial addressable-pocket counts.",
        "group": "addenda",
    },
]

UI = {
    "site_title": "EyeNet Invest",
    "home": "Home",
    "menu": "Menu",
    "browse": "Browse",
    "search_ph": "Search investor primer…",
    "search_label": "Search wiki",
    "no_match": "No matching pages",
    "pdf": "PDF",
    "pdf_title": "Open printable primer (Save as PDF)",
    "pdf_href": "/print/",
    "prev": "Previous",
    "next": "Next",
    "footer": "EyeNet Vision · Investor primer · Confidential for investor discussion",
    "home_title": "EyeNet Invest",
    "home_lead": (
        "On-premises vision that detects, decides, and acts — distilled from the "
        "value thesis and business plan for investor discussion."
    ),
    "hero_eyebrow": "Edge Vision · Operational Action · Seed Ladder",
    "hero_h1": "EyeNet investor primer",
    "hero_lead": (
        "On-premises vision that detects, decides, and acts — for homes, care, "
        "offices, ships, industrial sites, and venues where cloud cameras cannot follow."
    ),
    "meta": [
        ("Type", "Investor Primer"),
        ("Date", "21 October 2026"),
        ("Structure", "Bet · Wedges · Motions · Seed · Footprint"),
        ("Seed ladder", "$0.5M → $1M → $2.5M"),
    ],
}


def href(path: str) -> str:
    path = path.strip("/")
    return "/" if not path else f"/{path}/"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def strip_section_heads(html: str) -> str:
    return re.sub(r'<div class="section-head">.*?</div>\s*', "", html, flags=re.S)


def extract_cover_and_sections(html: str) -> tuple[str, dict[str, str]]:
    cover_m = re.search(
        r'<section class="cover"[^>]*>(.*?)</section>',
        html,
        flags=re.S,
    )
    cover = cover_m.group(1) if cover_m else ""
    by_id: dict[str, str] = {}
    for m in re.finditer(
        r'<section class="section[^"]*"[^>]*id="(page-\d+)"[^>]*>(.*?)</section>',
        html,
        flags=re.S,
    ):
        by_id[m.group(1)] = strip_section_heads(m.group(2).strip())
    return cover, by_id


def wiki_links(html: str) -> str:
    """Rewrite in-document anchors to wiki routes."""
    html = html.replace('href="#page-7"', 'href="/addendum-a/"')
    html = html.replace('href="#page-8"', 'href="/addendum-b/"')
    for i in range(1, 9):
        html = html.replace(f'href="#ref-{i}"', f'href="/addendum-b/#ref-{i}"')
    return html


def page_label(path: str) -> str:
    path = path.strip("/")
    if not path:
        return UI["home"]
    for sec in SECTIONS:
        if sec["slug"] == path:
            return sec["nav"]
    return path


def pager_html(path: str) -> str:
    path = path.strip("/")
    try:
        idx = PAGE_ORDER.index(path)
    except ValueError:
        return ""
    prev_path = PAGE_ORDER[idx - 1] if idx > 0 else None
    next_path = PAGE_ORDER[idx + 1] if idx + 1 < len(PAGE_ORDER) else None
    prev = (
        f'<a class="pager-link pager-prev" href="{href(prev_path)}" '
        f'aria-label="{UI["prev"]}: {page_label(prev_path)}">'
        f'<span class="pager-dir">{UI["prev"]}</span>'
        f'<span class="pager-title">{page_label(prev_path)}</span></a>'
        if prev_path is not None
        else '<span class="pager-link pager-prev is-empty"></span>'
    )
    nxt = (
        f'<a class="pager-link pager-next" href="{href(next_path)}" '
        f'aria-label="{UI["next"]}: {page_label(next_path)}">'
        f'<span class="pager-dir">{UI["next"]}</span>'
        f'<span class="pager-title">{page_label(next_path)}</span></a>'
        if next_path is not None
        else '<span class="pager-link pager-next is-empty"></span>'
    )
    return f'<nav class="pager" aria-label="Page">{prev}{nxt}</nav>'


def sidebar_html(current: str) -> str:
    def cur(slug: str) -> str:
        return ' aria-current="page"' if current == slug else ""

    primary = [s for s in SECTIONS if s.get("group") != "addenda"]
    addenda = [s for s in SECTIONS if s.get("group") == "addenda"]

    links = [
        f'<a href="/" data-home="true" data-title="{UI["home"]}"{cur("home")}>{UI["home"]}</a>'
    ]
    for sec in primary:
        links.append(
            f'<a href="/{sec["slug"]}/" data-title="{sec["nav"]}"'
            f'{cur(sec["slug"])}>{sec["nav"]}</a>'
        )

    kids = "\n".join(
        f'<a class="nav-child" href="/{sec["slug"]}/" data-title="{sec["nav"]}"'
        f'{cur(sec["slug"])}>{sec["nav"]}</a>'
        for sec in addenda
    )
    links.append(
        f"""
<div class="nav-group is-open" data-nav-group="addenda">
<div class="nav-group-head">
<a class="nav-group-link" href="/addendum-a/" data-title="Addenda"{cur("addendum-a")}>Addenda</a>
<button type="button" class="nav-group-toggle" aria-expanded="true" aria-controls="nav-group-addenda" aria-label="Toggle Addenda">▾</button>
</div>
<div class="nav-group-body" id="nav-group-addenda">
{kids}
</div>
</div>"""
    )
    return "\n".join(links)


def header_nav(section: str) -> str:
    items = [
        ("home", UI["home"], "/"),
        ("the-bet", "The bet", "/the-bet/"),
        ("seed-ladder", "Seed ladder", "/seed-ladder/"),
        ("footprint", "Footprint", "/footprint/"),
    ]
    out = []
    for slug, label, url in items:
        ac = ' aria-current="section"' if section == slug else ""
        out.append(f'<a href="{url}"{ac}>{label}</a>')
    return "".join(out)


def render_page(
    *,
    path: str,
    title: str,
    body: str,
    audience: str,
    section: str | None = None,
    wide: bool = True,
) -> str:
    section = section or audience
    page_title = (
        UI["site_title"]
        if title == UI["site_title"]
        else f'{title} — {UI["site_title"]}'
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title}</title>
  <meta name="description" content="{UI["home_lead"]}">
  <link rel="icon" href="/assets/eyenet-dark.svg?v={ASSET_V}" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
</head>
<body data-lang="en" data-audience="{audience}" data-wide="{"true" if wide else "false"}" data-search-index="/assets/search-index.json?v={ASSET_V}">
  <header class="site-header">
    <div class="site-header-inner">
      <div class="header-nav">
        <button type="button" class="sidebar-toggle" id="sidebarToggle" aria-expanded="false" aria-controls="wikiSidebar">{UI["menu"]}</button>
        <a class="brand" href="/" aria-label="{UI["site_title"]} home">
          <img class="brand-logo" src="/assets/eyenet-dark.svg?v={ASSET_V}" alt="EyeNet">
        </a>
      </div>
      <nav class="header-nav" aria-label="Site sections">{header_nav(section)}
        <a class="pdf-btn" href="{UI["pdf_href"]}" title="{UI["pdf_title"]}">{UI["pdf"]}</a>
      </nav>
    </div>
  </header>
  <div class="sidebar-backdrop" id="sidebarBackdrop"></div>
  <div class="layout">
    <aside class="sidebar" id="wikiSidebar" aria-label="Wiki pages">
      <div class="search-wrap">
        <label class="visually-hidden" for="wikiSearch" style="position:absolute;left:-9999px">{UI["search_label"]}</label>
        <input id="wikiSearch" type="search" placeholder="{UI["search_ph"]}" autocomplete="off" spellcheck="false">
      </div>
      <div class="sidebar-label">{UI["browse"]}</div>
      <nav class="sidebar-nav" id="sidebarNav">
{sidebar_html(audience)}
      </nav>
      <div class="search-empty" id="searchEmpty">{UI["no_match"]}</div>
      <div class="search-hits" id="searchHits"></div>
    </aside>
    <div class="content-wrap">
      <main class="page">
{body}
      </main>
      <footer class="site-footer">
        <div class="site-footer-inner">
          {pager_html(path)}
          <div class="footer-meta">{UI["footer"]}</div>
        </div>
      </footer>
    </div>
  </div>
  <script src="/assets/wiki.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def page_shell_title(num: str, title: str) -> str:
    return (
        f'<div class="section-head">'
        f'<span class="section-num">{num}</span><h1>{title}</h1></div>\n'
    )


def build_print(src_html: str) -> None:
    """Write printable primer under /print/ with deploy-root asset paths."""
    html = src_html
    html = html.replace('src="assets/eyenet-dark.svg"', 'src="/assets/eyenet-dark.svg"')
    html = html.replace(
        'src="../../../product/logos/svg/eyenet-dark.svg"',
        'src="/assets/eyenet-dark.svg"',
    )
    old_tb = re.search(r'<div class="no-print toolbar">.*?</div>\s*', html, flags=re.S)
    toolbar = """  <div class="no-print toolbar">
    <div>
      <p><a href="/">← EyeNet Invest</a> · Printable investor primer</p>
      <p style="margin-top:4px">Use your browser’s Print dialog and choose <strong>Save as PDF</strong>.</p>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
      <button type="button" onclick="window.print()">Print / Save as PDF</button>
    </div>
  </div>
"""
    if old_tb:
        html = html[: old_tb.start()] + toolbar + html[old_tb.end() :]
    write(ROOT / "print" / "index.html", html)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing source primer: {SRC}")
    src_html = SRC.read_text(encoding="utf-8")
    _cover, by_id = extract_cover_and_sections(src_html)
    missing = [s["id"] for s in SECTIONS if s["id"] not in by_id]
    if missing:
        raise SystemExit(f"Missing primer sections: {missing}")

    search: list[dict] = []

    meta = "".join(
        f"<div><span>{k}</span><strong>{v}</strong></div>" for k, v in UI["meta"]
    )
    cards = "".join(
        f'<a class="landing-card" href="/{sec["slug"]}/">'
        f'<span class="num">{sec["num"]}</span>'
        f'<strong>{sec["nav"]}</strong>'
        f'<span>{sec["card"]}</span></a>'
        for sec in SECTIONS
    )
    home_body = f"""
<div class="hero-band">
  <p class="eyebrow">{UI["hero_eyebrow"]}</p>
  <h1>{UI["hero_h1"]}</h1>
  <p class="lead">{UI["hero_lead"]}</p>
  <div class="hero-meta">{meta}</div>
</div>
<p class="lead">{UI["home_lead"]}</p>
<div class="landing-cards">{cards}</div>
"""
    write(
        ROOT / "index.html",
        render_page(
            path="",
            title=UI["home_title"],
            body=home_body,
            audience="home",
            section="home",
        ),
    )
    search.append(
        {
            "lang": "en",
            "url": "/",
            "title": UI["home_title"],
            "section": UI["home"],
            "sectionSlug": "home",
            "text": re.sub(r"<[^>]+>", " ", home_body),
        }
    )

    for sec in SECTIONS:
        body = page_shell_title(sec["num"], sec["title"]) + wiki_links(by_id[sec["id"]])
        write(
            ROOT / sec["slug"] / "index.html",
            render_page(
                path=sec["slug"],
                title=sec["nav"],
                body=body,
                audience=sec["slug"],
                section=sec["slug"],
            ),
        )
        search.append(
            {
                "lang": "en",
                "url": f'/{sec["slug"]}/',
                "title": sec["title"],
                "section": sec["nav"],
                "sectionSlug": sec["slug"],
                "text": re.sub(r"<[^>]+>", " ", body),
            }
        )

    write(ROOT / "assets" / "search-index.json", json.dumps(search, ensure_ascii=False, indent=2))
    print(f"search index entries: {len(search)}")
    build_print(src_html)

    # Keep logo present
    logo = ROOT / "assets" / "eyenet-dark.svg"
    if not logo.exists():
        shutil.copy2(
            Path(__file__).resolve().parents[2] / "value" / "assets" / "eyenet-dark.svg",
            logo,
        )


if __name__ == "__main__":
    main()
