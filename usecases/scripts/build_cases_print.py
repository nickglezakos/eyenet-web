#!/usr/bin/env python3
"""Build a print-only EN/EL site with only Most Valuable Cases from value/print."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VALUE = REPO / "value"
OUT = REPO / "usecases"

SRC = {
    "en": VALUE / "print" / "index.html",
    "el": VALUE / "el" / "print" / "index.html",
}

CASE_ORDER_EN = [
    "page-8",   # HR Presence
    "page-12",  # Mall / screens
    "page-13",  # Shop floor
    "page-10",  # Cottage / family
    "page-7",   # Home care
    "page-9",   # Security
    "page-11",  # Shipping
]

# Greek print keeps the same section ids as EN for these cases.
CASE_ORDER_EL = CASE_ORDER_EN

META = {
    "en": {
        "title": "Most Valuable Cases — EyeNet",
        "cover_chip": "Most Valuable Cases",
        "cover_eyebrow": "Machine Vision · Edge Intelligence · Operational Action",
        "cover_h1": "Most Valuable Cases",
        "cover_lead": "",
        "meta": [
            ("Type", "Cases Brochure"),
            ("Date", "2 November 2026"),
            ("Structure", "Seven featured cases"),
            ("Deployment", "On-Premises / VPN"),
        ],
        "home_num": "00",
        "home_h2": "Most Valuable Cases",
        "home_lead": (
            "Featured use cases across HR, signage, shop floor, family protection, "
            "home care, security, shipping, and industrial sites."
        ),
        "toolbar_back": "",
        "toolbar_note": "Use your browser’s Print dialog and choose <strong>Save as PDF</strong>.",
        "toolbar_other": ("EL version", "/el/"),
        "print_btn": "Print / Save as PDF",
        "nav_prev": "← Previous",
        "nav_next": "Next →",
        "cover_nav": "Cover",
        "toc_nav": "Contents",
        "footer_left": "eyenet-vision.com",
        "footer_right": "nick@eyenet-vision.com",
    },
    "el": {
        "title": "Ενδεικτικές περιπτώσεις χρήσης — EyeNet",
        "cover_chip": "Ενδεικτικές περιπτώσεις χρήσης",
        "cover_eyebrow": "Μηχανική όραση · Edge Intelligence · Επιχειρησιακή δράση",
        "cover_h1": "Ενδεικτικές περιπτώσεις χρήσης",
        "cover_lead": "",
        "meta": [
            ("Τύπος", "Brochure περιπτώσεων"),
            ("Ημερομηνία", "2 Νοεμβρίου 2026"),
            ("Δομή", "Επτά επιλεγμένες περιπτώσεις"),
            ("Ανάπτυξη", "On-Premises / VPN"),
        ],
        "home_num": "00",
        "home_h2": "Ενδεικτικές περιπτώσεις χρήσης",
        "home_lead": (
            "Επιλεγμένες περιπτώσεις σε HR, ψηφιακή σήμανση, χώρο πώλησης, οικογενειακή προστασία, "
            "κατ’ οίκον φροντίδα, ασφάλεια, ναυτιλία και βιομηχανικές εγκαταστάσεις."
        ),
        "toolbar_back": "",
        "toolbar_note": "Χρησιμοποιήστε Print και επιλέξτε <strong>Save as PDF</strong>.",
        "toolbar_other": ("EN version", "/"),
        "print_btn": "Εκτύπωση / Αποθήκευση PDF",
        "nav_prev": "← Προηγούμενο",
        "nav_next": "Επόμενο →",
        "cover_nav": "Εξώφυλλο",
        "toc_nav": "Περιεχόμενα",
        "footer_left": "eyenet-vision.com",
        "footer_right": "nick@eyenet-vision.com",
    },
}


def extract_head_styles(html: str) -> str:
    m = re.search(r"(<style>.*?</style>)", html, flags=re.S)
    if not m:
        raise SystemExit("No <style> block in source print page")
    return m.group(1)


def extract_sections(html: str) -> dict[str, str]:
    """Return id -> full <section>...</section> including attributes."""
    sections: dict[str, str] = {}
    for m in re.finditer(
        r'(<section\b[^>]*\bid="([^"]+)"[^>]*>)(.*?)(</section>)',
        html,
        flags=re.S,
    ):
        open_tag, sid, body, close = m.group(1), m.group(2), m.group(3), m.group(4)
        sections[sid] = open_tag + body + close
    return sections


def persona_title(section_html: str) -> str | None:
    m = re.search(
        r'<h4>\s*<span class="n">\d+</span>\s*(.*?)</h4>',
        section_html,
        flags=re.S,
    )
    if not m:
        return None
    title = re.sub(r"<[^>]+>", "", m.group(1))
    return re.sub(r"\s+", " ", title).strip()


def set_nav_label(section_html: str, label: str) -> str:
    return re.sub(
        r'data-nav-label="[^"]*"',
        f'data-nav-label="{label}"',
        section_html,
        count=1,
    )


def set_section_num(section_html: str, num: str) -> str:
    return re.sub(
        r'(<span class="section-num">)\d+(</span>)',
        rf"\g<1>{num}\g<2>",
        section_html,
        count=1,
    )


def rewrite_section_h2(section_html: str, title: str) -> str:
    return re.sub(
        r"(<div class=\"section-head\">\s*<span class=\"section-num\">\d+</span><h2>)(.*?)(</h2>)",
        rf"\1{title}\3",
        section_html,
        count=1,
        flags=re.S,
    )


def collect_assets(html: str) -> set[str]:
    return set(re.findall(r'(?:src|href)="(/assets/[^"]+)"', html))


def copy_assets(paths: set[str]) -> None:
    for rel in sorted(paths):
        src = VALUE / rel.lstrip("/")
        dst = OUT / rel.lstrip("/")
        if not src.exists():
            # Try without leading assets duplication
            alt = VALUE / "assets" / Path(rel).name
            if alt.exists():
                src = alt
            else:
                print(f"WARN missing asset: {rel}")
                continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def cover_html(ui: dict) -> str:
    meta = "".join(
        f"<div><span>{k}</span><strong>{v}</strong></div>" for k, v in ui["meta"]
    )
    return f"""    <section class="cover" id="page-0" data-nav-label="{ui['cover_nav']}">
      <div>
        <div class="cover-top">
          <div class="cover-brand">
            <img src="/assets/eyenet-dark.svg" alt="EyeNet" />
            <span class="cover-chip">{ui['cover_chip']}</span>
          </div>
        </div>
        <p class="cover-eyebrow">{ui['cover_eyebrow']}</p>
        <h1>{ui['cover_h1']}</h1>
        {f'<p class="cover-lead">{ui["cover_lead"]}</p>' if ui.get("cover_lead") else ""}
        <div class="cover-meta">
          {meta}
        </div>
      </div>
      <div class="cover-foot">
        <span>{ui['footer_left']}</span>
        <span>{ui['footer_right']}</span>
      </div>
    </section>"""


def toc_html(ui: dict, case_cards: list[tuple[str, str, str]]) -> str:
    """case_cards: (num, title, blurb)"""
    meta = "".join(
        f"<div><span>{k}</span><strong>{v}</strong></div>" for k, v in ui["meta"]
    )
    cards = "".join(
        f'<div class="print-toc-card"><span class="num">{num}</span>'
        f"<strong>{title}</strong><p>{blurb}</p></div>"
        for num, title, blurb in case_cards
    )
    return f"""<section class="section flow page-start print-home" id="page-home" data-nav-label="{ui['toc_nav']}">
      <div class="section-head"><span class="section-num">{ui['home_num']}</span><h2>{ui['home_h2']}</h2></div>
      <p class="eyebrow">{ui['cover_eyebrow']}</p>
      <p class="lead" style="font-size:12pt;color:var(--ink);font-weight:600">{ui['cover_h1']}</p>
      <p class="lead">{ui['home_lead']}</p>
      <div class="print-home-meta">{meta}</div>
      <div class="print-toc">{cards}</div>
    </section>"""


def toolbar_html(ui: dict) -> str:
    other_label, other_href = ui["toolbar_other"]
    return f"""  <div class="no-print toolbar">
    <div>
      <p>{ui['cover_chip']} · Print</p>
      <p style="margin-top:4px">{ui['toolbar_note']}</p>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
      <a href="{other_href}" style="color:var(--brand);font-weight:600;text-decoration:none">{other_label}</a>
      <button type="button" onclick="window.print()">{ui['print_btn']}</button>
    </div>
  </div>"""


def nav_html(ui: dict) -> str:
    return f"""  <nav class="doc-nav no-print" aria-label="Page navigation">
    <button type="button" class="doc-nav-prev">{ui['nav_prev']}</button>
    <div class="doc-nav-mid">
      <span class="doc-nav-label"></span>
      <button type="button" class="doc-nav-pdf" onclick="window.print()">PDF</button>
    </div>
    <button type="button" class="doc-nav-next">{ui['nav_next']}</button>
  </nav>"""


NAV_SCRIPT = r"""<script>
(function () {
  var pages = Array.prototype.slice.call(document.querySelectorAll(".sheet > section[data-nav-label]"));
  if (!pages.length) return;
  var prevBtn = document.querySelector(".doc-nav-prev");
  var nextBtn = document.querySelector(".doc-nav-next");
  var labelEl = document.querySelector(".doc-nav-label");
  var index = 0;

  function currentIndex() {
    var mid = window.scrollY + window.innerHeight * 0.28;
    var best = 0;
    for (var i = 0; i < pages.length; i++) {
      if (pages[i].offsetTop <= mid) best = i;
    }
    return best;
  }

  function sync() {
    index = currentIndex();
    var page = pages[index];
    labelEl.textContent = (index + 1) + " / " + pages.length + " · " + page.getAttribute("data-nav-label");
    prevBtn.disabled = index <= 0;
    nextBtn.disabled = index >= pages.length - 1;
  }

  function go(delta) {
    var next = Math.max(0, Math.min(pages.length - 1, currentIndex() + delta));
    pages[next].scrollIntoView({ behavior: "smooth", block: "start" });
  }

  prevBtn.addEventListener("click", function () { go(-1); });
  nextBtn.addEventListener("click", function () { go(1); });
  window.addEventListener("scroll", sync, { passive: true });
  window.addEventListener("resize", sync);
  sync();
})();
</script>"""


def case_blurb(section_html: str) -> str:
    m = re.search(r'<p class="who">(.*?)</p>', section_html, flags=re.S)
    if not m:
        return ""
    text = re.sub(r"<[^>]+>", "", m.group(1))
    return re.sub(r"\s+", " ", text).strip()


CASES_LAYOUT_CSS = """
    /* ===== Value-cases: full-width visual, one case per print page ===== */
    .sheet {
      max-width: 220mm;
      margin: 0 auto;
      padding: 10mm 0 96px;
    }
    @media print {
      .sheet { max-width: none; padding: 0; margin: 0; }
    }

    .case-page {
      display: flex;
      flex-direction: column;
      gap: 0;
      padding: 0 !important;
      border-bottom: 0 !important;
      min-height: 250mm;
      break-inside: avoid-page;
      page-break-inside: avoid;
    }
    .case-page.page-start {
      break-before: page;
      page-break-before: always;
    }

    .case-hero {
      position: relative;
      width: 100%;
      margin: 0 0 14px;
      overflow: hidden;
      background: #0f172a;
      break-inside: avoid;
      page-break-inside: avoid;
    }
    .case-hero img {
      display: block;
      width: 100%;
      height: 82mm;
      object-fit: cover;
      object-position: center;
      filter: grayscale(0.15) contrast(1.05);
    }
    .case-hero-veil {
      position: absolute; inset: 0;
      background: linear-gradient(to top, rgba(15,23,42,0.72) 0%, rgba(15,23,42,0.12) 45%, rgba(15,23,42,0.05) 100%);
      pointer-events: none;
    }
    .case-hero-meta {
      position: absolute; left: 0; right: 0; bottom: 0;
      padding: 18px 18px 16px;
      color: #fff;
      z-index: 1;
    }
    .case-hero-num {
      display: inline-block;
      margin-bottom: 8px;
      padding: 3px 9px;
      background: rgba(25,118,210,0.92);
      color: #fff;
      font-size: 9px;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }
    .case-hero-meta h2 {
      margin: 0 0 6px;
      color: #fff;
      font-size: 18pt;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.15;
      max-width: 34ch;
    }
    .case-hero-meta .who {
      margin: 0;
      color: rgba(255,255,255,0.78);
      font-size: 9pt;
      font-weight: 500;
      line-height: 1.35;
      max-width: 58ch;
    }
    .case-hero-credit {
      position: absolute; top: 10px; right: 12px; z-index: 1;
      margin: 0;
      color: rgba(255,255,255,0.55);
      font-size: 7pt;
      letter-spacing: 0.02em;
    }

    .case-body {
      display: grid;
      grid-template-columns: 1.35fr 0.9fr;
      gap: 16px;
      align-items: start;
      padding: 0 2px 8px;
    }
    .case-intro {
      margin: 0 0 12px;
      font-size: 10.25pt;
      line-height: 1.45;
      color: var(--ink);
    }
    .case-features {
      margin: 0;
      padding-left: 16px;
      font-size: 9.25pt;
      line-height: 1.4;
    }
    .case-features li + li { margin-top: 5px; }

    .case-aside {
      background: var(--band);
      padding: 14px 14px 12px;
      break-inside: avoid;
      page-break-inside: avoid;
    }
    .case-aside h3 {
      margin: 0 0 8px;
      font-size: 10pt;
      font-weight: 800;
      color: var(--brand-dark);
    }
    .case-aside > p {
      margin: 0 0 12px;
      font-size: 9.25pt;
      line-height: 1.4;
      color: var(--ink);
    }
    .case-aside .tags { margin-top: 10px; }
    .case-aside .side-note {
      margin-top: 10px;
      font-size: 8.5pt;
      color: var(--soft);
    }
    .case-notify {
      margin-top: 12px;
      padding-top: 10px;
      border-top: 1px solid var(--line);
    }
    .case-notify h5 {
      margin: 0 0 6px;
      font-size: 8.5pt;
      font-weight: 800;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--brand);
    }
    .case-notify ul {
      margin: 0;
      padding-left: 14px;
      font-size: 8.5pt;
      color: var(--muted);
    }
    .case-notify li + li { margin-top: 3px; }

    @media print {
      .case-page {
        min-height: 0;
        height: auto;
        max-height: none;
        overflow: hidden;
        break-after: page;
        page-break-after: always;
      }
      .case-page:last-of-type {
        break-after: auto;
        page-break-after: auto;
      }
      .case-hero {
        margin-left: -14mm;
        margin-right: -14mm;
        width: calc(100% + 28mm);
      }
      .case-hero img { height: 70mm; }
      .case-hero-meta { padding: 16px 14mm 14px; }
      .case-hero-credit { right: 14mm; }
      .case-body { gap: 12px; }
      .case-intro { font-size: 9.75pt; }
      .case-features { font-size: 8.75pt; }
      .case-features li + li { margin-top: 3.5px; }
      .case-aside > p,
      .case-notify ul { font-size: 8.5pt; }
    }
    @media (max-width: 720px) {
      .case-body { grid-template-columns: 1fr; }
      .case-hero img { height: 52vw; min-height: 180px; max-height: 280px; }
      .case-page { min-height: 0; }
    }
"""


def _inner(html: str, pattern: str) -> str:
    m = re.search(pattern, html, flags=re.S)
    return m.group(1).strip() if m else ""


def render_case_page(section_html: str, num: int, nav_label: str, sid: str) -> str:
    """Rebuild a case section as full-width visual + one printable page."""
    title = persona_title(section_html) or sid
    who = _inner(section_html, r'<p class="who">(.*?)</p>')
    intro = _inner(section_html, r'<p class="case-intro">(.*?)</p>')

    features = ""
    fm = re.search(
        r'<p class="case-intro">.*?</p>\s*<ul>(.*?)</ul>\s*<div class="notify">',
        section_html,
        flags=re.S,
    )
    if fm:
        features = fm.group(1).strip()
    else:
        fm = re.search(r'<ul>(.*?)</ul>\s*<div class="notify">', section_html, flags=re.S)
        if fm:
            features = fm.group(1).strip()

    notify_h = _inner(section_html, r'<div class="notify">\s*<h5>(.*?)</h5>')
    notify_ul = _inner(section_html, r'<div class="notify">\s*<h5>.*?</h5>\s*<ul>(.*?)</ul>')

    img_src = _inner(section_html, r'<img class="card-visual"[^>]*src="([^"]+)"')
    img_alt = _inner(section_html, r'<img class="card-visual"[^>]*alt="([^"]*)"')
    credit = _inner(section_html, r'<p class="card-visual-credit">(.*?)</p>')
    why_h = _inner(section_html, r'<h4>(Why it matters|Γιατί μετράει)</h4>')
    why_p = _inner(
        section_html,
        r'<h4>(?:Why it matters|Γιατί μετράει)</h4>\s*<p>(.*?)</p>',
    )
    tags = _inner(section_html, r'<div class="tags">(.*?)</div>')
    side = _inner(section_html, r'<p class="side-note">(.*?)</p>')

    credit_html = f'<p class="case-hero-credit">{credit}</p>' if credit else ""
    side_html = f'<p class="side-note">{side}</p>' if side else ""
    notify_html = ""
    if notify_h and notify_ul:
        notify_html = f"""        <div class="case-notify">
          <h5>{notify_h}</h5>
          <ul>
            {notify_ul}
          </ul>
        </div>"""

    return f"""<section class="section case-page page-start" id="{sid}" data-nav-label="{nav_label}">
      <div class="case-hero">
        <img src="{img_src}" alt="{img_alt}" />
        <div class="case-hero-veil"></div>
        {credit_html}
        <div class="case-hero-meta">
          <span class="case-hero-num">Case {num:02d}</span>
          <h2>{title}</h2>
          <p class="who">{who}</p>
        </div>
      </div>
      <div class="case-body">
        <div class="case-main">
          <p class="case-intro">{intro}</p>
          <ul class="case-features">
            {features}
          </ul>
        </div>
        <aside class="case-aside">
          <h3>{why_h or "Why it matters"}</h3>
          <p>{why_p}</p>
          <div class="tags">
            {tags}
          </div>
          {side_html}
          {notify_html}
        </aside>
      </div>
    </section>"""


def build_lang(lang: str) -> str:
    ui = META[lang]
    src_html = SRC[lang].read_text(encoding="utf-8")
    style = extract_head_styles(src_html)
    # Inject layout CSS before closing </style>
    if "</style>" in style:
        style = style.replace("</style>", CASES_LAYOUT_CSS + "\n  </style>", 1)
    else:
        style = style + f"<style>{CASES_LAYOUT_CSS}</style>"

    sections = extract_sections(src_html)
    order = CASE_ORDER_EN if lang == "en" else CASE_ORDER_EL

    case_sections: list[str] = []
    toc_cards: list[tuple[str, str, str]] = []
    for i, sid in enumerate(order, start=1):
        if sid not in sections:
            raise SystemExit(f"Missing section {sid} in {lang} print source")
        sec = sections[sid]
        title = persona_title(sec) or sid
        nav = f"{i:02d} · {title}"
        case_sections.append(render_case_page(sec, i, nav, sid))
        toc_cards.append((f"{i:02d}", title, case_blurb(sec)))

    body = "\n\n".join(
        [
            cover_html(ui),
            toc_html(ui, toc_cards),
            *case_sections,
        ]
    )

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{ui['title']}</title>
  {style}
</head>
<body>
{toolbar_html(ui)}

  <div class="sheet">
{body}

  </div>

{nav_html(ui)}
{NAV_SCRIPT}
</body>
</html>
"""
    return html


def apply_copy_edits(lang: str, html: str) -> str:
    """Editorial tweaks for the cases-only brochure (kept across rebuilds)."""
    if lang == "en":
        reps = [
            (
                "Connectors such as HubSpot keep grants and contacts aligned",
                "Connectors with CRM systems, such as HubSpot, keep presence grants and contacts aligned",
            ),
            (
                "<li><strong>HubSpot CRM</strong> — first CRM connector: sync contacts, post grants to HubSpot in real time</li>",
                "<li><strong>CRM Connectors</strong> — e.g. HubSpot CRM connector: sync contacts, post grants to HubSpot in real time</li>",
            ),
            (
                "HR / People ops (daily digests, not manual chase)",
                "HR / People ops (frequent presence reports, near real time, daily, weekly, monthly, configurable, etc.)",
            ),
            (
                "Facilities · HubSpot contact timeline (grants)",
                "Facilities · CRM contact timeline (grants)",
            ),
            (
                "Families need light protection for the home",
                "Families need automated protection for the home",
            ),
            (
                "when an unknown person enters living areas",
                "when an unknown person stands in front of a door or enters living areas",
            ),
            (
                "Secure zones</strong> — alarm if an unspecified person enters living areas",
                "Secure zones</strong> — alarm if an unspecified person stands in front of a door or enters living areas",
            ),
            (
                "— lightly, privately, without a full security team",
                "— automatically, privately, without a full security team",
            ),
        ]
        for old, new in reps:
            html = html.replace(old, new)
        html, _ = re.subn(
            r'\n\s*<div class="panel summary-panel">\s*'
            r'<h4>Use case → primary why</h4>.*?</div>\s*</div>\s*(?=</section>)',
            "\n",
            html,
            count=1,
            flags=re.S,
        )
        html, _ = re.subn(
            r'\n\s*<div class="kicker">Featured use cases — where EyeNet replaces manual presence, '
            r'blind nights, and disconnected sites with automatic vision\.</div>',
            "",
            html,
        )
        return html

    reps = [
        (
            "Connectors όπως το HubSpot κρατούν grants και επαφές συγχρονισμένα",
            "Connectors με συστήματα CRM, όπως το HubSpot, κρατούν presence grants και επαφές συγχρονισμένα",
        ),
        (
            "<li><strong>HubSpot CRM</strong> — πρώτος CRM connector: συγχρονισμός επαφών, post grants στο HubSpot σε πραγματικό χρόνο</li>",
            "<li><strong>CRM Connectors</strong> — π.χ. HubSpot CRM connector: συγχρονισμός επαφών, post grants στο HubSpot σε πραγματικό χρόνο</li>",
        ),
        (
            "HR / People ops (ημερήσια digests, όχι χειροκίνητο κυνήγι)",
            "HR / People ops (συχνές αναφορές παρουσίας, σχεδόν πραγματικού χρόνου, ημερήσιες, εβδομαδιαίες, μηνιαίες, παραμετροποιήσιμες κ.λπ.)",
        ),
        (
            "Εγκαταστάσεις · timeline επαφής HubSpot (grants)",
            "Εγκαταστάσεις · timeline επαφής CRM (grants)",
        ),
        (
            "Οι οικογένειες χρειάζονται ελαφριά προστασία για σπίτι",
            "Οι οικογένειες χρειάζονται αυτοματοποιημένη προστασία για σπίτι",
        ),
        (
            "όταν άγνωστο πρόσωπο μπαίνει σε χώρους διαβίωσης",
            "όταν άγνωστο πρόσωπο στέκεται μπροστά σε πόρτα ή μπαίνει σε χώρους διαβίωσης",
        ),
        (
            "Secure zones</strong> — συναγερμός αν άγνωστο πρόσωπο μπει σε χώρους διαβίωσης",
            "Secure zones</strong> — συναγερμός αν άγνωστο πρόσωπο σταθεί μπροστά σε πόρτα ή μπει σε χώρους διαβίωσης",
        ),
        (
            "— ελαφρά, ιδιωτικά, χωρίς πλήρη ομάδα ασφαλείας",
            "— αυτόματα, ιδιωτικά, χωρίς πλήρη ομάδα ασφαλείας",
        ),
    ]
    for old, new in reps:
        html = html.replace(old, new)
    html, _ = re.subn(
        r'\n\s*<div class="panel summary-panel">\s*'
        r'<h4>Περίπτωση χρήσης → βασικό γιατί</h4>.*?</div>\s*</div>\s*(?=</section>)',
        "\n",
        html,
        count=1,
        flags=re.S,
    )
    html, _ = re.subn(
        r'\n\s*<div class="kicker">Επιλεγμένες περιπτώσεις χρήσης — όπου το EyeNet αντικαθιστά '
        r'χειροκίνητη παρουσία, τυφλές νύχτες και αποσυνδεδεμένους χώρους με αυτόματη όραση\.</div>',
        "",
        html,
    )
    return html


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "el").mkdir(parents=True, exist_ok=True)

    en = apply_copy_edits("en", build_lang("en"))
    el = apply_copy_edits("el", build_lang("el"))
    (OUT / "index.html").write_text(en, encoding="utf-8")
    (OUT / "el" / "index.html").write_text(el, encoding="utf-8")

    assets = collect_assets(en) | collect_assets(el)
    # Always include brand mark
    assets.add("/assets/eyenet-dark.svg")
    copy_assets(assets)

    readme = OUT / "README.md"
    readme.write_text(
        """# EyeNet use cases (print-only)

Separate bilingual print site with **only** the featured use cases from `value/`.
Full-width visuals · one use case per printable page.

- English: `/` (Print → Save as PDF)
- Greek: `/el/`

## Rebuild

After updating the value print brochure:

```bash
python3 usecases/scripts/build_cases_print.py
```

## Preview

```bash
cd usecases
python3 -m http.server 8769
# open http://127.0.0.1:8769/ and http://127.0.0.1:8769/el/
```

## Deploy

Cloudflare Pages project with root directory `usecases` (separate from `value.eyenet-vision.com`).
""",
        encoding="utf-8",
    )
    print("wrote", OUT / "index.html")
    print("wrote", OUT / "el" / "index.html")
    print(f"assets copied: {len(assets)}")


if __name__ == "__main__":
    main()
