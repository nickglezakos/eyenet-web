# EyeNet use cases (print-only)

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
