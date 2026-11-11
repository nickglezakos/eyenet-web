#!/usr/bin/env python3
"""Copy invest Typical use cases into value Most Valuable Cases overrides."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVEST = ROOT.parent / "invest"
PRIMER = INVEST / "content" / "eyenet-investor-primer.html"
CONTENT = ROOT / "content"
SITE_CSS = ROOT / "assets" / "site.css"
INVEST_CSS = INVEST / "assets" / "site.css"

MAP = {
    "wedge-hr": "why-hr-presence",
    "wedge-signage": "why-mall",
    "wedge-shop": "why-shop-floor",
    "wedge-family": "why-cottage",
    "wedge-care": "why-home-care",
    "wedge-security": "why-security",
    "wedge-shipping": "why-shipping",
}


def extract_cases(html: str) -> dict[str, str]:
    found = re.findall(
        r'(<article class="case-page" id="(wedge-[^"]+)".*?</article>)',
        html,
        flags=re.S,
    )
    return {wid: body.strip() + "\n" for body, wid in found}


def case_css_block() -> str:
    text = INVEST_CSS.read_text(encoding="utf-8")
    m = re.search(
        r"(/\* Where it pays — featured use cases.*?)\n/\* Point-to-point differentiators",
        text,
        flags=re.S,
    )
    if not m:
        raise SystemExit("Could not extract case CSS from invest site.css")
    return m.group(1).rstrip() + "\n"


def main() -> None:
    cases = extract_cases(PRIMER.read_text(encoding="utf-8"))
    if set(cases) != set(MAP):
        raise SystemExit(f"case id mismatch: {sorted(cases)} vs {sorted(MAP)}")

    for wid, stem in MAP.items():
        for lang in ("en", "el"):
            path = CONTENT / f"{stem}-{lang}.html"
            path.write_text(cases[wid], encoding="utf-8")
            print(f"wrote {path.name} ({len(cases[wid])} chars)")

    css = SITE_CSS.read_text(encoding="utf-8")
    block = case_css_block()
    marker = "/* Invest case-page UX (synced from invest) */"
    if marker in css:
        start = css.index(marker)
        css = css[:start].rstrip() + "\n\n" + marker + "\n" + block + "\n"
    else:
        css = css.rstrip() + "\n\n" + marker + "\n" + block + "\n"
    SITE_CSS.write_text(css, encoding="utf-8")
    print("updated site.css with case-page UX")


if __name__ == "__main__":
    main()
