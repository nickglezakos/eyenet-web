# EyeNet Most Valuable Cases (print-only)

Separate bilingual print site with **only** the Most Valuable Cases from `value/`.

- English: `/` (Print → Save as PDF)
- Greek: `/el/`

## Rebuild

After updating the value print brochure:

```bash
python3 value-cases/scripts/build_cases_print.py
```

## Preview

```bash
cd value-cases
python3 -m http.server 8767
# open http://127.0.0.1:8767/ and http://127.0.0.1:8767/el/
```

## Deploy

Cloudflare Pages project with root directory `value-cases` (separate from `value.eyenet-vision.com`).
