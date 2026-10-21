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

ASSET_V = "20261021o"

WITH_HEADING = {
    "en": "Who uses EyeNet",
    "el": "Ποιος χρησιμοποιεί το EyeNet",
}
CONTENT_DIR = ROOT / "content"

INNOVATION_HEADING = {
    "en": "Simple yet powerful innovation",
    "el": "Απλή κι όμως ισχυρή καινοτομία",
}

WHAT_HEADING = {
    "en": "EyeNet understands what it sees and acts on it automatically",
    "el": "Το EyeNet κατανοεί ό,τι βλέπει και ενεργεί αυτόματα",
}

WHY_HEADING = {
    "en": "Most Valuable Cases",
    "el": "Πιο πολύτιμες περιπτώσεις",
}

PACKAGES_HEADING = {
    "en": "Commercial Packages — B2C · B2B · Enterprise",
    "el": "Εμπορικά πακέτα — B2C · B2B · Enterprise",
}

# Reading order for Previous / Next footer links (path relative to lang root).
PAGE_ORDER = [
    "",
    "what",
    "why",
    "why/hr-presence",
    "why/mall",
    "why/cottage",
    "why/home-care",
    "why/security",
    "why/shipping",
    "with-eyenet",
    "packages",
    "packages/b2c",
    "packages/b2b",
    "packages/enterprise",
    "innovation",
]

# Brochure §05 persona index → why child slug (source order, not display order).
WHY_PERSONA_INDEX = {
    "home-care": 0,
    "hr-presence": 1,
    "security": 2,
    "cottage": 3,
    "shipping": 4,
    "mall": 5,
}


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


def _ext(label: str, url: str) -> str:
    """External citation link (new tab)."""
    return (
        f'<a class="source-link" href="{url}" target="_blank" rel="noopener noreferrer">'
        f"{label}</a>"
    )


def normalize_package_addressable_pockets(html: str, lang: str) -> str:
    """Normalize package pocket headings with cite-backed, linked market metrics."""
    # Primary / public sources (checked Oct 2026).
    url_census_acs = "https://data.census.gov/table/ACSDT1Y2024.C25075"
    url_census_cbp = "https://www.census.gov/data/datasets/2023/econ/cbp/2023-cbp.html"
    url_marketing = "https://naicscodes.org/industry/54161-management-consulting-services/"
    url_retail = "https://data.census.gov/table/ECNBASIC2022.EC2244BASIC"
    url_restaurants = "https://naicscodes.org/industry-group/7225-restaurants-and-other-eating-places/"
    url_nasco = "https://www.nasco.org/wp-content/uploads/2024/09/2024_White_Paper.pdf"
    url_nces = "https://nces.ed.gov/ccd/tables/202425_summary_3.asp"
    url_ibis_wh = (
        "https://www.ibisworld.com/united-states/number-of-businesses/"
        "general-warehousing-storage/1224/"
    )
    url_airbnb_hosts = (
        "https://www.credaily.com/briefs/the-political-influence-of-short-term-rentals-is-growing/"
    )

    b2c_list_en = (
        "<li>~52K marketing consulting establishments "
        f"({_ext('U.S. Census CBP 2023, NAICS 541613', url_marketing)})</li>"
        "<li>~87M owner-occupied homes "
        f"({_ext('U.S. Census ACS 2024', url_census_acs)}) · "
        "~0.8M U.S. Airbnb hosts "
        f"({_ext('industry reports 2024', url_airbnb_hosts)})</li>"
        "<li>~8K U.S. contract security companies "
        f"({_ext('NASCO 2024', url_nasco)})</li>"
        "<li>~1.0M+ retail + ~0.6M restaurant establishments "
        f"({_ext('Census Economic Census', url_retail)} · "
        f"{_ext('CBP / NAICS 7225', url_restaurants)})</li>"
    )
    b2b_list_en = (
        "<li>Multi-location retail &amp; offices · ACV path $12–36K "
        "(EyeNet plan unit economics)</li>"
        "<li>~8K U.S. contract security companies "
        f"({_ext('NASCO 2024', url_nasco)}) · Starter → Pro</li>"
        "<li>~99K public K–12 schools "
        f"({_ext('NCES SY 2024–25', url_nces)}) · campus pilot to roll-out</li>"
        "<li>~38K general warehousing &amp; storage businesses "
        f"({_ext('IBISWorld 2024', url_ibis_wh)})</li>"
    )
    b2c_list_el = (
        "<li>~52K marketing consulting establishments "
        f"({_ext('U.S. Census CBP 2023, NAICS 541613', url_marketing)})</li>"
        "<li>~87M owner-occupied homes "
        f"({_ext('U.S. Census ACS 2024', url_census_acs)}) · "
        "~0.8M U.S. Airbnb hosts "
        f"({_ext('industry reports 2024', url_airbnb_hosts)})</li>"
        "<li>~8K U.S. contract security companies "
        f"({_ext('NASCO 2024', url_nasco)})</li>"
        "<li>~1.0M+ retail + ~0.6M restaurant establishments "
        f"({_ext('Census Economic Census', url_retail)} · "
        f"{_ext('CBP / NAICS 7225', url_restaurants)})</li>"
    )
    b2b_list_el = (
        "<li>Πολυτοπικό retail &amp; γραφεία · ACV path $12–36K "
        "(EyeNet plan unit economics)</li>"
        "<li>~8K U.S. contract security companies "
        f"({_ext('NASCO 2024', url_nasco)}) · Starter → Pro</li>"
        "<li>~99K δημόσια σχολεία K–12 "
        f"({_ext('NCES SY 2024–25', url_nces)}) · campus pilot έως roll-out</li>"
        "<li>~38K general warehousing &amp; storage businesses "
        f"({_ext('IBISWorld 2024', url_ibis_wh)})</li>"
    )

    sources_en = f"""<div class="source-block">
<p class="side-note"><strong>External pocket sources</strong> (checked Oct 2026) — click to verify:</p>
<ul class="source-list">
<li>{_ext('U.S. Census ACS 2024 — owner-occupied housing', url_census_acs)}</li>
<li>{_ext('U.S. Census CBP 2023 datasets', url_census_cbp)} · {_ext('marketing consulting (NAICS 54161)', url_marketing)}</li>
<li>{_ext('Census Economic Census — retail trade', url_retail)} · {_ext('restaurants (NAICS 7225)', url_restaurants)}</li>
<li>{_ext('NASCO 2024 — U.S. contract security companies (~8K)', url_nasco)}</li>
<li>{_ext('NCES CCD — public K–12 schools SY 2024–25', url_nces)}</li>
<li>{_ext('IBISWorld — general warehousing &amp; storage businesses', url_ibis_wh)}</li>
<li>{_ext('U.S. Airbnb host count (industry reporting)', url_airbnb_hosts)}</li>
</ul>
<p class="side-note"><strong>Internal:</strong> TAM bands and target-share % are EyeNet Vision business-plan assumptions (U.S., conservative) — not Census/NCES figures.</p>
</div>"""
    sources_el = f"""<div class="source-block">
<p class="side-note"><strong>Εξωτερικές πηγές pockets</strong> (ελέγχθηκαν Οκτ 2026) — κλικ για επαλήθευση:</p>
<ul class="source-list">
<li>{_ext('U.S. Census ACS 2024 — owner-occupied housing', url_census_acs)}</li>
<li>{_ext('U.S. Census CBP 2023 datasets', url_census_cbp)} · {_ext('marketing consulting (NAICS 54161)', url_marketing)}</li>
<li>{_ext('Census Economic Census — retail trade', url_retail)} · {_ext('restaurants (NAICS 7225)', url_restaurants)}</li>
<li>{_ext('NASCO 2024 — U.S. contract security companies (~8K)', url_nasco)}</li>
<li>{_ext('NCES CCD — public K–12 schools SY 2024–25', url_nces)}</li>
<li>{_ext('IBISWorld — general warehousing &amp; storage businesses', url_ibis_wh)}</li>
<li>{_ext('U.S. Airbnb host count (industry reporting)', url_airbnb_hosts)}</li>
</ul>
<p class="side-note"><strong>Εσωτερικά:</strong> TAM και target-share % είναι υποθέσεις του EyeNet Vision business plan (ΗΠΑ, συντηρητικά) — όχι στοιχεία Census/NCES.</p>
</div>"""

    # Drop any prior sources footnotes before re-injecting.
    html = re.sub(
        r'<p class="side-note"[^>]*>.*?(?:Pocket counts|Μετρήσεις pockets|External pocket|Εξωτερικές πηγές).*?</p>\s*',
        "",
        html,
        flags=re.S,
    )
    html = re.sub(r'<div class="source-block">.*?</div>\s*', "", html, flags=re.S)

    if lang == "en":
        html = re.sub(
            r"(<h4(?:\s+style=\"[^\"]*\")?>)(?:Who buys|Segment map)(</h4>)",
            r"\1Addressable pockets\2",
            html,
        )
        html = re.sub(
            r"(<h4(?:\s+style=\"[^\"]*\")?>Addressable pockets</h4>\s*<ul>)\s*"
            r"(?:<li>(?:100,000\+|~52K marketing|140M|~87M owner|50,000\+|~8K U\.S\. contract|"
            r"1\.5M\+|~1\.0M\+).*?</li>\s*){4}"
            r"</ul>",
            r"\1" + b2c_list_en + r"</ul>",
            html,
            count=1,
            flags=re.S,
        )
        html = re.sub(
            r"(<span class=\"stat-label\">B2B / Enterprise TAM \(U\.S\.\)</span>\s*)"
            r"(?:<p>Target share 1–2% of mid-market wedge → ~\$20–80M opportunity\.</p>\s*)?"
            r"(?:<p[^>]*>Primary commercial wedge before full Enterprise\.</p>)",
            r"\1"
            r"<p>Target share 1–2% of mid-market wedge → ~$20–80M opportunity.</p>"
            r'<p style="font-size:0.9rem;color:var(--muted)">Primary commercial wedge before full Enterprise.</p>',
            html,
            count=1,
        )
        html = re.sub(
            r"(<h4(?:\s+style=\"[^\"]*\")?>Addressable pockets</h4>\s*<ul>)\s*"
            r"(?:<li>(?:Multi-location retail|Regional security|Schools / campuses|Warehouses|"
            r"~8K U\.S\. contract security|~99K public|~38K general).*?</li>\s*){4}"
            r"</ul>",
            r"\1" + b2b_list_en + r"</ul>",
            html,
            count=1,
            flags=re.S,
        )
        if "source-block" not in html and "Addressable pockets" in html:
            html = re.sub(
                r"(Addressable pockets</h4>\s*<ul>.*?</ul>)",
                r"\1\n" + sources_en,
                html,
                count=1,
                flags=re.S,
            )
    else:
        html = re.sub(
            r"(<h4(?:\s+style=\"[^\"]*\")?>)(?:Ποιος αγοράζει|Χάρτης τμημάτων|Διευθυνόμενες τσέπες)(</h4>)",
            r"\1Addressable pockets\2",
            html,
        )
        html = re.sub(
            r"(<h4(?:\s+style=\"[^\"]*\")?>Addressable pockets</h4>\s*<ul>)\s*"
            r"(?:<li>(?:100,000\+|~52K marketing|140M|~87M owner|50,000\+|~8K U\.S\. contract|"
            r"1\.5M\+|~1\.0M\+|ανεξάρτητοι).*?</li>\s*){4}"
            r"</ul>",
            r"\1" + b2c_list_el + r"</ul>",
            html,
            count=1,
            flags=re.S,
        )
        html = re.sub(
            r"(<span class=\"stat-label\">B2B / Enterprise TAM \(ΗΠΑ\)</span>\s*)"
            r"(?:<p>Target share 1–2% του mid-market wedge → ~\$20–80M opportunity\.</p>\s*)?"
            r"(?:<p[^>]*>Κύρια εμπορική σφήνα πριν το πλήρες Enterprise\.</p>)",
            r"\1"
            r"<p>Target share 1–2% του mid-market wedge → ~$20–80M opportunity.</p>"
            r'<p style="font-size:0.9rem;color:var(--muted)">Κύρια εμπορική σφήνα πριν το πλήρες Enterprise.</p>',
            html,
            count=1,
        )
        html = re.sub(
            r"(<h4(?:\s+style=\"[^\"]*\")?>Addressable pockets</h4>\s*<ul>)\s*"
            r"(?:<li>(?:Πολυτοπικό retail|Multi-location retail|Regional security|Schools / campuses|Warehouses|"
            r"Περιφερειακές|Σχολεία|Αποθήκες|~8K U\.S\. contract|~99K|~38K general).*?</li>\s*){4}"
            r"</ul>",
            r"\1" + b2b_list_el + r"</ul>",
            html,
            count=1,
            flags=re.S,
        )
        if "source-block" not in html and "Addressable pockets" in html:
            html = re.sub(
                r"(Addressable pockets</h4>\s*<ul>.*?</ul>)",
                r"\1\n" + sources_el,
                html,
                count=1,
                flags=re.S,
            )
    return html


def relocate_what_lead_kicker(html: str) -> str:
    """Move the What lead kicker to sit just before Addendum — EyeNet in action."""
    m = re.search(
        r'<div class="kicker">(?:EyeNet turns ordinary cameras|Το EyeNet μετατρέπει συνηθισμένες κάμερες).*?</div>\s*',
        html,
        flags=re.S,
    )
    if not m:
        return html
    kicker = m.group(0).rstrip() + "\n\n"
    html = html[: m.start()] + html[m.end() :]
    html, n = re.subn(
        r"(<h2>(?:Addendum — EyeNet in action|Παράρτημα — το EyeNet σε δράση)</h2>)",
        kicker + r"\1",
        html,
        count=1,
    )
    if n != 1:
        raise SystemExit("Could not place What lead kicker before Addendum")
    return html


def apply_case_label_copy(html: str, lang: str) -> str:
    """Rename Security and Mall marketing studio case labels / related cards."""
    if lang == "en":
        repls = [
            (
                r"Security personnel — night &amp; perimeter",
                "Security: night and Perimeter",
            ),
            (r"Security night &amp; perimeter", "Security: night and Perimeter"),
            (r"Security night & perimeter", "Security: night and Perimeter"),
            (
                r'data-nav-label="05 · Security"',
                'data-nav-label="05 · Security: night and Perimeter"',
            ),
            (
                r"Mall marketing studio — foot traffic → intelligence",
                "Vision-adaptive Intelligent Signage",
            ),
            (
                r"Mall marketing studio — κίνηση → νοημοσύνη",
                "Vision-adaptive Intelligent Signage",
            ),
            (r"Mall marketing studio", "Vision-adaptive Intelligent Signage"),
            (
                r'data-nav-label="05 · Mall"',
                'data-nav-label="05 · Vision-adaptive Intelligent Signage"',
            ),
            (r"<h5>Mall marketer</h5>", "<h5>Signage marketer</h5>"),
            (
                r"With EyeNet, a mall marketer gets foot traffic turned into measurable studio ROI",
                "With EyeNet, a signage marketer gets foot traffic turned into measurable studio ROI",
            ),
            (
                r"Mall operators · retail marketing · agencies · brand studios",
                "Retail · venues · agencies · brand studios · digital signage operators",
            ),
            (
                r"<li><strong>Mall as studio</strong> — digital signage network becomes a measurable marketing studio across concourses, shops, and spots</li>",
                "<li><strong>Signage as studio</strong> — every screen becomes a measurable marketing surface across concourses, shops, and spots</li>",
            ),
            (
                r"Vision-adaptive Signage turns mall foot traffic into measurable marketing intelligence",
                "Vision-adaptive Intelligent Signage turns foot traffic into measurable marketing intelligence",
            ),
            (
                r'alt="EyeNet digital signage marketing"',
                'alt="EyeNet Vision-adaptive Intelligent Signage"',
            ),
            (
                r"Shipping — crew where they should be",
                "Shipping and industrial",
            ),
            (r">Shipping<", ">Shipping and industrial<"),
            (
                r'data-nav-label="05 · Shipping"',
                'data-nav-label="05 · Shipping and industrial"',
            ),
            (
                r"<h5>Fleet manager</h5>",
                "<h5>Fleet &amp; industrial ops</h5>",
            ),
            (
                r"With EyeNet, a fleet manager gets a clear operational outlook of every ship — who is onboard, where they should be — with a few targeted mobile notifications even on thin connectivity\.",
                "With EyeNet, a fleet or plant manager gets a clear operational outlook of every ship or industrial site — who is onboard or on site, where they should be — with a few targeted mobile notifications even on thin connectivity.",
            ),
        ]
    else:
        repls = [
            (
                r"Προσωπικό ασφαλείας — νύχτα &amp; περίμετρος",
                "Ασφάλεια: νύχτα και περίμετρος",
            ),
            (r"Ασφάλεια νύχτα &amp; περίμετρος", "Ασφάλεια: νύχτα και περίμετρος"),
            (r"Ασφάλεια νύχτα & περίμετρος", "Ασφάλεια: νύχτα και περίμετρος"),
            (
                r'data-nav-label="05 · [^"]*[Αα]σφάλ[^"]*"',
                'data-nav-label="05 · Ασφάλεια: νύχτα και περίμετρος"',
            ),
            (
                r"Mall marketing studio — κίνηση → νοημοσύνη",
                "Vision-adaptive Intelligent Signage",
            ),
            (
                r"Mall marketing studio — foot traffic → intelligence",
                "Vision-adaptive Intelligent Signage",
            ),
            (r"Mall marketing studio", "Vision-adaptive Intelligent Signage"),
            (
                r'data-nav-label="05 · Mall"',
                'data-nav-label="05 · Vision-adaptive Intelligent Signage"',
            ),
            (
                r"Operators mall · retail marketing · agencies · brand studios",
                "Retail · χώροι · agencies · brand studios · operators digital signage",
            ),
            (
                r"<li><strong>Mall ως studio</strong> — το δίκτυο digital signage γίνεται μετρήσιμο marketing studio σε διαδρόμους, καταστήματα και spots</li>",
                "<li><strong>Signage ως studio</strong> — κάθε οθόνη γίνεται μετρήσιμη marketing επιφάνεια σε διαδρόμους, καταστήματα και spots</li>",
            ),
            (
                r"Το vision-adaptive Signage μετατρέπει την κίνηση στο mall σε μετρήσιμη marketing νοημοσύνη",
                "Το Vision-adaptive Intelligent Signage μετατρέπει την κίνηση σε μετρήσιμη marketing νοημοσύνη",
            ),
            (
                r'alt="EyeNet digital signage marketing"',
                'alt="EyeNet Vision-adaptive Intelligent Signage"',
            ),
            (
                r"Ναυτιλία — πλήρωμα εκεί που πρέπει",
                "Ναυτιλία και βιομηχανία",
            ),
            (r">Ναυτιλία<", ">Ναυτιλία και βιομηχανία<"),
            (
                r'data-nav-label="05 · Ναυτιλία"',
                'data-nav-label="05 · Ναυτιλία και βιομηχανία"',
            ),
            (
                r"<h5>Διαχειριστής στόλου</h5>",
                "<h5>Λειτουργίες στόλου &amp; βιομηχανίας</h5>",
            ),
            (
                r"Με το EyeNet, ένας διαχειριστής στόλου αποκτά καθαρή επιχειρησιακή εικόνα κάθε πλοίου — ποιος είναι επί του σκάφους, πού πρέπει να είναι — με λίγες στοχευμένες mobile ειδοποιήσεις ακόμη και με λεπτή συνδεσιμότητα\.",
                "Με το EyeNet, ένας διαχειριστής στόλου ή εργοστασίου αποκτά καθαρή επιχειρησιακή εικόνα κάθε πλοίου ή βιομηχανικού χώρου — ποιος είναι επί του σκάφους ή στον χώρο, πού πρέπει να είναι — με λίγες στοχευμένες mobile ειδοποιήσεις ακόμη και με λεπτή συνδεσιμότητα.",
            ),
        ]
    for pattern, repl in repls:
        html = re.sub(pattern, repl, html)
    return html


def apply_family_protection_copy(html: str, lang: str) -> str:
    """Rename/rephrase Cottage & remote living → Family protection at home and remote."""
    if lang == "en":
        repls = [
            (
                r'(<h4><span class="n">4</span>\s*)Cottage &amp; remote living(</h4>)',
                r"\1Family protection at home and remote\2",
            ),
            (
                r'<p class="who">Families · cottage owners · undergraduates away from home</p>',
                '<p class="who">Families · parents · households · students living away</p>',
            ),
            (
                r"<li><strong>Cottage / second-home protection</strong> — intrusion and unknown-person alerts when empty</li>",
                "<li><strong>Home protection</strong> — intrusion and unknown-person alerts when the house is empty</li>",
            ),
            (
                r"<li><strong>Remote students</strong> — undergraduates living away; family peace of mind without cloud video</li>",
                "<li><strong>Family away / remote students</strong> — peace of mind when loved ones live away, without cloud video</li>",
            ),
            (
                r"<li><strong>Presence check</strong> — confirm someone is \(or should be\) in the dwelling</li>",
                "<li><strong>Presence check</strong> — confirm someone is (or should be) at home</li>",
            ),
            (
                r"<li>Owner / family \(mobile push · email\)</li>",
                "<li>Parents / family (mobile push · email)</li>",
            ),
            (
                r"<li>Resident \(student / occupant\)</li>",
                "<li>Resident (student / household member)</li>",
            ),
            (
                r"Protect people and places that sit far from family — lightly, privately, without a full security team\.",
                "Protect family at home and when someone is away — lightly, privately, without a full security team.",
            ),
            (
                r'data-nav-label="05 · Cottage"',
                'data-nav-label="05 · Family protection"',
            ),
            (
                r"Cottage / remote → family peace of mind",
                "Family protection → peace of mind at home and remote",
            ),
            (
                r"<h5>Family · cottage &amp; remote living</h5>",
                "<h5>Family protection at home and remote</h5>",
            ),
            (
                r"With EyeNet, a parent gets peace of mind for a cottage or a student living away — intrusion and presence events as a few targeted phone notifications, video never forced to the cloud\.",
                "With EyeNet, a parent gets peace of mind for the family home and for loved ones living away — intrusion and presence events as a few targeted phone notifications, video never forced to the cloud.",
            ),
            (
                r'alt="EyeNet remote operations"',
                'alt="EyeNet family protection at home and remote"',
            ),
        ]
    else:
        repls = [
            (
                r'(<h4><span class="n">4</span>\s*)Εξοχικό &amp; απομακρυσμένη διαβίωση(</h4>)',
                r"\1Οικογενειακή προστασία στο σπίτι και εξ αποστάσεως\2",
            ),
            (
                r"<p class=\"who\">Οικογένειες · ιδιοκτήτες εξοχικών · προπτυχιακοί μακριά από το σπίτι</p>",
                '<p class="who">Οικογένειες · γονείς · νοικοκυριά · φοιτητές μακριά από το σπίτι</p>',
            ),
            (
                r"<li><strong>Προστασία εξοχικού / δεύτερης κατοικίας</strong> — alerts εισβολής και αγνώστων όταν είναι κενό</li>",
                "<li><strong>Προστασία σπιτιού</strong> — alerts εισβολής και αγνώστων όταν το σπίτι είναι κενό</li>",
            ),
            (
                r"<li><strong>Απομακρυσμένοι φοιτητές</strong> — προπτυχιακοί μακριά· ηρεμία οικογένειας χωρίς cloud video</li>",
                "<li><strong>Οικογένεια μακριά / φοιτητές</strong> — ηρεμία όταν αγαπημένα πρόσωπα ζουν μακριά, χωρίς cloud video</li>",
            ),
            (
                r"<li><strong>Έλεγχος παρουσίας</strong> — επιβεβαίωση ότι κάποιος είναι \(ή πρέπει να είναι\) στην κατοικία</li>",
                "<li><strong>Έλεγχος παρουσίας</strong> — επιβεβαίωση ότι κάποιος είναι (ή πρέπει να είναι) στο σπίτι</li>",
            ),
            (
                r"<li>Ιδιοκτήτης / οικογένεια \(mobile push · email\)</li>",
                "<li>Γονείς / οικογένεια (mobile push · email)</li>",
            ),
            (
                r"<li>Κάτοικος \(φοιτητής / ένοικος\)</li>",
                "<li>Κάτοικος (φοιτητής / μέλος νοικοκυριού)</li>",
            ),
            (
                r"Προστασία ανθρώπων και χώρων μακριά από την οικογένεια — ελαφρά, ιδιωτικά, χωρίς πλήρη ομάδα ασφαλείας\.",
                "Προστασία της οικογένειας στο σπίτι και όταν κάποιος είναι μακριά — ελαφρά, ιδιωτικά, χωρίς πλήρη ομάδα ασφαλείας.",
            ),
            (
                r'data-nav-label="05 · [^"]*"',
                'data-nav-label="05 · Οικογενειακή προστασία"',
            ),
            (
                r"<h5>Οικογένεια · εξοχικό &amp; απομακρυσμένη διαβίωση</h5>",
                "<h5>Οικογενειακή προστασία στο σπίτι και εξ αποστάσεως</h5>",
            ),
            (
                r"Με το EyeNet, ένας γονέας αποκτά ηρεμία για εξοχικό ή φοιτητή μακριά από το σπίτι — γεγονότα εισβολής και παρουσίας ως λίγες στοχευμένες ειδοποιήσεις τηλεφώνου, χωρίς υποχρεωτικό cloud video\.",
                "Με το EyeNet, ένας γονέας αποκτά ηρεμία για το οικογενειακό σπίτι και για αγαπημένα πρόσωπα μακριά — γεγονότα εισβολής και παρουσίας ως λίγες στοχευμένες ειδοποιήσεις τηλεφώνου, χωρίς υποχρεωτικό cloud video.",
            ),
            (
                r'alt="EyeNet απομακρυσμένες λειτουργίες"',
                'alt="EyeNet οικογενειακή προστασία στο σπίτι και εξ αποστάσεως"',
            ),
        ]
    for pattern, repl in repls:
        html = re.sub(pattern, repl, html, count=0)
    return html


def relocate_what_edge_cards(html: str) -> str:
    """Move Edge / Action / Scale cards to just after EyeNet tech feature set."""
    m = re.search(
        r'<div class="cols-3">\s*'
        r'<div class="panel">\s*<span class="stat cyan">Edge</span>.*?</div>\s*'
        r'<div class="panel alt">\s*<span class="stat brand">(?:Action|Δράση)</span>.*?</div>\s*'
        r'<div class="panel">\s*<span class="stat ok">(?:Scale|Κλίμακα)</span>.*?</div>\s*'
        r"</div>\s*",
        html,
        flags=re.S,
    )
    if not m:
        raise SystemExit("Could not find Edge / Action / Scale cards")
    cards = m.group(0).rstrip() + "\n\n"
    html = html[: m.start()] + html[m.end() :]
    html, n = re.subn(
        r"(<h2>EyeNet tech feature set</h2>\s*)",
        r"\1" + cards,
        html,
        count=1,
    )
    if n != 1:
        raise SystemExit("Could not place Edge / Action / Scale after tech feature set")
    return html


WIKI_BASE = "https://wiki.eyenet-vision.com"


def _wiki_href(path: str) -> str:
    return f'{WIKI_BASE}{path}'


def _wiki_a(label: str, path: str) -> str:
    return (
        f'<a class="source-link" href="{_wiki_href(path)}" '
        f'target="_blank" rel="noopener noreferrer">{label}</a>'
    )


def _wiki_chip(href: str | None = None) -> str:
    """Minimized EyeNet logo + wiki pill linking to the product wiki."""
    url = href or f"{WIKI_BASE}/"
    return (
        f'<a class="wiki-chip" href="{url}" target="_blank" rel="noopener noreferrer" '
        f'title="EyeNet wiki">'
        f'<img class="wiki-chip-logo" src="/assets/eyenet-dark.svg?v={ASSET_V}" alt="" width="52" height="13" decoding="async">'
        f'<span class="wiki-chip-label">wiki</span>'
        f"</a>"
    )


def _wiki_more(_lang: str, links: list[tuple[str, str]]) -> str:
    """EyeNet wiki chip + arrow + deep links."""
    joined = " · ".join(_wiki_a(label, path) for label, path in links)
    return (
        f'<p class="wiki-more">'
        f"{_wiki_chip()}"
        f'<span class="wiki-more-arrow" aria-hidden="true">→</span>'
        f"{joined}"
        f"</p>\n"
    )


def inject_wiki_read_more(html: str, lang: str) -> str:
    """Prefer EyeNet wiki deep-links under tech feature set sections."""
    if "EyeNet tech feature set" not in html:
        return html
    # Idempotent: strip prior injections.
    html = re.sub(r'<p class="wiki-more">.*?</p>\s*', "", html, flags=re.S)
    html = re.sub(
        r'\s*<span class="wiki-more-inline">.*?</span>',
        "",
        html,
        flags=re.S,
    )

    # Intro after Edge / Action / Scale cards (or directly under the heading).
    intro = _wiki_more(
        lang,
        [
            ("What is EyeNet", "/what-is-eyenet/"),
            ("Shared platform", "/what-is-eyenet/shared-platform.html"),
            ("User guide", "/owners-admins/"),
        ],
    )
    cols3 = re.search(
        r'<h2>EyeNet tech feature set</h2>\s*'
        r'<div class="cols-3">\s*'
        r'<div class="panel">.*?</div>\s*'
        r'<div class="panel alt">.*?</div>\s*'
        r'<div class="panel">.*?</div>\s*'
        r"</div>\s*",
        html,
        flags=re.S,
    )
    if cols3:
        html = html[: cols3.end()] + intro + html[cols3.end() :]
    else:
        html, n = re.subn(
            r"(<h2>EyeNet tech feature set</h2>\s*)",
            r"\1" + intro,
            html,
            count=1,
        )
        if n != 1:
            raise SystemExit("Could not inject wiki intro under tech feature set")

    # (heading regex, wiki links) — EN + EL heading variants.
    section_links: list[tuple[str, list[tuple[str, str]]]] = [
        (
            r"1\. Computer vision &amp; people analytics",
            [
                ("Detections, individuals &amp; persons", "/owners-admins/detections-individuals-persons.html"),
                ("Cameras and detection", "/owners-admins/cameras-and-detection.html"),
                ("Presence", "/what-is-eyenet/presence.html"),
            ],
        ),
        (
            r"2\. (?:Camera &amp; hardware integration|Ενσωμάτωση καμερών &amp; hardware)",
            [
                ("Cameras and detection", "/owners-admins/cameras-and-detection.html"),
                ("Hardware &amp; Docker", "/owners-admins/hardware.html"),
            ],
        ),
        (
            r"3\. (?:Intelligent triggers &amp; automated actions|Έξυπνα triggers &amp; αυτοματοποιημένες ενέργειες)",
            [
                ("Vradar — alerts &amp; automation", "/owners-admins/alerts-and-automation.html"),
                ("Vradar overview", "/what-is-eyenet/vradar.html"),
                ("Digital signage", "/owners-admins/digital-signage.html"),
            ],
        ),
        (
            r"4\. (?:Video &amp; data management|Διαχείριση βίντεο &amp; δεδομένων)",
            [
                ("Media and collections", "/owners-admins/media-management.html"),
                ("Shared platform", "/what-is-eyenet/shared-platform.html"),
            ],
        ),
        (
            r"5\. (?:Intelligent communications|Έξυπνες επικοινωνίες)",
            [
                ("Vradar — alerts &amp; automation", "/owners-admins/alerts-and-automation.html"),
            ],
        ),
        (
            r"6\. Analytics &amp; insights",
            [
                ("Analytics and reports", "/owners-admins/analytics-and-reports.html"),
            ],
        ),
        (
            r"7\. (?:Deployment architecture|Αρχιτεκτονική ανάπτυξης)",
            [
                ("First install", "/owners-admins/"),
                ("Hardware &amp; Docker", "/owners-admins/hardware.html"),
                ("Remote access &amp; multi-site", "/owners-admins/multi-site-and-remote.html"),
            ],
        ),
        (
            r"8\. (?:Security &amp; access control|Ασφάλεια &amp; έλεγχος πρόσβασης)",
            [
                ("User management", "/owners-admins/users-and-roles.html"),
                ("Remote access &amp; VPN", "/owners-admins/multi-site-and-remote.html"),
            ],
        ),
        (
            r"9\. (?:Scalability &amp; expandability|Κλιμάκωση &amp; επεκτασιμότητα)",
            [
                ("Hardware &amp; Docker", "/owners-admins/hardware.html"),
                ("Digital signage", "/owners-admins/digital-signage.html"),
                ("Matrix", "/what-is-eyenet/matrix.html"),
            ],
        ),
        (
            r"10\. (?:Support &amp; monitoring|Υποστήριξη &amp; παρακολούθηση)",
            [
                ("Remote access &amp; multi-site", "/owners-admins/multi-site-and-remote.html"),
                ("Vradar — alerts &amp; automation", "/owners-admins/alerts-and-automation.html"),
            ],
        ),
        (
            r"(?:Technical architecture highlights|Τεχνικά highlights αρχιτεκτονικής)",
            [
                ("Vradar — alerts &amp; automation", "/owners-admins/alerts-and-automation.html"),
                ("Entrances and activity", "/owners-admins/entrances-and-activity.html"),
                ("Digital signage", "/owners-admins/digital-signage.html"),
                ("Signage overview", "/what-is-eyenet/signage.html"),
            ],
        ),
    ]

    for heading_re, links in section_links:
        more = _wiki_more(lang, links)
        html, n = re.subn(
            rf"(<h2>{heading_re}</h2>)(.*?)(?=\n<h2>|\Z)",
            lambda m, _more=more: m.group(1) + m.group(2).rstrip() + "\n" + _more + "\n",
            html,
            count=1,
            flags=re.S,
        )
        if n != 1:
            raise SystemExit(f"Could not inject wiki read-more for heading: {heading_re}")

    # Screenshot captions — inline wiki prefs where a guide exists.
    caption_links = [
        (
            r"(<figcaption><strong>Main Dashboard</strong> — [^<]+)",
            "/what-is-eyenet/",
            "EyeNet wiki",
        ),
        (
            r"(<figcaption><strong>Analytics Filters</strong> — [^<]+)",
            "/owners-admins/analytics-and-reports.html",
            "Analytics and reports",
        ),
        (
            r"(<figcaption><strong>System Settings</strong> — [^<]+)",
            "/owners-admins/users-and-roles.html",
            "User management / Settings",
        ),
        (
            r"(<figcaption><strong>Analytics Dashboard</strong> — [^<]+)",
            "/owners-admins/analytics-and-reports.html",
            "Analytics and reports",
        ),
        (
            r"(<figcaption><strong>Detection Analytics</strong> — [^<]+)",
            "/owners-admins/cameras-and-detection.html",
            "Cameras and detection",
        ),
        (
            r"(<figcaption><strong>Camera Management</strong> — [^<]+)",
            "/owners-admins/cameras-and-detection.html",
            "Cameras and detection",
        ),
        (
            r"(<figcaption><strong>Triggers Management</strong> — [^<]+)",
            "/owners-admins/alerts-and-automation.html",
            "Vradar — alerts &amp; automation",
        ),
        (
            r"(<figcaption><strong>Actions Editor</strong> — [^<]+)",
            "/owners-admins/alerts-and-automation.html",
            "Vradar — alerts &amp; automation",
        ),
        (
            r"(<figcaption><strong>Digital Signage</strong> — [^<]+)",
            "/owners-admins/digital-signage.html",
            "Digital signage",
        ),
        (
            r"(<figcaption><strong>MVR Group Details</strong> — [^<]+)",
            "/owners-admins/detections-individuals-persons.html",
            "Detections, individuals &amp; persons",
        ),
        (
            r"(<figcaption><strong>Media Upload</strong> — [^<]+)",
            "/owners-admins/media-management.html",
            "Media and collections",
        ),
        (
            r"(<figcaption><strong>Signage Android App</strong> — [^<]+)",
            "/owners-admins/digital-signage.html",
            "Digital signage",
        ),
    ]
    def _caption_inline(path: str, label: str) -> str:
        return (
            f' <span class="wiki-more-inline">'
            f"{_wiki_chip(_wiki_href(path))} "
            f"{_wiki_a(label, path)}"
            f"</span>"
        )

    for cap_re, path, label in caption_links:
        html, n = re.subn(
            cap_re + r"(</figcaption>)",
            r"\1" + _caption_inline(path, label) + r"\2",
            html,
            count=1,
        )
        if n != 1:
            pass

    # EL captions keep English <strong> titles; retry any still missing wiki chip.
    for strong, path, label in [
        ("Main Dashboard", "/what-is-eyenet/", "What is EyeNet"),
        ("Analytics Filters", "/owners-admins/analytics-and-reports.html", "Analytics and reports"),
        ("System Settings", "/owners-admins/users-and-roles.html", "User management / Settings"),
        ("Analytics Dashboard", "/owners-admins/analytics-and-reports.html", "Analytics and reports"),
        ("Detection Analytics", "/owners-admins/cameras-and-detection.html", "Cameras and detection"),
        ("Camera Management", "/owners-admins/cameras-and-detection.html", "Cameras and detection"),
        ("Triggers Management", "/owners-admins/alerts-and-automation.html", "Vradar — alerts &amp; automation"),
        ("Actions Editor", "/owners-admins/alerts-and-automation.html", "Vradar — alerts &amp; automation"),
        ("Digital Signage", "/owners-admins/digital-signage.html", "Digital signage"),
        ("MVR Group Details", "/owners-admins/detections-individuals-persons.html", "Detections, individuals &amp; persons"),
        ("Media Upload", "/owners-admins/media-management.html", "Media and collections"),
        ("Signage Android App", "/owners-admins/digital-signage.html", "Digital signage"),
    ]:
        if f"<strong>{strong}</strong>" not in html:
            continue
        if re.search(
            rf"<figcaption><strong>{re.escape(strong)}</strong>.*?class=\"wiki-chip\"",
            html,
            flags=re.S,
        ):
            continue
        html = re.sub(
            rf"(<figcaption><strong>{re.escape(strong)}</strong>.*?)(</figcaption>)",
            r"\1" + _caption_inline(path, label) + r"\2",
            html,
            count=1,
            flags=re.S,
        )

    return html


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
            "innovation": "Simple yet powerful innovation",
            "with-eyenet": "Who uses EyeNet",
            "what": "What is EyeNet",
            "why": "Most Valuable Cases",
            "packages": "Commercial Packages",
        },
        "why_children": [
            ("hr-presence", "HR Presence"),
            ("mall", "Vision-adaptive Intelligent Signage"),
            ("cottage", "Family protection at home and remote"),
            ("home-care", "Home care · Virtual Ward"),
            ("security", "Security: night and Perimeter"),
            ("shipping", "Shipping and industrial"),
        ],
        "pkg_children": [
            ("b2c", "B2C Light"),
            ("b2b", "B2B Starter & Professional"),
            ("enterprise", "Enterprise"),
        ],
        "pkg_card_blurb": {
            "b2c": "Freemium + self-serve · $20–$300/month · event options $200–$1,200",
            "b2b": "Sales-assisted SaaS · $500–$3,000/month · multi-site ready",
            "enterprise": "Strategic accounts · $5,000+/month · unlimited scale · custom integrations",
        },
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
            ("Structure", "What · Cases · Who · Commercial Packages · Innovation"),
            ("Deployment", "On-Premises / VPN"),
        ],
        "cards": [
            ("01", "what", "EyeNet understands what it sees and acts on it automatically",
             "Edge intelligence, action automation, and hardware-bound scale."),
            ("02", "why", "Most Valuable Cases",
             "Featured use cases across HR, signage, family protection, home care, security, shipping, and industrial sites."),
            ("03", "with-eyenet", "Who uses EyeNet",
             "Strong outcomes for fleet, industrial sites, care, HR, security, family, and signage operators."),
            ("04", "packages", "Commercial Packages",
             "B2C Light, B2B Starter & Professional, and Enterprise motions."),
            ("05", "innovation", "Simple yet powerful innovation",
             "On-premises vision that decides and acts — plus freedom from the camera wall with targeted alerts."),
        ],
        "page_titles": {
            "innovation": "Simple yet powerful innovation",
            "with-eyenet": "Who uses EyeNet",
            "what": "EyeNet understands what it sees and acts on it automatically",
            "why": "Most Valuable Cases",
            "packages": "Commercial Packages — B2C · B2B · Enterprise",
        },
        "why_index_kicker": (
            "Featured use cases — where EyeNet replaces manual presence, "
            "blind nights, and disconnected sites with automatic vision."
        ),
        "pkg_index_kicker": (
            "Self-serve consumer volume, mid-market B2B contracts, "
            "and enterprise-scale deployments."
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
            "innovation": "Απλή κι όμως ισχυρή καινοτομία",
            "with-eyenet": "Ποιος χρησιμοποιεί το EyeNet",
            "what": "Τι είναι το EyeNet",
            "why": "Πιο πολύτιμες περιπτώσεις",
            "packages": "Εμπορικά πακέτα",
        },
        "why_children": [
            ("hr-presence", "HR Presence"),
            ("mall", "Vision-adaptive Intelligent Signage"),
            ("cottage", "Οικογενειακή προστασία στο σπίτι και εξ αποστάσεως"),
            ("home-care", "Home care · Virtual Ward"),
            ("security", "Ασφάλεια: νύχτα και περίμετρος"),
            ("shipping", "Ναυτιλία και βιομηχανία"),
        ],
        "pkg_children": [
            ("b2c", "B2C Light"),
            ("b2b", "B2B Starter & Professional"),
            ("enterprise", "Enterprise"),
        ],
        "pkg_card_blurb": {
            "b2c": "Freemium + self-serve · $20–$300/μήνα · event options $200–$1,200",
            "b2b": "Sales-assisted SaaS · $500–$3,000/μήνα · έτοιμο για multi-site",
            "enterprise": "Strategic accounts · $5,000+/μήνα · απεριόριστη κλίμακα · custom integrations",
        },
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
            ("Δομή", "Τι · Περιπτώσεις · Ποιος · Εμπορικά πακέτα · Καινοτομία"),
            ("Ανάπτυξη", "On-Premises / VPN"),
        ],
        "cards": [
            ("01", "what", "Το EyeNet κατανοεί ό,τι βλέπει και ενεργεί αυτόματα",
             "Edge νοημοσύνη, αυτοματοποίηση δράσης και κλίμακα με βάση το hardware."),
            ("02", "why", "Πιο πολύτιμες περιπτώσεις",
             "Επιλεγμένες περιπτώσεις χρήσης σε HR, signage, οικογενειακή προστασία, home care, ασφάλεια, ναυτιλία και βιομηχανία."),
            ("03", "with-eyenet", "Ποιος χρησιμοποιεί το EyeNet",
             "Δυνατά αποτελέσματα για στόλο, βιομηχανικούς χώρους, φροντίδα, HR, ασφάλεια, οικογένεια και signage."),
            ("04", "packages", "Εμπορικά πακέτα",
             "B2C Light, B2B Starter & Professional και Enterprise."),
            ("05", "innovation", "Απλή κι όμως ισχυρή καινοτομία",
             "On-premises όραση που αποφασίζει και ενεργεί — και ελευθερία από το camera wall με στοχευμένα alerts."),
        ],
        "page_titles": {
            "innovation": "Απλή κι όμως ισχυρή καινοτομία",
            "with-eyenet": "Ποιος χρησιμοποιεί το EyeNet",
            "what": "Το EyeNet κατανοεί ό,τι βλέπει και ενεργεί αυτόματα",
            "why": "Πιο πολύτιμες περιπτώσεις",
            "packages": "Εμπορικά πακέτα — B2C · B2B · Enterprise",
        },
        "why_index_kicker": (
            "Επιλεγμένες περιπτώσεις χρήσης — όπου το EyeNet αντικαθιστά χειροκίνητη παρουσία, "
            "τυφλές νύχτες και αποσυνδεδεμένους χώρους με αυτόματη όραση."
        ),
        "pkg_index_kicker": (
            "Self-serve καταναλωτικός όγκος, mid-market B2B συμβόλαια "
            "και enterprise κλίμακα."
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
        f'<a href="{p}/what/" data-title="{sections["what"]}"{cur("what")}>{sections["what"]}</a>',
        group("why", ui["why_children"], sections["why"]),
        f'<a href="{p}/with-eyenet/" data-title="{sections["with-eyenet"]}"{cur("with-eyenet")}>{sections["with-eyenet"]}</a>',
        group("packages", ui["pkg_children"], sections["packages"]),
        f'<a href="{p}/innovation/" data-title="{sections["innovation"]}"{cur("innovation")}>{sections["innovation"]}</a>',
    ]
    return "\n".join(links)


def header_nav(lang: str, section: str) -> str:
    ui = UI[lang]
    p = prefix(lang)
    items = [
        ("home", ui["home"], f"{p}/" if p else "/"),
        ("why", ui["sections"]["why"], f"{p}/why/"),
        ("packages", ui["sections"]["packages"], f"{p}/packages/"),
        ("innovation", ui["sections"]["innovation"], f"{p}/innovation/"),
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
        f'<a class="pager-link pager-prev" href="{href(lang, prev_path)}" '
        f'aria-label="{ui["prev"]}: {page_label(lang, prev_path)}">'
        f'<span class="pager-dir">{ui["prev"]}</span>'
        f'<span class="pager-title">{page_label(lang, prev_path)}</span></a>'
        if prev_path is not None
        else '<span class="pager-link pager-prev is-empty"></span>'
    )
    nxt = (
        f'<a class="pager-link pager-next" href="{href(lang, next_path)}" '
        f'aria-label="{ui["next"]}: {page_label(lang, next_path)}">'
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

    # Merged innovation page (brochure §01 + §02) — last in reading order
    innov_title = ui["page_titles"]["innovation"]
    innov_body = (
        page_shell_title(lang, "05", innov_title)
        + fix_asset_paths(sections["01"])
        + "\n"
        + fix_asset_paths(sections["02"])
    )
    write(
        base / "innovation" / "index.html",
        render_page(
            lang=lang,
            path="innovation",
            title=innov_title,
            body=innov_body,
            audience="innovation",
            section="innovation",
            wide=True,
        ),
    )
    search_entries.append(
        {
            "lang": lang,
            "url": f"{pfx}/innovation/",
            "title": innov_title,
            "section": ui["sections"]["innovation"],
            "sectionSlug": "innovation",
            "text": re.sub(r"<[^>]+>", " ", innov_body),
        }
    )

    # Remaining single pages: (brochure section key, slug, display num, wide)
    mapping = [
        ("04", "what", "01", True),
        ("03", "with-eyenet", "03", True),
    ]
    for src_num, slug, display_num, wide in mapping:
        title = ui["page_titles"][slug]
        body = page_shell_title(lang, display_num, title) + fix_asset_paths(sections[src_num])
        if slug == "what":
            extra = CONTENT_DIR / f"what-functionalities-{lang}.html"
            if extra.exists():
                body += "\n" + extra.read_text(encoding="utf-8")
            body = inject_wiki_read_more(
                relocate_what_edge_cards(relocate_what_lead_kicker(body)),
                lang,
            )
        if slug == "with-eyenet":
            body = apply_case_label_copy(apply_family_protection_copy(body, lang), lang)
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
        summary = apply_family_protection_copy(sm.group(1), lang)
    why_body = (
        page_shell_title(lang, "02", ui["page_titles"]["why"])
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

    for i, (child, label) in enumerate(ui["why_children"]):
        persona_html = personas[WHY_PERSONA_INDEX[child]]
        override_name = {
            "cottage": f"why-cottage-{lang}.html",
            "mall": f"why-mall-{lang}.html",
            "shipping": f"why-shipping-{lang}.html",
        }.get(child)
        if override_name:
            override = CONTENT_DIR / override_name
            if override.exists():
                persona_html = override.read_text(encoding="utf-8")
            elif child == "cottage":
                persona_html = apply_family_protection_copy(persona_html, lang)
        else:
            persona_html = apply_case_label_copy(persona_html, lang)
            # Keep display numbers aligned with reading order.
            persona_html = re.sub(
                r'(<h4><span class="n">)\d+(</span>)',
                rf"\g<1>{i + 1}\2",
                persona_html,
                count=1,
            )
        body = (
            page_shell_title(lang, "02", label)
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
        f"<span>{ui['pkg_card_blurb'][child]}</span></a>"
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
        page_shell_title(lang, "04", ui["page_titles"]["packages"])
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
        body = page_shell_title(lang, "04", label) + normalize_package_addressable_pockets(
            fix_asset_paths(block), lang
        )
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
    sync_print_pages()
    write_legacy_redirects()


def write_legacy_redirects() -> None:
    """Point old Competition breaker / Freedom URLs at the merged innovation page."""
    targets = [
        (ROOT / "competition-breaker" / "index.html", "/innovation/"),
        (ROOT / "freedom" / "index.html", "/innovation/"),
        (ROOT / "el" / "competition-breaker" / "index.html", "/el/innovation/"),
        (ROOT / "el" / "freedom" / "index.html", "/el/innovation/"),
    ]
    for path, dest in targets:
        path.parent.mkdir(parents=True, exist_ok=True)
        write(
            path,
            (
                "<!DOCTYPE html><html lang=\"en\"><head>"
                f'<meta charset="utf-8"><meta http-equiv="refresh" content="0;url={dest}">'
                f'<link rel="canonical" href="{dest}">'
                f"<title>Redirect</title></head><body>"
                f'<p><a href="{dest}">Continue to Simple yet powerful innovation</a></p>'
                "</body></html>\n"
            ),
        )


PRINT_EXTRA_CSS = """
    .breaker-grid { grid-template-columns: 1fr 1fr; }
    .notify > p + p { margin-top: 8px; }
    .func-gallery {
      display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0 18px;
    }
    .func-gallery figure {
      margin: 0; background: var(--band); break-inside: avoid; page-break-inside: avoid;
    }
    .func-gallery img {
      display: block; width: 100%; height: 110px; object-fit: cover; object-position: top center;
      background: #0f172a;
    }
    .func-gallery figcaption {
      padding: 8px 10px 10px; font-size: 8pt; color: var(--muted); line-height: 1.35;
    }
    .func-gallery figcaption strong {
      display: block; color: var(--ink); margin-bottom: 2px; font-size: 8.5pt;
    }
    .lead { color: var(--muted); }
"""


def sync_print_pages() -> None:
    """Rebuild printable brochure pages from source + inject What functionalities."""
    for lang, src in (("en", SRC_EN), ("el", SRC_EL)):
        html = src.read_text(encoding="utf-8")
        html = html.replace(
            'src="../../../product/logos/svg/eyenet-dark.svg"',
            'src="/assets/eyenet-dark.svg"',
        )
        html = html.replace('src="assets/', 'src="/assets/images/')

        if lang == "en":
            toolbar = """  <div class="no-print toolbar">
    <div>
      <p><a href="/">← Back to EyeNet Value</a> · Printable EN brochure</p>
      <p style="margin-top:4px">Use your browser’s Print dialog and choose <strong>Save as PDF</strong>.</p>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
      <a href="/el/print/" style="color:var(--brand);font-weight:600;text-decoration:none">EL version</a>
      <button type="button" onclick="window.print()">Print / Save as PDF</button>
    </div>
  </div>"""
        else:
            toolbar = """  <div class="no-print toolbar">
    <div>
      <p><a href="/el/">← Πίσω στο EyeNet Αξία</a> · Εκτυπώσιμη έκδοση EL</p>
      <p style="margin-top:4px">Χρησιμοποιήστε Print και επιλέξτε <strong>Save as PDF</strong>.</p>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
      <a href="/print/" style="color:var(--brand);font-weight:600;text-decoration:none">EN version</a>
      <button type="button" onclick="window.print()">Εκτύπωση / Αποθήκευση PDF</button>
    </div>
  </div>"""

        html = re.sub(
            r'  <div class="no-print(?: toolbar)?">.*?</div>\n',
            toolbar + "\n",
            html,
            count=1,
            flags=re.S,
        )

        if "</style>" in html and ".func-gallery" not in html:
            html = html.replace("</style>", PRINT_EXTRA_CSS + "\n  </style>", 1)

        extra_path = CONTENT_DIR / f"what-functionalities-{lang}.html"
        if extra_path.exists():
            extra = extra_path.read_text(encoding="utf-8")
            # Expand What section before it closes (after Edge/Action/Scale cols).
            pattern = (
                r'(<section[^>]*(?:04 · What|04 · Τι)[^>]*>'
                r'.*?<div class="cols-3">.*?</div>\s*)'
                r'(</section>)'
            )
            updated, n = re.subn(
                pattern,
                rf"\1\n{extra}\n    \2",
                html,
                count=1,
                flags=re.S,
            )
            if n != 1:
                # Fallback: first section-num 04 block
                pattern2 = (
                    r'(<span class="section-num">04</span>.*?<div class="cols-3">.*?</div>\s*)'
                    r'(</section>)'
                )
                updated, n = re.subn(
                    pattern2,
                    rf"\1\n{extra}\n    \2",
                    html,
                    count=1,
                    flags=re.S,
                )
            if n != 1:
                raise SystemExit(f"Could not inject What functionalities into print ({lang})")
            html = inject_wiki_read_more(
                relocate_what_edge_cards(relocate_what_lead_kicker(updated)),
                lang,
            )

        heading = WHAT_HEADING[lang]
        html, n_title = re.subn(
            r'(<span class="section-num">04</span>\s*<h2>)(?:What|Τι)(</h2>)',
            rf"\1{heading}\2",
            html,
            count=1,
        )
        if n_title != 1:
            raise SystemExit(f"Could not rename What heading in print ({lang})")

        why_heading = WHY_HEADING[lang]
        html, n_why = re.subn(
            r'(<span class="section-num">05</span>\s*<h2>)(?:Why|Γιατί)(</h2>)',
            rf"\1{why_heading}\2",
            html,
        )
        if n_why < 1:
            raise SystemExit(f"Could not rename Why headings in print ({lang})")

        with_heading = WITH_HEADING[lang]
        html, n_with = re.subn(
            r'(<span class="section-num">03</span>\s*<h2>)(?:With EyeNet…|Με το EyeNet…)(</h2>)',
            rf"\1{with_heading}\2",
            html,
        )
        if n_with < 1:
            raise SystemExit(f"Could not rename With EyeNet headings in print ({lang})")

        pkg_heading = PACKAGES_HEADING[lang]
        html, n_pkg = re.subn(
            r'(<span class="section-num">06</span>\s*<h2>)(?:Packages — B2C · B2B · Enterprise|Πακέτα — B2C · B2B · Enterprise)(</h2>)',
            rf"\1{pkg_heading}\2",
            html,
        )
        if n_pkg < 1:
            raise SystemExit(f"Could not rename Packages headings in print ({lang})")

        innov_heading = INNOVATION_HEADING[lang]
        html, n_innov1 = re.subn(
            r'(<span class="section-num">01</span>\s*<h2>)(?:Why EyeNet is a competition breaker|Γιατί το EyeNet σπάει τον ανταγωνισμό)(</h2>)',
            rf"\1{innov_heading}\2",
            html,
        )
        if n_innov1 < 1:
            raise SystemExit(f"Could not rename Competition breaker headings in print ({lang})")
        html, n_innov2 = re.subn(
            r'<span class="section-num">02</span>\s*<h2>(?:You don.t watch cameras — they watch for you|Δεν κοιτάτε κάμερες — αυτές κοιτάνε για εσάς)</h2>',
            f'<span class="section-num">01</span><h2>{innov_heading}</h2>',
            html,
        )
        if n_innov2 < 1:
            raise SystemExit(f"Could not merge Freedom headings into innovation in print ({lang})")

        # Reading order: What · Cases · Who · Packages · Innovation
        html = reorder_print_sections(html, lang)
        html = apply_case_label_copy(apply_family_protection_copy(html, lang), lang)
        html = inject_print_case_overrides(html, lang)
        html = normalize_package_addressable_pockets(html, lang)
        html = re.sub(
            r"(Dual go-to-market from the business plan:\s*|Διπλό go-to-market από το business plan:\s*)",
            "",
            html,
        )

        out = ROOT / ("el/print/index.html" if lang == "el" else "print/index.html")
        write(out, html)


def sort_why_print_sections(
    matches: list[re.Match[str]], lang: str
) -> list[re.Match[str]]:
    """HR → Vision signage → Family → Homecare → Security → Shipping and industrial."""
    patterns = [
        r"HR Presence",
        r"Mall marketing|Vision-adaptive Intelligent Signage",
        r"Cottage|Family protection|Εξοχικό|Οικογενειακή προστασία",
        r"Home care",
        r"Security personnel|Security: night|Προσωπικό ασφαλείας|Ασφάλεια:",
        r"Shipping|Ναυτιλία",
    ]
    remaining = list(matches)
    ordered: list[re.Match[str]] = []
    for pat in patterns:
        found = next((m for m in remaining if re.search(pat, m.group(0))), None)
        if not found:
            raise SystemExit(f"Missing why print persona for /{pat}/ ({lang})")
        ordered.append(found)
        remaining.remove(found)
    return ordered + remaining


def inject_print_case_overrides(html: str, lang: str) -> str:
    """Replace cottage/mall personas in print with content overrides when present."""
    overrides = [
        (
            f"why-cottage-{lang}.html",
            r'<div class="persona(?: alt)?">\s*<h4><span class="n">\d+</span>\s*'
            r"(?:Family protection at home and remote|Οικογενειακή προστασία στο σπίτι και εξ αποστάσεως|"
            r"Cottage &amp; remote living|Εξοχικό &amp; απομακρυσμένη διαβίωση)</h4>.*?"
            r"(?=</section>)",
        ),
        (
            f"why-mall-{lang}.html",
            r'<div class="persona(?: alt)?">\s*<h4><span class="n">\d+</span>\s*'
            r"(?:Vision-adaptive Intelligent Signage|Mall marketing studio[^<]*)</h4>.*?"
            r"(?=</section>)",
        ),
        (
            f"why-shipping-{lang}.html",
            r'<div class="persona(?: alt)?">\s*<h4><span class="n">\d+</span>\s*'
            r"(?:Shipping and industrial|Shipping — crew where they should be|"
            r"Ναυτιλία και βιομηχανία|Ναυτιλία — πλήρωμα εκεί που πρέπει)</h4>.*?"
            r"(?=</section>)",
        ),
    ]
    for fname, pattern in overrides:
        path = CONTENT_DIR / fname
        if not path.exists():
            continue
        body = path.read_text(encoding="utf-8").rstrip() + "\n"
        html, n = re.subn(pattern, body, html, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"Could not inject print override {fname} ({lang})")
    return html


def reorder_print_sections(html: str, lang: str) -> str:
    """Reorder print sections to wiki reading order, then renumber 01–05."""
    section_re = re.compile(r"<section\b[^>]*>.*?</section>", flags=re.S)
    sections = list(section_re.finditer(html))
    if not sections:
        raise SystemExit(f"No print sections found ({lang})")

    def sec_num(m: re.Match[str]) -> str | None:
        n = re.search(r'<span class="section-num">(\d+)</span>', m.group(0))
        return n.group(1) if n else None

    # Brochure keys after innovation merge (§02→§01): desired order before renumber.
    # what=04, why=05, who=03, packages=06, innovation=01
    order_keys = ["04", "05", "03", "06", "01"]
    by_num: dict[str, list[re.Match[str]]] = {}
    for m in sections:
        n = sec_num(m)
        if n:
            by_num.setdefault(n, []).append(m)
    for key in order_keys:
        if key not in by_num:
            raise SystemExit(f"Missing print section {key} ({lang})")

    by_num["05"] = sort_why_print_sections(by_num["05"], lang)

    ordered = [m for key in order_keys for m in by_num[key]]
    # Display: what→01, why→02, who→03, packages→04, innovation→05
    renumber = {"04": "01", "05": "02", "03": "03", "06": "04", "01": "05"}
    rebuilt: list[str] = []
    why_persona_i = 0
    for m in ordered:
        block = m.group(0)
        n = sec_num(m)
        if n in renumber:
            block = block.replace(
                f'<span class="section-num">{n}</span>',
                f'<span class="section-num">{renumber[n]}</span>',
                1,
            )
        if n == "05" and re.search(r'<h4><span class="n">\d+</span>', block):
            why_persona_i += 1
            block = re.sub(
                r'(<h4><span class="n">)\d+(</span>)',
                rf"\g<1>{why_persona_i}\2",
                block,
                count=1,
            )
        rebuilt.append(block)

    start = sections[0].start()
    end = sections[-1].end()
    return html[:start] + "\n\n".join(rebuilt) + html[end:]


if __name__ == "__main__":
    main()
