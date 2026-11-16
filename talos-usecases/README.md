# TalosVision use cases (print-only)

Local Talos-branded clone of the EyeNet `usecases/` brochure.
Same structure (full-width visuals · one case per page) with TalosVision chrome from `talosvisionweb`.

- English: `/` (Print → Save as PDF)
- Greek: `/el/`

## Rebuild

```bash
python3 talos-usecases/scripts/build_cases_print.py
```

## Preview

```bash
cd talos-usecases
python3 -m http.server 8771
# open http://127.0.0.1:8771/ and http://127.0.0.1:8771/el/
```

## Branding source

Logos and palette from `/Documents/talosvisionweb` (`#00D4FF` cyan, `#3B82F6` azure, `#0F2142` navy).
