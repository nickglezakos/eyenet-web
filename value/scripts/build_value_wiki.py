#!/usr/bin/env python3
"""Build the bilingual EyeNet Value wiki static site."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_EN = Path(
    "/Users/nickgklezakos/Documents/ppl-meta-code/docs/company/business plan/value/"
    "how-eyenet-changes-the-machine-vision-landscape.html"
)
SRC_EL = Path(
    "/Users/nickgklezakos/Documents/ppl-meta-code/docs/company/business plan/value/"
    "how-eyenet-changes-the-machine-vision-landscape-el.html"
)

ASSET_V = "20261018e"

# Reading order for Previous / Next footer links (path relative to lang root).
PAGE_ORDER = [
    "",
    "competition-breaker",
    "freedom",
    "with-eyenet",
    "what",
    "why",
    "why/home-care",
    "why/hr-presence",
    "why/security",
    "why/cottage",
    "why/shipping",
    "why/mall",
    "packages",
    "packages/b2c",
    "packages/b2b",
    "packages/enterprise",
]


def strip_section_heads(html: str) -> str:
    """Remove duplicate section-head blocks inside body fragments."""
    return re.sub(
        r'<div class="section-head">.*?</div>\s*',
        "",
        html,
        flags=re.S,
    )


def extract_sections(html: str) -> dict[str, str]:
    """Map section numbers to concatenated inner HTML of matching sections."""
    parts = re.findall(
        r'<section class="section[^"]*"[^>]*>(.*?)</section>',
        html,
        flags=re.S,
    )
    buckets: dict[str, list[str]] = {}
    for part in parts:
        m = re.search(r'<span class="section-num">(\d+)</span>', part)
        if not m:
            continue
        num = m.group(1)
        buckets.setdefault(num, []).append(strip_section_heads(part))
    return {k: "\n".join(v) for k, v in buckets.items()}


def fix_asset_paths(html: str) -> str:
    return html.replace('src="assets/', 'src="/assets/images/')


def notify_cards(items: list[tuple[str, str]]) -> str:
    bits = []
    for i, (title, body) in enumerate(items):
        alt = " alt" if i % 2 else ""
        bits.append(
            f'<div class="notify{alt}"><h5>{title}</h5><p>{body}</p></div>'
        )
    return '<div class="breaker-grid">' + "".join(bits) + "</div>"


UI = {
    "en": {
        "site_title": "EyeNet Value",
        "home": "Home",
        "menu": "Menu",
        "browse": "Browse",
        "search_ph": "Search value wiki…",
        "search_label": "Search wiki",
        "no_match": "No matching pages",
        "pdf": "PDF",
        "pdf_title": "Open printable brochure (Save as PDF)",
        "pdf_href": "/print/",
        "prev": "Previous",
        "next": "Next",
        "footer": "EyeNet Vision · Value · Confidential for commercial discussion",
        "sections": {
            "home": "Home",
            "competition-breaker": "Competition breaker",
            "freedom": "Freedom from the feed",
            "with-eyenet": "With EyeNet",
            "what": "What",
            "why": "Why",
            "packages": "Packages",
        },
        "why_children": [
            ("home-care", "Home care · Virtual Ward"),
            ("hr-presence", "HR Presence"),
            ("security", "Security night & perimeter"),
            ("cottage", "Cottage & remote living"),
            ("shipping", "Shipping"),
            ("mall", "Mall marketing studio"),
        ],
        "pkg_children": [
            ("b2c", "B2C Light"),
            ("b2b", "B2B Starter & Professional"),
            ("enterprise", "Enterprise"),
        ],
        "home_title": "EyeNet Value",
        "home_lead": (
            "How EyeNet changes the machine vision landscape — "
            "from passive cameras to on-premises vision that detects, decides, and acts."
        ),
        "hero_eyebrow": "Machine Vision · Edge Intelligence · Operational Action",
        "hero_h1": "How EyeNet changes the machine vision landscape",
        "hero_lead": (
            "From passive cameras to on-premises vision that detects, decides, and acts — "
            "across home care, SME, enterprise, industry, and fleets."
        ),
        "meta": [
            ("Type", "Value Brochure"),
            ("Date", "18 October 2026"),
            ("Structure", "Breaker · Freedom · Intro · What · Why · Packages"),
            ("Deployment", "On-Premises / VPN"),
        ],
        "cards": [
            ("01", "competition-breaker", "Competition breaker",
             "Why EyeNet decides, acts, and stays on premises where competitors cannot follow."),
            ("02", "freedom", "Freedom from the feed",
             "You don’t watch cameras — they watch for you with targeted alerts."),
            ("03", "with-eyenet", "With EyeNet…",
             "Strong outcomes for fleet, care, HR, security, family, and mall operators."),
            ("04", "what", "What",
             "Edge intelligence, action automation, and hardware-bound scale."),
            ("05", "why", "Why",
             "Featured use cases across home care, HR, security, cottage, shipping, and malls."),
            ("06", "packages", "Packages",
             "B2C Light, B2B Starter & Professional, and Enterprise motions."),
        ],
        "page_titles": {
            "competition-breaker": "Why EyeNet is a competition breaker",
            "freedom": "You don’t watch cameras — they watch for you",
            "with-eyenet": "With EyeNet…",
            "what": "What",
            "why": "Why",
            "packages": "Packages — B2C · B2B · Enterprise",
        },
        "why_index_kicker": (
            "Featured use cases — where EyeNet replaces manual presence, "
            "blind nights, and disconnected sites with automatic vision."
        ),
        "pkg_index_kicker": (
            "Dual go-to-market from the business plan: self-serve consumer volume, "
            "mid-market B2B contracts, and enterprise-scale deployments."
        ),
    },
    "el": {
        "site_title": "EyeNet Αξία",
        "home": "Αρχική",
        "menu": "Μενού",
        "browse": "Περιήγηση",
        "search_ph": "Αναζήτηση…",
        "search_label": "Αναζήτηση",
        "no_match": "Δεν βρέθηκαν σελίδες",
        "pdf": "PDF",
        "pdf_title": "Άνοιγμα εκτυπώσιμης έκδοσης (Αποθήκευση ως PDF)",
        "pdf_href": "/el/print/",
        "prev": "Προηγούμενο",
        "next": "Επόμενο",
        "footer": "EyeNet Vision · Αξία · Εμπιστευτικό για εμπορική συζήτηση",
        "sections": {
            "home": "Αρχική",
            "competition-breaker": "Σπάσιμο ανταγωνισμού",
            "freedom": "Ελευθερία από το feed",
            "with-eyenet": "Με το EyeNet",
            "what": "Τι",
            "why": "Γιατί",
            "packages": "Πακέτα",
        },
        "why_children": [
            ("home-care", "Home care · Virtual Ward"),
            ("hr-presence", "HR Presence"),
            ("security", "Ασφάλεια νύχτα & περίμετρος"),
            ("cottage", "Εξοχικό & απομακρυσμένη διαβίωση"),
            ("shipping", "Ναυτιλία"),
            ("mall", "Mall marketing studio"),
        ],
        "pkg_children": [
            ("b2c", "B2C Light"),
            ("b2b", "B2B Starter & Professional"),
            ("enterprise", "Enterprise"),
        ],
        "home_title": "EyeNet Αξία",
        "home_lead": (
            "Πώς το EyeNet αλλάζει το τοπίο του machine vision — "
            "από παθητικές κάμερες σε on-premises όραση που ανιχνεύει, αποφασίζει και ενεργεί."
        ),
        "hero_eyebrow": "Machine Vision · Edge Intelligence · Λειτουργική δράση",
        "hero_h1": "Πώς το EyeNet αλλάζει το τοπίο του machine vision",
        "hero_lead": (
            "Από παθητικές κάμερες σε on-premises όραση που ανιχνεύει, αποφασίζει και ενεργεί — "
            "σε home care, SME, enterprise, βιομηχανία και στόλους."
        ),
        "meta": [
            ("Τύπος", "Value Brochure"),
            ("Ημερομηνία", "18 Οκτωβρίου 2026"),
            ("Δομή", "Breaker · Ελευθερία · Intro · Τι · Γιατί · Πακέτα"),
            ("Ανάπτυξη", "On-Premises / VPN"),
        ],
        "cards": [
            ("01", "competition-breaker", "Σπάσιμο ανταγωνισμού",
             "Γιατί το EyeNet αποφασίζει, ενεργεί και μένει στις εγκαταστάσεις σας."),
            ("02", "freedom", "Ελευθερία από το feed",
             "Δεν κοιτάτε κάμερες — αυτές κοιτάνε για εσάς με στοχευμένα alerts."),
            ("03", "with-eyenet", "Με το EyeNet…",
             "Δυνατά αποτελέσματα για στόλο, φροντίδα, HR, ασφάλεια, οικογένεια και mall."),
            ("04", "what", "Τι",
             "Edge νοημοσύνη, αυτοματοποίηση δράσης και κλίμακα με βάση το hardware."),
            ("05", "why", "Γιατί",
             "Επιλεγμένες περιπτώσεις χρήσης σε home care, HR, ασφάλεια, εξοχικό, ναυτιλία και mall."),
            ("06", "packages", "Πακέτα",
             "B2C Light, B2B Starter & Professional και Enterprise."),
        ],
        "page_titles": {
            "competition-breaker": "Γιατί το EyeNet σπάει τον ανταγωνισμό",
            "freedom": "Δεν κοιτάτε κάμερες — αυτές κοιτάνε για εσάς",
            "with-eyenet": "Με το EyeNet…",
            "what": "Τι",
            "why": "Γιατί",
            "packages": "Πακέτα — B2C · B2B · Enterprise",
        },
        "why_index_kicker": (
            "Επιλεγμένες περιπτώσεις χρήσης — όπου το EyeNet αντικαθιστά χειροκίνητη παρουσία, "
            "τυφλές νύχτες και αποσυνδεδεμένους χώρους με αυτόματη όραση."
        ),
        "pkg_index_kicker": (
            "Διπλό go-to-market από το business plan: self-serve καταναλωτικός όγκος, "
            "mid-market B2B συμβόλαια και enterprise κλίμακα."
        ),
    },
}


def prefix(lang: str) -> str:
    return "/el" if lang == "el" else ""


def href(lang: str, path: str) -> str:
    path = path.strip("/")
    base = prefix(lang)
    if not path:
        return f"{base}/" if base else "/"
    return f"{base}/{path}/"


def alt_lang_url(lang: str, path: str) -> str:
    other = "el" if lang == "en" else "en"
    return href(other, path)


def sidebar_html(lang: str, current: str) -> str:
    ui = UI[lang]
    p = prefix(lang)
    sections = ui["sections"]

    def cur(slug: str) -> str:
        return ' aria-current="page"' if current == slug else ""

    def group(slug: str, children: list[tuple[str, str]], label: str) -> str:
        open_cls = " is-open"
        kids = "\n".join(
            f'<a class="nav-child" href="{p}/{slug}/{child}/" data-title="{title}"'
            f'{cur(f"{slug}/{child}")}>{title}</a>'
            for child, title in children
        )
        return f"""
<div class="nav-group{open_cls}" data-nav-group="{slug}">
<div class="nav-group-head">
<a class="nav-group-link" href="{p}/{slug}/" data-title="{label}"{cur(slug)}>{label}</a>
<button type="button" class="nav-group-toggle" aria-expanded="true" aria-controls="nav-group-{slug}" aria-label="Toggle {label}">▾</button>
</div>
<div class="nav-group-body" id="nav-group-{slug}">
{kids}
</div>
</div>"""

    home = f"{p}/" if p else "/"
    links = [
        f'<a href="{home}" data-home="true" data-title="{sections["home"]}"{cur("home")}>{sections["home"]}</a>',
        f'<a href="{p}/competition-breaker/" data-title="{sections["competition-breaker"]}"{cur("competition-breaker")}>{sections["competition-breaker"]}</a>',
        f'<a href="{p}/freedom/" data-title="{sections["freedom"]}"{cur("freedom")}>{sections["freedom"]}</a>',
        f'<a href="{p}/with-eyenet/" data-title="{sections["with-eyenet"]}"{cur("with-eyenet")}>{sections["with-eyenet"]}</a>',
        f'<a href="{p}/what/" data-title="{sections["what"]}"{cur("what")}>{sections["what"]}</a>',
        group("why", ui["why_children"], sections["why"]),
        group("packages", ui["pkg_children"], sections["packages"]),
    ]
    return "\n".join(links)


def header_nav(lang: str, section: str) -> str:
    ui = UI[lang]
    p = prefix(lang)
    items = [
        ("home", ui["home"], f"{p}/" if p else "/"),
        ("competition-breaker", ui["sections"]["competition-breaker"], f"{p}/competition-breaker/"),
        ("why", ui["sections"]["why"], f"{p}/why/"),
        ("packages", ui["sections"]["packages"], f"{p}/packages/"),
    ]
    out = []
    for slug, label, url in items:
        ac = ' aria-current="section"' if section == slug or (slug != "home" and section.startswith(slug)) else ""
        if slug == "home" and section == "home":
            ac = ' aria-current="section"'
        out.append(f'<a href="{url}"{ac}>{label}</a>')
    return "".join(out)


def page_label(lang: str, path: str) -> str:
    ui = UI[lang]
    path = path.strip("/")
    if not path:
        return ui["home"]
    if path in ui["sections"]:
        return ui["sections"][path]
    if path.startswith("why/"):
        child = path.split("/", 1)[1]
        for slug, label in ui["why_children"]:
            if slug == child:
                return label
    if path.startswith("packages/"):
        child = path.split("/", 1)[1]
        for slug, label in ui["pkg_children"]:
            if slug == child:
                return label
    return path


def pager_html(lang: str, path: str) -> str:
    ui = UI[lang]
    path = path.strip("/")
    try:
        idx = PAGE_ORDER.index(path)
    except ValueError:
        return ""
    prev_path = PAGE_ORDER[idx - 1] if idx > 0 else None
    next_path = PAGE_ORDER[idx + 1] if idx + 1 < len(PAGE_ORDER) else None
    prev = (
        f'<a class="pager-link pager-prev" href="{href(lang, prev_path)}">'
        f'<span class="pager-dir">{ui["prev"]}</span>'
        f'<span class="pager-title">{page_label(lang, prev_path)}</span></a>'
        if prev_path is not None
        else '<span class="pager-link pager-prev is-empty"></span>'
    )
    nxt = (
        f'<a class="pager-link pager-next" href="{href(lang, next_path)}">'
        f'<span class="pager-dir">{ui["next"]}</span>'
        f'<span class="pager-title">{page_label(lang, next_path)}</span></a>'
        if next_path is not None
        else '<span class="pager-link pager-next is-empty"></span>'
    )
    return f'<nav class="pager" aria-label="Page">{prev}{nxt}</nav>'


def render_page(
    *,
    lang: str,
    path: str,
    title: str,
    body: str,
    audience: str,
    wide: bool = False,
    section: str | None = None,
) -> str:
    ui = UI[lang]
    section = section or audience
    p = prefix(lang)
    en_url = href("en", path)
    el_url = href("el", path)
    html_lang = "el" if lang == "el" else "en"
    home_href = f"{p}/" if p else "/"
    pager = pager_html(lang, path)
    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title if title != ui["site_title"] else ui["site_title"]}{" — " + ui["site_title"] if title != ui["site_title"] else ""}</title>
  <meta name="description" content="{ui["home_lead"]}">
  <link rel="icon" href="/assets/eyenet-dark.svg?v={ASSET_V}" type="image/svg+xml">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="el" href="{el_url}">
  <link rel="alternate" hreflang="x-default" href="{href("en", path)}">
  <link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
</head>
<body data-lang="{lang}" data-audience="{audience}" data-wide="{"true" if wide else "false"}" data-search-index="/assets/search-index.json?v={ASSET_V}">
  <header class="site-header">
    <div class="site-header-inner">
      <div class="header-nav">
        <button type="button" class="sidebar-toggle" id="sidebarToggle" aria-expanded="false" aria-controls="wikiSidebar">{ui["menu"]}</button>
        <a class="brand" href="{home_href}" aria-label="{ui["site_title"]} home">
          <img class="brand-logo" src="/assets/eyenet-dark.svg?v={ASSET_V}" alt="EyeNet">
        </a>
      </div>
      <nav class="header-nav" aria-label="Site sections">{header_nav(lang, section)}
        <a class="pdf-btn" href="{ui["pdf_href"]}" title="{ui["pdf_title"]}">{ui["pdf"]}</a>
        <div class="lang-switch" aria-label="Language">
          <a href="{en_url}"{" aria-current=\"true\"" if lang == "en" else ""}>EN</a>
          <a href="{el_url}"{" aria-current=\"true\"" if lang == "el" else ""}>EL</a>
        </div>
      </nav>
    </div>
  </header>
  <div class="sidebar-backdrop" id="sidebarBackdrop"></div>
  <div class="layout">
    <aside class="sidebar" id="wikiSidebar" aria-label="Wiki pages">
      <div class="search-wrap">
        <label class="visually-hidden" for="wikiSearch" style="position:absolute;left:-9999px">{ui["search_label"]}</label>
        <input id="wikiSearch" type="search" placeholder="{ui["search_ph"]}" autocomplete="off" spellcheck="false">
      </div>
      <div class="sidebar-label">{ui["browse"]}</div>
      <nav class="sidebar-nav" id="sidebarNav">
{sidebar_html(lang, audience)}
      </nav>
      <div class="search-empty" id="searchEmpty">{ui["no_match"]}</div>
      <div class="search-hits" id="searchHits"></div>
    </aside>
    <div class="content-wrap">
      <main class="page">
{body}
      </main>
      <footer class="site-footer">
        <div class="site-footer-inner">
          {pager}
          <div class="footer-meta">{ui["footer"]}</div>
        </div>
      </footer>
    </div>
  </div>
  <script src="/assets/wiki.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def split_personas(section_html: str) -> list[str]:
    return re.findall(r'(<div class="persona[^"]*">.*?</div>\s*</div>\s*</div>)', section_html, flags=re.S)


def split_packages(section_html: str) -> list[str]:
    return re.findall(r'(<div class="persona[^"]*">.*?(?:</div>\s*){3})', section_html, flags=re.S)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def page_shell_title(lang: str, num: str, title: str) -> str:
    return f'<div class="section-head"><span class="section-num">{num}</span><h1>{title}</h1></div>'


def build_lang(lang: str, sections: dict[str, str], search_entries: list[dict]) -> None:
    ui = UI[lang]
    base = ROOT / ("el" if lang == "el" else "")
    pfx = prefix(lang)

    # Home
    meta = "".join(
        f"<div><span>{k}</span><strong>{v}</strong></div>" for k, v in ui["meta"]
    )
    cards = "".join(
        f'<a class="landing-card" href="{pfx}/{slug}/">'
        f'<span class="num">{num}</span><strong>{title}</strong><span>{desc}</span></a>'
        for num, slug, title, desc in ui["cards"]
    )
    home_body = f"""
<div class="hero-band">
  <p class="eyebrow">{ui["hero_eyebrow"]}</p>
  <h1>{ui["hero_h1"]}</h1>
  <p class="lead">{ui["hero_lead"]}</p>
  <div class="hero-meta">{meta}</div>
</div>
<p class="lead">{ui["home_lead"]}</p>
<div class="landing-cards">{cards}</div>
"""
    write(
        base / "index.html",
        render_page(
            lang=lang,
            path="",
            title=ui["home_title"],
            body=home_body,
            audience="home",
            section="home",
            wide=True,
        ),
    )
    search_entries.append(
        {
            "lang": lang,
            "url": f"{pfx}/" if pfx else "/",
            "title": ui["home_title"],
            "section": ui["sections"]["home"],
            "sectionSlug": "home",
            "text": re.sub(r"<[^>]+>", " ", home_body),
        }
    )

    mapping = [
        ("01", "competition-breaker", True),
        ("02", "freedom", False),
        ("03", "with-eyenet", True),
        ("04", "what", False),
    ]
    for num, slug, wide in mapping:
        title = ui["page_titles"][slug]
        body = page_shell_title(lang, num, title) + fix_asset_paths(sections[num])
        write(
            base / slug / "index.html",
            render_page(
                lang=lang,
                path=slug,
                title=title,
                body=body,
                audience=slug,
                section=slug,
                wide=wide,
            ),
        )
        search_entries.append(
            {
                "lang": lang,
                "url": f"{pfx}/{slug}/",
                "title": title,
                "section": ui["sections"][slug],
                "sectionSlug": slug,
                "text": re.sub(r"<[^>]+>", " ", body),
            }
        )

    # Why index + children
    personas = split_personas(sections["05"])
    why_cards = "".join(
        f'<a class="landing-card" href="{pfx}/why/{child}/">'
        f'<span class="num">{i+1:02d}</span><strong>{label}</strong>'
        f"<span>{ui['why_index_kicker']}</span></a>"
        for i, (child, label) in enumerate(ui["why_children"])
    )
    # keep summary panel from section if present
    summary = ""
    sm = re.search(r'(<div class="panel summary-panel">.*?</div>)', sections["05"], flags=re.S)
    if sm:
        summary = sm.group(1)
    why_body = (
        page_shell_title(lang, "05", ui["page_titles"]["why"])
        + f'<div class="kicker">{ui["why_index_kicker"]}</div>'
        + f'<div class="landing-cards">{why_cards}</div>'
        + summary
    )
    write(
        base / "why" / "index.html",
        render_page(
            lang=lang,
            path="why",
            title=ui["page_titles"]["why"],
            body=why_body,
            audience="why",
            section="why",
            wide=True,
        ),
    )
    search_entries.append(
        {
            "lang": lang,
            "url": f"{pfx}/why/",
            "title": ui["page_titles"]["why"],
            "section": ui["sections"]["why"],
            "sectionSlug": "why",
            "text": re.sub(r"<[^>]+>", " ", why_body),
        }
    )

    for i, ((child, label), persona_html) in enumerate(zip(ui["why_children"], personas)):
        body = (
            page_shell_title(lang, "05", label)
            + fix_asset_paths(persona_html)
        )
        write(
            base / "why" / child / "index.html",
            render_page(
                lang=lang,
                path=f"why/{child}",
                title=label,
                body=body,
                audience=f"why/{child}",
                section="why",
                wide=True,
            ),
        )
        search_entries.append(
            {
                "lang": lang,
                "url": f"{pfx}/why/{child}/",
                "title": label,
                "section": ui["sections"]["why"],
                "sectionSlug": "why",
                "text": re.sub(r"<[^>]+>", " ", body),
            }
        )

    # Packages
    packages = split_packages(sections["06"])
    # Prefer first 3 persona blocks
    if len(packages) < 3:
        # fallback: greedy persona match
        packages = re.findall(
            r'<div class="persona.*?(?=<div class="persona|<div class="panel summary-panel"|$)',
            sections["06"],
            flags=re.S,
        )
        packages = [p.rstrip() + ("</div>" if not p.rstrip().endswith("</div>") else "") for p in packages]

    pkg_cards = "".join(
        f'<a class="landing-card" href="{pfx}/packages/{child}/">'
        f'<span class="num">{i+1:02d}</span><strong>{label}</strong>'
        f"<span>{ui['pkg_index_kicker']}</span></a>"
        for i, (child, label) in enumerate(ui["pkg_children"])
    )
    pkg_summary = ""
    sm = re.search(r'(<div class="panel summary-panel">.*?</div>)', sections["06"], flags=re.S)
    if sm:
        pkg_summary = sm.group(1)
    footer_note = ""
    fn = re.search(r'(<p class="footer-note">.*?</p>)', sections["06"], flags=re.S)
    if fn:
        footer_note = fn.group(1)

    pkg_body = (
        page_shell_title(lang, "06", ui["page_titles"]["packages"])
        + f'<div class="kicker">{ui["pkg_index_kicker"]}</div>'
        + f'<div class="landing-cards">{pkg_cards}</div>'
        + pkg_summary
        + footer_note
    )
    write(
        base / "packages" / "index.html",
        render_page(
            lang=lang,
            path="packages",
            title=ui["page_titles"]["packages"],
            body=pkg_body,
            audience="packages",
            section="packages",
            wide=True,
        ),
    )
    search_entries.append(
        {
            "lang": lang,
            "url": f"{pfx}/packages/",
            "title": ui["page_titles"]["packages"],
            "section": ui["sections"]["packages"],
            "sectionSlug": "packages",
            "text": re.sub(r"<[^>]+>", " ", pkg_body),
        }
    )

    # Extract package personas more reliably
    pkg_blocks = re.findall(
        r'(<div class="persona(?: alt)?">\s*<h4>.*?)(?=<div class="persona|<div class="panel summary-panel"|<p class="footer-note"|$)',
        sections["06"],
        flags=re.S,
    )
    pkg_blocks = [b.strip() for b in pkg_blocks]
    if len(pkg_blocks) < 3:
        raise SystemExit(f"Expected 3 package blocks for {lang}, got {len(pkg_blocks)}")

    for (child, label), block in zip(ui["pkg_children"], pkg_blocks[:3]):
        body = page_shell_title(lang, "06", label) + fix_asset_paths(block)
        write(
            base / "packages" / child / "index.html",
            render_page(
                lang=lang,
                path=f"packages/{child}",
                title=label,
                body=body,
                audience=f"packages/{child}",
                section="packages",
                wide=True,
            ),
        )
        search_entries.append(
            {
                "lang": lang,
                "url": f"{pfx}/packages/{child}/",
                "title": label,
                "section": ui["sections"]["packages"],
                "sectionSlug": "packages",
                "text": re.sub(r"<[^>]+>", " ", body),
            }
        )


def main() -> None:
    en_sections = extract_sections(SRC_EN.read_text(encoding="utf-8"))
    el_sections = extract_sections(SRC_EL.read_text(encoding="utf-8"))
    for key in ("01", "02", "03", "04", "05", "06"):
        if key not in en_sections or key not in el_sections:
            raise SystemExit(f"Missing section {key}")

    # Fix why persona split: use dedicated regex on full section
    def personas(section: str) -> list[str]:
        blocks = re.findall(
            r'(<div class="persona(?: alt)?">\s*<h4>.*?)(?=<div class="persona|<div class="panel summary-panel"|$)',
            section,
            flags=re.S,
        )
        return [b.strip() for b in blocks]

    # monkeypatch split for why by storing on sections dict as side channel
    global split_personas
    en_personas = personas(en_sections["05"])
    el_personas = personas(el_sections["05"])
    if len(en_personas) != 6 or len(el_personas) != 6:
        raise SystemExit(f"Expected 6 personas, got EN={len(en_personas)} EL={len(el_personas)}")

    def split_personas_fixed(section_html: str) -> list[str]:
        return personas(section_html)

    globals()["split_personas"] = split_personas_fixed

    search: list[dict] = []
    build_lang("en", en_sections, search)
    build_lang("el", el_sections, search)

    # clean text
    for e in search:
        e["text"] = re.sub(r"\s+", " ", e["text"]).strip()

    write(ROOT / "assets" / "search-index.json", json.dumps(search, ensure_ascii=False, indent=2))
    print(f"search index entries: {len(search)}")


if __name__ == "__main__":
    main()
