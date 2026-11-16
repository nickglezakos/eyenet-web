# TalosVision investor primer (print-only)

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
