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

## Deploy

Point the `value.eyenet-vision.com` host document root at this `value/` folder (same pattern as the product wiki). English is at `/`; Greek mirrors under `/el/`.
