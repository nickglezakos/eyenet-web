#!/usr/bin/env python3
"""Clone value/ into talos-value/ with TalosVision logo and branding."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "value"
OUT = REPO / "talos-value"
TALOS_ASSETS = REPO / "talos-usecases" / "assets"

TEXT_SUFFIXES = {".html", ".css", ".js", ".json", ".md", ".htaccess", ".txt"}

TALOS_SITE_CSS_EXTRA = """
/* TalosVision brand overrides */
:root {
  --brand: #3B82F6;
  --brand-dark: #0F2142;
  --cyan: #00D4FF;
}

.brand {
  gap: 10px;
}

.brand-logo {
  height: 32px;
  width: auto;
  max-width: 40px;
  object-fit: contain;
}

.brand-wordmark {
  font-family: Inter, "Segoe UI", system-ui, -apple-system, sans-serif;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1;
  color: #E8F4FD;
  white-space: nowrap;
}

.brand-wordmark .brand-vision {
  background: linear-gradient(90deg, #00D4FF, #3B82F6, #00D4FF);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}

.wiki-chip-logo {
  width: 18px !important;
  height: 18px !important;
  object-fit: contain;
}

.site-header {
  background: rgba(4, 13, 24, 0.96);
}
"""

PRINT_BRAND_CSS = """
    :root {
      --brand: #3B82F6;
      --brand-dark: #0F2142;
      --cyan: #00D4FF;
    }
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
    .cover-chip {
      border-color: rgba(0, 212, 255, 0.45);
      color: #E8F4FD;
      background: rgba(0, 212, 255, 0.12);
    }
    .section-num, .tag, .print-toc-card .num { color: var(--brand); }
    .no-print.toolbar button, .doc-nav-pdf { background: #0F2142 !important; }
    .cover {
      background: linear-gradient(165deg, #040D18 0%, #0F2142 48%, #163a66 100%) !important;
    }
"""

COVER_BRAND = """\
          <div class="cover-brand">
            <img src="/assets/talos-full-logo-ux-recolored.png" alt="" class="cover-logo-icon" />
            <span class="cover-wordmark">TALOS<span class="cover-vision">VISION</span></span>
            <span class="cover-chip">VALUE</span>
          </div>"""

HEADER_BRAND = """\
        <a class="brand" href="{home}" aria-label="TalosVision Value home">
          <img class="brand-logo" src="/assets/talos-full-logo-ux-recolored.png?v=talos" alt="">
          <span class="brand-wordmark">TALOS<span class="brand-vision">VISION</span></span>
        </a>"""


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if "scripts" in parts and path.name == "build_value_wiki.py":
        return True
    return False


def copy_tree() -> None:
    if OUT.exists():
        # Keep our builder; wipe regenerated outputs
        for child in OUT.iterdir():
            if child.name == "scripts":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        OUT.mkdir(parents=True)

    def ignore(directory: str, names: list[str]) -> set[str]:
        ignored: set[str] = set()
        # Don't copy the EyeNet rebuild script into the Talos tree root scripts clash
        if Path(directory).resolve() == (SRC / "scripts").resolve():
            ignored.add("build_value_wiki.py")
        return ignored

    # Copy everything except we manage scripts ourselves
    for item in SRC.iterdir():
        if item.name == "scripts":
            continue
        dest = OUT / item.name
        if item.is_dir():
            shutil.copytree(item, dest, ignore=ignore, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)


def rename_with_eyenet_dirs() -> None:
    for path in sorted(OUT.rglob("with-eyenet"), reverse=True):
        if path.is_dir():
            path.rename(path.with_name("with-talosvision"))


def protect(text: str) -> tuple[str, dict[str, str]]:
    """Shield URLs/paths that must keep eyenet substrings."""
    tokens: dict[str, str] = {}

    def stash(match: re.Match[str]) -> str:
        key = f"__PROTECT_{len(tokens)}__"
        tokens[key] = match.group(0)
        return key

    # Product wiki host + paths (keep working deep links)
    text = re.sub(r"https?://wiki\.eyenet-vision\.com[^\s\"'<>]*", stash, text)
    text = re.sub(r"wiki\.eyenet-vision\.com[^\s\"'<>]*", stash, text)
    # Existing asset filename
    text = text.replace(
        "/assets/images/functionalities/eyenet-security.jpg",
        "__EYENET_SECURITY_IMG__",
    )
    tokens["__EYENET_SECURITY_IMG__"] = "/assets/images/functionalities/eyenet-security.jpg"
    return text, tokens


def unprotect(text: str, tokens: dict[str, str]) -> str:
    for key, val in tokens.items():
        text = text.replace(key, val)
    return text


def rebrand_text(text: str) -> str:
    text, tokens = protect(text)

    reps = [
        ("nick@eyenet-vision.com", "info@talosgroup.eu"),
        ("eyenet-vision.com", "talosgroup.eu"),
        ("nick@talosgroup.eu", "info@talosgroup.eu"),
        ("EyeNet Value", "TalosVision Value"),
        ("EyeNet Vision", "TalosVision"),
        ("value.eyenet", "value.talos"),  # noop if already swapped
        ("/with-eyenet/", "/with-talosvision/"),
        ("with-eyenet/", "with-talosvision/"),
        ("What is EyeNet", "What is TalosVision"),
        ("Who uses EyeNet", "Who uses TalosVision"),
        ("Ποιος χρησιμοποιεί το EyeNet", "Ποιος χρησιμοποιεί το TalosVision"),
        ("Το EyeNet", "Το TalosVision"),
        ("το EyeNet", "το TalosVision"),
        ("του EyeNet", "του TalosVision"),
        ("τα EyeNet", "τα TalosVision"),
        ("EyeNet", "TalosVision"),
        ("Eyenet", "TalosVision"),
        # lowercase path/token leftovers (not protected)
        ("eyenet-dark.svg", "talos-full-logo-ux-recolored.png"),
        ("/assets/eyenet-dark.svg", "/assets/talos-full-logo-ux-recolored.png"),
        ('alt="EyeNet"', 'alt="TalosVision"'),
        ('alt=""', 'alt=""'),  # noop keep
        ("eyenet", "talosvision"),
    ]
    for old, new in reps:
        text = text.replace(old, new)

    text = text.replace("TalosVisionVision", "TalosVision")
    text = text.replace("talosvisionvision", "talosvision")
    text = text.replace("Visual: TalosVision", "Visual: talosgroup.eu")
    text = text.replace("Οπτικό: TalosVision", "Οπτικό: talosgroup.eu")

    return unprotect(text, tokens)


def rewrite_header_brand(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        home = "/el/" if '/el/' in m.group(0) or 'href="/el/"' in m.group(0) else "/"
        # Detect from surrounding file context via aria/home links in match
        if 'href="/el/"' in m.group(0) or "el/with" in m.group(0):
            home = "/el/"
        # Better: look at brand href in match
        hm = re.search(r'href="([^"]+)"', m.group(0))
        home = hm.group(1) if hm else "/"
        if home not in ("/", "/el/"):
            home = "/el/" if home.startswith("/el") else "/"
        return HEADER_BRAND.format(home=home)

    return re.sub(
        r'<a class="brand" href="[^"]*" aria-label="[^"]*">\s*'
        r'<img class="brand-logo" src="[^"]*" alt="[^"]*">\s*'
        r"</a>",
        repl,
        html,
        flags=re.S,
    )


def rewrite_print_cover(html: str) -> str:
    if 'class="cover"' not in html:
        return html
    if "</style>" in html and "--brand: #3B82F6" not in html:
        html = html.replace("</style>", PRINT_BRAND_CSS + "\n  </style>", 1)
    html = re.sub(
        r'<div class="cover-brand">\s*'
        r'<img src="/assets/[^"]+" alt="[^"]*"\s*/?>\s*'
        r'<span class="cover-chip">[^<]*</span>\s*'
        r"</div>",
        COVER_BRAND,
        html,
        count=1,
        flags=re.S,
    )
    # Also handle already-rebranded logo without chip structure variants
    html = re.sub(
        r'<div class="cover-brand">\s*'
        r'<img src="/assets/talos-full-logo-ux-recolored\.png[^"]*" alt="[^"]*"\s*/?>\s*'
        r'<span class="cover-chip">[^<]*</span>\s*'
        r"</div>",
        COVER_BRAND,
        html,
        count=1,
        flags=re.S,
    )
    return html


def patch_site_css(css: str) -> str:
    css = re.sub(r"--brand:\s*#[0-9a-fA-F]+;", "--brand: #3B82F6;", css, count=1)
    css = re.sub(r"--brand-dark:\s*#[0-9a-fA-F]+;", "--brand-dark: #0F2142;", css, count=1)
    css = re.sub(r"--cyan:\s*#[0-9a-fA-F]+;", "--cyan: #00D4FF;", css, count=1)
    if "brand-wordmark" not in css:
        css = css.rstrip() + "\n" + TALOS_SITE_CSS_EXTRA
    return css


def transform_file(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    text = rebrand_text(raw)

    if path.suffix == ".css" and path.name == "site.css":
        text = patch_site_css(text)
    if path.suffix == ".html":
        text = rewrite_header_brand(text)
        if "print" in path.parts and path.name == "index.html":
            text = rewrite_print_cover(text)
        text = text.replace(
            'href="/assets/talos-full-logo-ux-recolored.png?v=20261021p" type="image/svg+xml"',
            'href="/assets/talos-full-logo-ux-recolored.png?v=talos" type="image/png"',
        )
        text = text.replace(
            'href="/assets/talos-full-logo-ux-recolored.png?v=talos" type="image/svg+xml"',
            'href="/assets/talos-full-logo-ux-recolored.png?v=talos" type="image/png"',
        )

    if text != raw:
        path.write_text(text, encoding="utf-8")


def copy_logos() -> None:
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


def write_readme() -> None:
    (OUT / "README.md").write_text(
        """# TalosVision Value wiki

Talos-branded clone of the EyeNet `value/` wiki (EN/EL), with TalosVision logo,
wordmark, and palette from `talos-usecases` / talosvisionweb.

- English: `/`
- Greek: `/el/`
- Print EN: `/print/` · Print EL: `/el/print/`

## Rebuild

Re-copies from `value/` and reapplies branding:

```bash
python3 talos-value/scripts/build_talos_value.py
```

## Preview

```bash
cd talos-value
python3 -m http.server 8773
# open http://127.0.0.1:8773/
```

## Branding

- Logo: `assets/talos-full-logo-ux-recolored.png`
- Palette: `#00D4FF` cyan · `#3B82F6` azure · `#0F2142` navy
- Contact chrome: `talosgroup.eu` / `info@talosgroup.eu`
- Product wiki deep links to `wiki.eyenet-vision.com` are preserved
""",
        encoding="utf-8",
    )


def main() -> None:
    if not SRC.is_dir():
        raise SystemExit(f"Missing source: {SRC}")

    (OUT / "scripts").mkdir(parents=True, exist_ok=True)
    copy_tree()
    rename_with_eyenet_dirs()
    copy_logos()

    for path in OUT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".htaccess"}:
            continue
        if "scripts" in path.parts and path.name.startswith("build_talos"):
            continue
        transform_file(path)

    write_readme()
    print("wrote", OUT)
    # quick sanity
    home = (OUT / "index.html").read_text(encoding="utf-8")
    assert "TalosVision" in home
    assert "talos-full-logo-ux-recolored.png" in home
    assert "EyeNet" not in home
    print("home OK; logo OK; no EyeNet on home")


if __name__ == "__main__":
    main()
