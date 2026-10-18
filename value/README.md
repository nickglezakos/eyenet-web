# EyeNet Value wiki

Static bilingual (EN default / EL) value site for `value.eyenet-vision.com`.

Wiki chrome matches [wiki.eyenet-vision.com](https://wiki.eyenet-vision.com/) (sidebar, search, mobile menu). Content UX and light palette follow the value brochure.

## Preview

```bash
cd value
python3 -m http.server 8766
# open http://127.0.0.1:8766/
```

## Rebuild pages

After editing brochure sources or `scripts/build_value_wiki.py`:

```bash
python3 scripts/build_value_wiki.py
```

## Printable PDF

- EN: `/print/` — browser **Print → Save as PDF**
- EL: `/el/print/`

Source brochure HTML is cloned from `ppl-meta-code/.../value/how-eyenet-changes-the-machine-vision-landscape*.html`.

## Deploy

Cloudflare Pages project with root directory `value`, custom domain `value.eyenet-vision.com`. English is at `/`; Greek mirrors under `/el/`.
