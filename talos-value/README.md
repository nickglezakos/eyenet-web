# TalosVision Value wiki

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
