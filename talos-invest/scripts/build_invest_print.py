#!/usr/bin/env python3
"""Build TalosVision-branded English print investor primer from invest/print."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "invest" / "print" / "index.html"
OUT = REPO / "talos-invest"
TALOS_ASSETS = REPO / "talos-usecases" / "assets"

TALOS_BRAND_CSS = """
    :root {
      --brand: #3B82F6;
      --brand-dark: #0F2142;
      --cyan: #00D4FF;
    }
    /* Icon + TALOSVISION wordmark (same pairing as talosvisionweb / talos-usecases) */
    .cover-brand {
      display: flex !important;
      align-items: center !important;
      gap: 14px !important;
      flex-wrap: wrap;
    }
    .cover-brand img,
    .cover-brand img.cover-logo,
    .cover-brand .cover-logo-icon {
      height: 52px !important;
      width: auto !important;
      max-width: 72px !important;
      object-fit: contain !important;
      filter: none !important;
      flex: 0 0 auto;
    }
    .cover-wordmark {
      font-family: Inter, "Segoe UI", system-ui, -apple-system, sans-serif;
      font-size: 28px;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1;
      color: #E8F4FD;
      white-space: nowrap;
    }
    .cover-wordmark .cover-vision {
      background: linear-gradient(90deg, #00D4FF, #3B82F6, #00D4FF);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      color: transparent;
    }
    .section-num,
    .tag,
    .print-toc-card .num {
      color: var(--brand);
    }
    .cover-chip {
      border-color: rgba(0, 212, 255, 0.45);
      color: #E8F4FD;
      background: rgba(0, 212, 255, 0.12);
    }
    .no-print.toolbar button,
    .doc-nav-pdf {
      background: #0F2142 !important;
    }
    .cover {
      background: linear-gradient(165deg, #040D18 0%, #0F2142 48%, #163a66 100%) !important;
    }
"""

COVER_BRAND = """\
          <div class="cover-brand">
            <img src="/assets/talos-full-logo-ux-recolored.png" alt="" class="cover-logo-icon" />
            <span class="cover-wordmark">TALOS<span class="cover-vision">VISION</span></span>
            <span class="cover-chip">Investor Primer</span>
          </div>"""

TOOLBAR = """\
  <div class="no-print toolbar">
    <div>
      <p>TalosVision Investor Primer · Print</p>
      <p style="margin-top:4px">Use your browser’s Print dialog and choose <strong>Save as PDF</strong>.</p>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
      <a href="/talos-usecases/" style="color:var(--brand);font-weight:600;text-decoration:none">Cases brochure</a>
      <button type="button" onclick="window.print()">Print / Save as PDF</button>
    </div>
  </div>
"""


def fix_toolbar(html: str) -> str:
    """Replace the broken/duplicated invest print toolbar with a clean Talos one."""
    html, n = re.subn(
        r'<div class="no-print toolbar">.*?</div>\s*'
        r'<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">.*?</div>\s*</div>',
        TOOLBAR.rstrip(),
        html,
        count=1,
        flags=re.S,
    )
    if n:
        return html
    # Fallback: first toolbar only
    return re.sub(
        r'<div class="no-print toolbar">.*?</div>',
        TOOLBAR.rstrip(),
        html,
        count=1,
        flags=re.S,
    )


def rewrite_cover_brand(html: str) -> str:
    return re.sub(
        r'<div class="cover-brand">\s*'
        r'<img src="/assets/[^"]+" alt="[^"]*"\s*/?>\s*'
        r'<span class="cover-chip">[^<]*</span>\s*'
        r"</div>",
        COVER_BRAND,
        html,
        count=1,
        flags=re.S,
    )


def apply_talos_branding(html: str) -> str:
    if "</style>" in html and "--brand: #3B82F6" not in html:
        html = html.replace("</style>", TALOS_BRAND_CSS + "\n  </style>", 1)

    html = fix_toolbar(html)
    html = rewrite_cover_brand(html)

    reps = [
        ("EyeNet Investor Primer — PDF", "TalosVision Investor Primer — PDF"),
        ("EyeNet investor primer", "TalosVision investor primer"),
        ("EyeNet Investor Primer", "TalosVision Investor Primer"),
        ("EyeNet Invest", "TalosVision Invest"),
        ("EyeNet Value", "TalosVision"),
        ("EyeNet Vision", "TalosVision"),
        # Email before bare domain (domain rewrite would leave nick@talosgroup.eu)
        ("nick@eyenet-vision.com", "info@talosgroup.eu"),
        ("eyenet-vision.com", "talosgroup.eu"),
        ("nick@talosgroup.eu", "info@talosgroup.eu"),
        ("EyeNet", "TalosVision"),
        ("eyenet", "talosvision"),
        ("Eyenet", "TalosVision"),
        ('/assets/eyenet-dark.svg"', '/assets/talos-full-logo-ux-recolored.png"'),
        ('alt="EyeNet"', 'alt="TalosVision"'),
        ("← EyeNet Invest", "TalosVision Investor Primer · Print"),
        ("value site", "cases brochure"),
    ]
    for old, new in reps:
        html = html.replace(old, new)

    html = html.replace("TalosVisionVision", "TalosVision")
    html = html.replace("talosvisionvision", "talosvision")
    # Keep FootfallCam company names intact if any accidental change (none expected)

    # Cover foot / contact already rewritten via domain/email reps
    html = re.sub(
        r'(<h1>)TalosVision investor primer(</h1>)',
        r"\1TalosVision investor primer\2",
        html,
        count=1,
    )
    return html


def copy_logo_assets() -> None:
    dest = OUT / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for name in (
        "talos-full-logo-ux-recolored.png",
        "talos-logo-ux-cyan.png",
        "talos-footer-logo.png",
        "talos-logo-dark-01.png",
    ):
        src = TALOS_ASSETS / name
        if src.is_file():
            shutil.copy2(src, dest / name)


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing source print page: {SRC}")

    OUT.mkdir(parents=True, exist_ok=True)
    html = apply_talos_branding(SRC.read_text(encoding="utf-8"))
    (OUT / "index.html").write_text(html, encoding="utf-8")
    copy_logo_assets()

    (OUT / "README.md").write_text(
        """# TalosVision investor primer (print-only)

English Talos-branded clone of the EyeNet `invest/print/` investor primer.
Same sections and content structure; TalosVision logo, wordmark, palette, and contact chrome from `talos-usecases` / talosvisionweb.

- English print: `/` (browser **Print → Save as PDF**)

## Rebuild

```bash
python3 talos-invest/scripts/build_invest_print.py
```

## Preview

```bash
cd talos-invest
python3 -m http.server 8772
# open http://127.0.0.1:8772/
```

## Branding source

Logos and palette from `talos-usecases/assets` (`#00D4FF` cyan, `#3B82F6` azure, `#0F2142` navy).
Source content: `invest/print/index.html`.
""",
        encoding="utf-8",
    )
    print("wrote", OUT / "index.html")
    print("assets →", OUT / "assets")


if __name__ == "__main__":
    main()
