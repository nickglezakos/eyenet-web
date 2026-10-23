# EyeNet Investor Primer wiki

English-only static investor site (same chrome/UX as the value wiki: sidebar, search, mobile menu, pager).

## Preview

```bash
cd invest
python3 -m http.server 8767
# open http://127.0.0.1:8767/
```

## Rebuild pages

After editing `content/eyenet-investor-primer.html`, `content/market-validation.html`, `content/reference-market-validation.html`, or `scripts/build_invest_wiki.py`:

```bash
python3 scripts/build_invest_wiki.py
```

**Market validation** (`/market-validation/`, section 07) is built from `content/market-validation.html`. FootfallCam source links live under **Addendum — Reference** (`/addendum-b/`).

## Printable PDF

`/print/` — browser **Print → Save as PDF**.

Source: `content/eyenet-investor-primer.html` (cloned from the business-plan value primer).

## Deploy

Cloudflare Pages project with root directory `invest`. English only at `/`.
