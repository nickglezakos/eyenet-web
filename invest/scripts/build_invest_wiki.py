#!/usr/bin/env python3
"""Build the English EyeNet Investor Primer wiki (value-wiki UX, EN only)."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "eyenet-investor-primer.html"
ASSET_V = "20261023d"

PAGE_ORDER = [
    "",
    "the-bet",
    "what-changes",
    "where-it-pays",
    "how-it-is-sold",
    "seed-ladder",
    "footprint",
    "market-validation",
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
        "id": None,
        "slug": "market-validation",
        "num": "07",
        "nav": "Market validation",
        "title": "Market validation",
        "card": "FootfallCam proves paid people-analytics demand — without covering EyeNet’s six wedges.",
        "content": "market-validation.html",
    },
    {
        "id": "page-7",
        "slug": "addendum-a",
        "num": "08",
        "nav": "Project status",
        "title": "Project status",
        "card": "Readiness, partners, and growth path.",
    },
    {
        "id": "page-8",
        "slug": "addendum-b",
        "num": "09",
        "nav": "Reference",
        "title": "Addendum — Reference",
        "card": "Sources for addressable pockets and market validation.",
        "group": "addenda",
        "append": "reference-market-validation.html",
        "kicker_override": (
            "Public references for How it is sold (addressable pockets) and for "
            "Market validation (FootfallCam). Enterprise segment dollars are EyeNet "
            "plan targets, not external census counts."
        ),
        "title_override": "Addendum — Reference",
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
        ("Structure", "Bet · Wedges · Motions · Seed · Footprint · Validation"),
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


def strip_existing_kicker(html: str) -> str:
    return re.sub(r'<div class="kicker">.*?</div>\s*', "", html, count=1, flags=re.S)


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

    if addenda:
        first_add = addenda[0]["slug"]
        kids = "\n".join(
            f'<a class="nav-child" href="/{sec["slug"]}/" data-title="{sec["nav"]}"'
            f'{cur(sec["slug"])}>{sec["nav"]}</a>'
            for sec in addenda
        )
        links.append(
            f"""
<div class="nav-group is-open" data-nav-group="addenda">
<div class="nav-group-head">
<a class="nav-group-link" href="/{first_add}/" data-title="Addenda"{cur(first_add)}>Addenda</a>
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
        ("market-validation", "Market validation", "/market-validation/"),
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


PRINT_EXTRA_CSS = """
    /* market-validation print extras */
    .persona {
      background: var(--band);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 14px 16px;
      margin: 0;
    }
    .persona.alt { background: var(--band-alt); }
    .persona h4 {
      margin: 0 0 6px;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .persona .n {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: var(--brand-dark);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
    }
    .persona .who {
      margin: 0 0 8px;
      color: var(--muted);
      font-size: 12px;
    }
    .persona ul { margin: 0; padding-left: 1.1em; color: var(--muted); font-size: 12px; }
    .intro-kickers { display: grid; gap: 12px; margin: 14px 0; }
    @media (min-width: 700px) {
      .intro-kickers.cols-3 { grid-template-columns: repeat(3, 1fr); }
    }
    .breaker-vs { display: grid; gap: 12px; }
    @media (min-width: 700px) {
      .breaker-vs.cols-2 { grid-template-columns: 1fr 1fr; }
    }
    .ffc-charts { display: grid; gap: 12px; margin: 12px 0 16px; }
    @media (min-width: 700px) {
      .ffc-charts { grid-template-columns: 1fr 1fr; }
    }
    .chart-block {
      background: var(--band);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 12px 14px;
    }
    .chart-block h4 { margin: 0 0 10px; font-size: 12px; }
    .bar-chart { display: flex; flex-direction: column; gap: 6px; }
    .bar-row {
      display: grid;
      grid-template-columns: 2.4rem 1fr 3.2rem;
      gap: 6px;
      align-items: center;
    }
    .bar-label { font-size: 10px; font-weight: 700; color: var(--muted); }
    .bar-track {
      height: 12px;
      background: rgba(15, 40, 70, 0.08);
      border-radius: 999px;
      overflow: hidden;
    }
    .bar-fill {
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--brand-dark), var(--brand));
      min-width: 2px;
    }
    .bar-fill.is-peak { background: linear-gradient(90deg, #0b6e4f, #1faa6e); }
    .bar-fill.is-dip { background: linear-gradient(90deg, #9a3412, #ea580c); }
    .bar-chart-accent .bar-fill { background: linear-gradient(90deg, #1e3a5f, #3b82c4); }
    .bar-chart-accent .bar-fill.is-peak { background: linear-gradient(90deg, #0b6e4f, #1faa6e); }
    .bar-value { font-size: 10px; font-weight: 700; text-align: right; }
    .ffc-geo { margin: 8px 0 14px; }
    .ffc-geo-track {
      display: flex;
      height: 28px;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--line);
    }
    .ffc-geo-uk, .ffc-geo-abroad {
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 11px;
      font-weight: 700;
    }
    .ffc-geo-uk { background: var(--brand-dark); }
    .ffc-geo-abroad { background: linear-gradient(90deg, var(--brand), #3b82c4); }
    .ffc-geo-caption { margin: 6px 0 0; font-size: 11px; color: var(--muted); }
"""


def build_print(src_html: str) -> None:
    """Write printable primer under /print/ with Market validation + current numbering."""
    html = src_html
    html = html.replace('src="assets/eyenet-dark.svg"', 'src="/assets/eyenet-dark.svg"')
    html = html.replace(
        'src="../../../product/logos/svg/eyenet-dark.svg"',
        'src="/assets/eyenet-dark.svg"',
    )

    if "/* market-validation print extras */" not in html:
        html = html.replace("  </style>", PRINT_EXTRA_CSS + "\n  </style>")

    mv_body = (ROOT / "content" / "market-validation.html").read_text(encoding="utf-8")
    mv_body = mv_body.replace(
        'href="/addendum-b/#market-validation-refs"',
        'href="#market-validation-refs"',
    )
    mv_section = f"""
    <section class="section flow page-start" id="page-mv" data-nav-label="07 · Market validation">
      <div class="section-head"><span class="section-num">07</span><h2>Market validation</h2></div>
{mv_body}
    </section>
"""
    if 'id="page-mv"' not in html:
        html = html.replace(
            "    <!-- 07 ADDENDUM A — PROJECT STATUS -->",
            mv_section + "\n    <!-- 08 PROJECT STATUS -->",
        )

    html = html.replace(
        'id="page-7" data-nav-label="07 · Addendum A"',
        'id="page-7" data-nav-label="08 · Project status"',
    )
    html = html.replace(
        '<span class="section-num">07</span><h2>Addendum A — Project status</h2>',
        '<span class="section-num">08</span><h2>Project status</h2>',
    )
    html = html.replace(
        'id="page-8" data-nav-label="08 · Addendum B"',
        'id="page-8" data-nav-label="09 · Reference"',
    )
    html = html.replace(
        '<span class="section-num">08</span><h2>Addendum B — Market sources (commercial packages)</h2>',
        '<span class="section-num">09</span><h2>Addendum — Reference</h2>',
    )
    html = html.replace(
        '<div class="kicker">Public references used for addressable pockets in How it is sold (B2C Light and B2B Starter / Pro). Same links as the value site commercial packages. Enterprise segment dollars are EyeNet plan targets, not external census counts.</div>',
        '<div class="kicker">Public references for How it is sold (addressable pockets) and for Market validation (FootfallCam). Enterprise segment dollars are EyeNet plan targets, not external census counts.</div>',
    )

    ref_extra = (ROOT / "content" / "reference-market-validation.html").read_text(
        encoding="utf-8"
    )
    if 'id="market-validation-refs"' not in html:
        html = html.replace(
            '      <p class="side-note">Cited from value site commercial packages',
            ref_extra
            + '\n      <p class="side-note">Cited from value site commercial packages',
        )

    html = html.replace(
        "Project status: <a href=\"#page-7\">Addendum A</a>. Commercial addressable-pocket links: <a href=\"#page-8\">Addendum B</a>.",
        'Market validation: <a href="#page-mv">§07</a>. Project status: <a href="#page-7">§08</a>. Reference: <a href="#page-8">§09</a>.',
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
    missing = [s["id"] for s in SECTIONS if s.get("id") and s["id"] not in by_id]
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
        page_title = sec.get("title_override") or sec["title"]
        if sec.get("content"):
            frag = (ROOT / "content" / sec["content"]).read_text(encoding="utf-8")
            body = page_shell_title(sec["num"], page_title) + frag
        else:
            body = page_shell_title(sec["num"], page_title) + wiki_links(
                by_id[sec["id"]]
            )
            if sec.get("kicker_override"):
                body = (
                    page_shell_title(sec["num"], page_title)
                    + f'<div class="kicker">{sec["kicker_override"]}</div>\n'
                    + strip_existing_kicker(wiki_links(by_id[sec["id"]]))
                )
            if sec.get("append"):
                body += (ROOT / "content" / sec["append"]).read_text(encoding="utf-8")
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
