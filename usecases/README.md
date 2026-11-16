# EyeNet use cases wiki

Customer-facing slice of `value/`:

- Home
- What is EyeNet (no wiki deep-links)
- Most Valuable Cases (as in value)
- Who uses EyeNet (as in value)
- Commercial Packages (pricing marked indicative `*`; TAM / financial model / internal notes removed)

Not included: Innovation, financial TAM panels, wiki.eyenet-vision.com chips.

## Preview

```bash
cd usecases
python3 -m http.server 8769 --bind 127.0.0.1
# open http://127.0.0.1:8769/
```

## Sync note

Do **not** blindly rsync `value/` → `usecases/` after this trim — that would restore Innovation, wiki links, and financials. Re-apply this transform (or edit here) after pulling value updates.
