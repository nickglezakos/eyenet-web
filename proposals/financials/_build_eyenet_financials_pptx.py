"""Build EyeNet Financials pitch deck (PPTX) from the print financials model.

Aligned to proposals/financials/print/index.html:
  Seed $2.5M · Accelerate (Series A) $5–7M · FTE · cash/runway · pricing → sources
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUT = r"D:\code\eyenet-web\proposals\financials\EyeNet Financials.pptx"
OUT_TMP = r"D:\code\eyenet-web\proposals\financials\EyeNet Financials.new.pptx"

NAVY = RGBColor(0x0F, 0x21, 0x42)
NAVY2 = RGBColor(0x1E, 0x3A, 0x5F)
CYAN = RGBColor(0x00, 0xD4, 0xFF)
AZURE = RGBColor(0x3B, 0x82, 0xF6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xE8, 0xEE, 0xF5)
MUTED = RGBColor(0x5B, 0x6B, 0x7C)
INK = RGBColor(0x1A, 0x23, 0x32)
GREEN = RGBColor(0x0B, 0x6E, 0x4F)
AMBER = RGBColor(0xB4, 0x53, 0x09)
LIGHT = RGBColor(0xF4, 0xF7, 0xFB)
LINE = RGBColor(0xD0, 0xD8, 0xE4)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = prs.slide_width, prs.slide_height
TOTAL = 24


def set_run(run, text, size=18, bold=False, color=INK, font="Calibri"):
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def add_text(shape, paragraphs):
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, p in enumerate(paragraphs):
        text = p.get("text", "")
        size = p.get("size", 16)
        bold = p.get("bold", False)
        color = p.get("color", INK)
        align = p.get("align", PP_ALIGN.LEFT)
        space_after = p.get("space_after", 6)
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.space_after = Pt(space_after)
        run = para.add_run()
        set_run(run, text, size=size, bold=bold, color=color)


def rect(slide, l, t, w, h, fill, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
    return s


def round_rect(slide, l, t, w, h, fill, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
    return s


def footer(slide, page):
    rect(slide, 0, Inches(7.15), W, Inches(0.35), NAVY)
    box = slide.shapes.add_textbox(Inches(0.5), Inches(7.18), Inches(10), Inches(0.28))
    add_text(
        box,
        [
            {
                "text": "EyeNet Vision  ·  Financials  ·  Confidential",
                "size": 10,
                "color": SOFT,
                "space_after": 0,
            }
        ],
    )
    num = slide.shapes.add_textbox(Inches(12.2), Inches(7.18), Inches(0.8), Inches(0.28))
    add_text(
        num,
        [
            {
                "text": f"{page}/{TOTAL}",
                "size": 10,
                "color": SOFT,
                "align": PP_ALIGN.RIGHT,
                "space_after": 0,
            }
        ],
    )


def header_band(slide, title, subtitle=None):
    rect(slide, 0, 0, W, Inches(1.15), NAVY)
    rect(slide, 0, Inches(1.15), W, Inches(0.06), CYAN)
    t = slide.shapes.add_textbox(Inches(0.55), Inches(0.28), Inches(11.5), Inches(0.5))
    add_text(t, [{"text": title, "size": 26, "bold": True, "color": WHITE, "space_after": 0}])
    if subtitle:
        s = slide.shapes.add_textbox(Inches(0.55), Inches(0.72), Inches(11.5), Inches(0.35))
        add_text(s, [{"text": subtitle, "size": 12, "color": CYAN, "space_after": 0}])


def blank_light(slide):
    rect(slide, 0, 0, W, H, LIGHT)


def kpi_card(slide, l, t, w, h, label, value, sub=None, accent=CYAN):
    round_rect(slide, l, t, w, h, WHITE, LINE)
    rect(slide, l, t, Inches(0.08), h, accent)
    lb = slide.shapes.add_textbox(l + Inches(0.25), t + Inches(0.18), w - Inches(0.4), Inches(0.3))
    add_text(lb, [{"text": label, "size": 11, "color": MUTED, "space_after": 0}])
    vb = slide.shapes.add_textbox(l + Inches(0.25), t + Inches(0.45), w - Inches(0.4), Inches(0.45))
    add_text(vb, [{"text": value, "size": 24, "bold": True, "color": NAVY, "space_after": 0}])
    if sub:
        sb = slide.shapes.add_textbox(l + Inches(0.25), t + Inches(0.95), w - Inches(0.4), Inches(0.4))
        add_text(sb, [{"text": sub, "size": 11, "color": MUTED, "space_after": 0}])


def table_block(slide, rows, y0, left=Inches(0.5), width=Inches(12.3), row_h=0.48, col_widths=None):
    """Simple table: rows[0] header, rest body. col_widths list of Inches or None (equal)."""
    n = len(rows[0])
    if col_widths is None:
        col_widths = [width / n] * n
    lefts = []
    x = left
    for w in col_widths:
        lefts.append(x)
        x += w
    rect(slide, left, y0, width, Inches(0.38), NAVY)
    for j, htxt in enumerate(rows[0]):
        tb = slide.shapes.add_textbox(lefts[j] + Inches(0.08), y0 + Inches(0.05), col_widths[j] - Inches(0.1), Inches(0.3))
        add_text(tb, [{"text": htxt, "size": 11, "bold": True, "color": WHITE, "space_after": 0}])
    for i, row in enumerate(rows[1:]):
        top = y0 + Inches(0.38) + Inches(i * row_h)
        bg = WHITE if i % 2 == 0 else SOFT
        rect(slide, left, top, width, Inches(row_h), bg, LINE)
        for j, cell in enumerate(row):
            tb = slide.shapes.add_textbox(
                lefts[j] + Inches(0.08), top + Inches(0.1), col_widths[j] - Inches(0.1), Inches(row_h - 0.12)
            )
            add_text(
                tb,
                [
                    {
                        "text": cell,
                        "size": 12,
                        "bold": j == 0,
                        "color": NAVY if j == 0 else INK,
                        "space_after": 0,
                    }
                ],
            )


# ---- 1 Cover ----
s = prs.slides.add_slide(prs.slide_layouts[6])
rect(s, 0, 0, W, H, NAVY)
rect(s, 0, Inches(5.9), W, Inches(1.6), NAVY2)
rect(s, 0, Inches(5.9), W, Inches(0.06), CYAN)
eyebrow = s.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11), Inches(0.4))
add_text(
    eyebrow,
    [
        {
            "text": "SEED $2.5M  ·  ACCELERATE $5–7M  ·  PRICING  ·  REVENUE  ·  PREREQUISITES",
            "size": 13,
            "bold": True,
            "color": CYAN,
            "space_after": 0,
        }
    ],
)
title = s.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(2.2))
add_text(
    title,
    [
        {"text": "EyeNet Financials", "size": 48, "bold": True, "color": WHITE, "space_after": 10},
        {
            "text": "Seed financial plan at $2.5M, compared on the same metrics to Accelerate",
            "size": 18,
            "color": SOFT,
            "space_after": 6,
        },
        {
            "text": "(Series A, $5–7M) — plus pricing, market, revenue path, and contract results.",
            "size": 18,
            "color": SOFT,
            "space_after": 0,
        },
    ],
)
meta = s.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.5), Inches(1.0))
add_text(
    meta,
    [
        {
            "text": "Seed ask $2.5M   ·   Accelerate $5–7M Series A   ·   Revenue path ~$1M → $8M → $26M",
            "size": 14,
            "color": SOFT,
            "space_after": 4,
        },
        {"text": "Confidential — for investor discussion", "size": 12, "color": CYAN, "space_after": 0},
    ],
)

# ---- 2 Agenda ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Contents", "Seed $2.5M · Accelerate (Series A) $5–7M · unit economics hold across both")
footer(s, 2)
items = [
    ("02", "Executive verdict", "Seed $2.5M · Accelerate $5–7M · capital path"),
    ("03", "Use of proceeds", "Same metrics · Seed vs Accelerate dollar compare"),
    ("04–05", "Speed, footprint & FTE", "Seed ~13.7 FTE · Accelerate ~33 FTE · combined 46.7"),
    ("06–07", "Accelerate & cash", "Series A terms · runway · ~$8.5M combined"),
    ("08–17", "Pricing → underwriting", "Packages · unit econ · market · scoreboard · failure modes"),
    ("18–19", "Competition answer", "Disruptive model · adaptable per vertical rival"),
]
for i, (num, title, sub) in enumerate(items):
    top = Inches(1.45) + Inches(i * 0.9)
    round_rect(s, Inches(0.55), top, Inches(12.2), Inches(0.8), WHITE, LINE)
    nbox = s.shapes.add_textbox(Inches(0.8), top + Inches(0.18), Inches(1.2), Inches(0.45))
    add_text(nbox, [{"text": num, "size": 18, "bold": True, "color": CYAN if i % 2 == 0 else AZURE, "space_after": 0}])
    tbox = s.shapes.add_textbox(Inches(2.1), top + Inches(0.12), Inches(10), Inches(0.55))
    add_text(
        tbox,
        [
            {"text": title, "size": 16, "bold": True, "color": NAVY, "space_after": 2},
            {"text": sub, "size": 12, "color": MUTED, "space_after": 0},
        ],
    )

# ---- 3 Executive verdict ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(
    s,
    "Executive verdict",
    "Single seed $2.5M · next round named Accelerate (Series A $5–7M) — same unit economics, denser GTM",
)
footer(s, 3)

kpi_card(
    s,
    Inches(0.5),
    Inches(1.45),
    Inches(6.0),
    Inches(2.35),
    "SEED ASK · ~13.7 FTE",
    "$2.5M",
    "Mkt 850 · Pers 550 · Sales/ft 450 · Tech 400 · Ops 250\nPeople ~$1.27M / non-people ~$1.23M · Q1–Q2 2026 · SAFE / note",
    CYAN,
)
kpi_card(
    s,
    Inches(6.8),
    Inches(1.45),
    Inches(6.0),
    Inches(2.35),
    "ACCELERATE (SERIES A)",
    "$5–7M",
    "Sales $2.5M · Mkt $1.5M · Product $1.2M · Runway $0.8M (at $6M mid)\nPre $20–30M · Q3–Q4 2026 · Preferred · ~33 FTE",
    GREEN,
)

path = [
    ("Seed $2.5M", "launch · pilots · footprint"),
    ("Accelerate $5–7M", "Series A · $20–30M pre"),
    ("~$1M → $8M → $26M", "2027–2029"),
    ("Exit $500M–$1B", "2029–2031"),
]
for i, (t, sub) in enumerate(path):
    left = Inches(0.5) + Inches(i * 3.2)
    fill = GREEN if i >= 2 else WHITE
    tc = WHITE if i >= 2 else NAVY
    sc = SOFT if i >= 2 else MUTED
    round_rect(s, left, Inches(4.05), Inches(3.0), Inches(1.15), fill, None if i >= 2 else LINE)
    tb = s.shapes.add_textbox(left + Inches(0.15), Inches(4.2), Inches(2.7), Inches(0.9))
    add_text(
        tb,
        [
            {"text": t, "size": 14, "bold": True, "color": tc, "space_after": 4},
            {"text": sub, "size": 11, "color": sc, "space_after": 0},
        ],
    )
    if i < 3:
        ar = s.shapes.add_textbox(left + Inches(2.95), Inches(4.4), Inches(0.3), Inches(0.4))
        add_text(ar, [{"text": "→", "size": 16, "bold": True, "color": CYAN, "space_after": 0}])

note = s.shapes.add_textbox(Inches(0.55), Inches(5.5), Inches(12.2), Inches(1.3))
add_text(
    note,
    [
        {
            "text": "Combined base case ~$8.5M ($2.5M seed + ~$6M Accelerate mid). Accelerate does not rewrite CAC, LTV, or payback.",
            "size": 13,
            "bold": True,
            "color": NAVY,
            "space_after": 6,
        },
        {
            "text": "Three motions hold across both rounds: B2C Light (CAC $20–30 · LTV:CAC ~30:1) · B2B Starter/Pro (retention 85–90% · payback 3–4 mo) · Enterprise (LTV ~$144K · CAC $3–5K · ~40:1).",
            "size": 12,
            "color": MUTED,
            "space_after": 0,
        },
    ],
)

# ---- 4 Use of proceeds Seed ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Use of proceeds — Seed $2.5M", "Denser sales/marketing + multi-site footprint in-seed · London representation")
footer(s, 4)
seed_cats = [
    ("Marketing", "$850K", "34%", CYAN),
    ("Personnel", "$550K", "22%", AZURE),
    ("Sales / footprint", "$450K", "18%", GREEN),
    ("Tech", "$400K", "16%", NAVY),
    ("Ops / R&D", "$250K", "10%", MUTED),
]
for i, (lab, amt, pct, accent) in enumerate(seed_cats):
    left = Inches(0.4) + Inches(i * 2.55)
    round_rect(s, left, Inches(1.5), Inches(2.4), Inches(2.8), WHITE, LINE)
    rect(s, left, Inches(1.5), Inches(2.4), Inches(0.12), accent)
    lb = s.shapes.add_textbox(left + Inches(0.15), Inches(1.8), Inches(2.1), Inches(0.5))
    add_text(lb, [{"text": lab, "size": 12, "color": MUTED, "space_after": 0}])
    ab = s.shapes.add_textbox(left + Inches(0.15), Inches(2.4), Inches(2.1), Inches(0.55))
    add_text(ab, [{"text": amt, "size": 26, "bold": True, "color": NAVY, "space_after": 0}])
    pb = s.shapes.add_textbox(left + Inches(0.15), Inches(3.15), Inches(2.1), Inches(0.4))
    add_text(pb, [{"text": pct, "size": 18, "bold": True, "color": accent, "space_after": 0}])

round_rect(s, Inches(0.5), Inches(4.6), Inches(12.3), Inches(2.2), WHITE, LINE)
rect(s, Inches(0.5), Inches(4.6), Inches(0.12), Inches(2.2), CYAN)
nb = s.shapes.add_textbox(Inches(0.85), Inches(4.75), Inches(11.7), Inches(1.9))
add_text(
    nb,
    [
        {"text": "What Seed buys & must prove", "size": 14, "bold": True, "color": NAVY, "space_after": 8},
        {
            "text": "Buys: denser sales/marketing + Greek + U.S. units + London representation (not a second R&D center).",
            "size": 13,
            "color": INK,
            "space_after": 6,
        },
        {
            "text": "Proof: 5–10 pilots · $50–100K ARR · 50-lead pipeline · 2–3 partners. Timing Q1–Q2 2026. Instrument: SAFE / convertible note.",
            "size": 13,
            "color": INK,
            "space_after": 6,
        },
        {"text": "Next: Accelerate (Series A) $5–7M.", "size": 13, "bold": True, "color": GREEN, "space_after": 0},
    ],
)

# ---- 5 Use of proceeds Accelerate + compare ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(
    s,
    "Use of proceeds — Accelerate $5–7M ($6M mid)",
    "Same metric frame as Seed · Sales / Marketing / Product / Runway",
)
footer(s, 5)

acc_cats = [
    ("Sales team", "$2.5M", "42%", GREEN),
    ("Marketing", "$1.5M", "25%", CYAN),
    ("Product", "$1.2M", "20%", AZURE),
    ("Runway", "$0.8M", "13%", MUTED),
]
for i, (lab, amt, pct, accent) in enumerate(acc_cats):
    left = Inches(0.5) + Inches(i * 3.2)
    round_rect(s, left, Inches(1.4), Inches(3.0), Inches(1.9), WHITE, LINE)
    rect(s, left, Inches(1.4), Inches(3.0), Inches(0.1), accent)
    lb = s.shapes.add_textbox(left + Inches(0.2), Inches(1.6), Inches(2.6), Inches(0.35))
    add_text(lb, [{"text": lab, "size": 12, "color": MUTED, "space_after": 0}])
    ab = s.shapes.add_textbox(left + Inches(0.2), Inches(2.05), Inches(2.6), Inches(0.5))
    add_text(ab, [{"text": amt, "size": 24, "bold": True, "color": NAVY, "space_after": 0}])
    pb = s.shapes.add_textbox(left + Inches(0.2), Inches(2.65), Inches(2.6), Inches(0.35))
    add_text(pb, [{"text": pct + " of mid", "size": 13, "bold": True, "color": accent, "space_after": 0}])

table_block(
    s,
    [
        ("Metric", "Seed $2.5M", "Accelerate mid", "Δ"),
        ("Marketing / demand", "$850K", "$1.5M", "+$650K"),
        ("Sales / GTM capacity", "$1.0M", "$2.5M", "+$1.5M"),
        ("Tech / product", "$400K", "$1.2M", "+$800K"),
        ("Ops / runway", "$250K", "$800K", "+$550K"),
        ("Total raise", "$2.5M", "$5–7M", "+$3.5M mid"),
    ],
    Inches(3.55),
    col_widths=[Inches(3.5), Inches(2.8), Inches(3.2), Inches(2.8)],
)

# ---- 6 Speed & footprint ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Speed framework & footprint", "Seed stands up GTM · Accelerate scales the same motions")
footer(s, 6)
table_block(
    s,
    [
        ("Bucket", "What Seed buys", "What Accelerate adds"),
        ("Sales coverage", "AE / SE / partner · Sales/ft line", "Enterprise AEs, SDRs, consultants ($2.5M)"),
        ("Marketing / CAC", "$850K demand + people", "$1.5M demand gen, content, events"),
        ("CS / pilots", "Deploy-to-value on any-camera", "CS tools inside product scaling"),
        ("Product", "Sentinel + packaging · Tech $400K", "Engineering expansion · Product $1.2M"),
        ("Footprint", "Greek + U.S. + London in seed", "Geographic expansion on Accelerate"),
        ("Working capital", "Edge-kit · Ops $250K", "Runway buffer $800K"),
    ],
    Inches(1.4),
    row_h=0.55,
    col_widths=[Inches(2.4), Inches(4.9), Inches(5.0)],
)
note = s.shapes.add_textbox(Inches(0.55), Inches(5.9), Inches(12.2), Inches(0.9))
add_text(
    note,
    [
        {
            "text": "Will not spend on: cloud-VMS rebuild · proprietary camera estate · second R&D center · per-camera license chase.",
            "size": 12,
            "color": MUTED,
            "space_after": 4,
        },
        {
            "text": "KPIs: Seed 5–10 pilots · $50–100K ARR · 50 leads · 2–3 partners  →  Accelerate entry ~$1M+ ARR · 50–75 B2B · path to ~200 / ~$8M.",
            "size": 12,
            "bold": True,
            "color": NAVY,
            "space_after": 0,
        },
    ],
)

# ---- 7 FTE Seed ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(
    s,
    "FTE granulation — Seed $2.5M → ~13.7 FTE",
    "Planning rates: Sales $82K · Marketing $76K · Eng $109K · CS $83K · Ops $100K",
)
footer(s, 7)
kpi_card(s, Inches(0.5), Inches(1.4), Inches(4.0), Inches(1.5), "TOTAL FTE", "13.7", "People $1.265M · Non-people $1.235M", CYAN)
kpi_card(s, Inches(4.7), Inches(1.4), Inches(4.0), Inches(1.5), "ENG + SALES", "4.5 + 4.5", "Core build + GTM capacity", AZURE)
kpi_card(s, Inches(8.9), Inches(1.4), Inches(4.0), Inches(1.5), "MKT · CS · OPS", "2.0 · 1.0 · 1.7", "Demand people + CS + ops", GREEN)

roles = [
    ("Eng", "4.5", "$109K"),
    ("Sales", "4.5", "$82K"),
    ("Marketing", "2.0", "$76K"),
    ("CS", "1.0", "$83K"),
    ("Ops", "1.7", "$100K"),
]
for i, (role, fte, rate) in enumerate(roles):
    left = Inches(0.5) + Inches(i * 2.55)
    round_rect(s, left, Inches(3.2), Inches(2.4), Inches(1.7), WHITE, LINE)
    rb = s.shapes.add_textbox(left + Inches(0.15), Inches(3.4), Inches(2.1), Inches(1.3))
    add_text(
        rb,
        [
            {"text": role, "size": 12, "color": MUTED, "space_after": 4},
            {"text": fte, "size": 28, "bold": True, "color": NAVY, "space_after": 4},
            {"text": rate + " / FTE", "size": 12, "color": MUTED, "space_after": 0},
        ],
    )
note = s.shapes.add_textbox(Inches(0.55), Inches(5.2), Inches(12.2), Inches(1.5))
add_text(
    note,
    [
        {
            "text": "Seed dollars → headcount via people shares (Personnel 100% · Marketing ~18% · Tech ~60% · Sales/ft ~55% · Ops ~50%).",
            "size": 13,
            "color": INK,
            "space_after": 6,
        },
        {
            "text": "Non-people: Marketing CAC $698K · Footprint $204K · Tech infra $182K · Ops/legal $150K (+ $1K personnel plug).",
            "size": 12,
            "color": MUTED,
            "space_after": 0,
        },
    ],
)

# ---- 8 FTE Accelerate + compare ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(
    s,
    "FTE — Accelerate ~33 · Combined 46.7",
    "Accelerate is incremental (does not include Seed). Roster at $6M mid of $5–7M ask.",
)
footer(s, 8)
kpi_card(s, Inches(0.5), Inches(1.35), Inches(4.0), Inches(1.4), "ACCELERATE FTE", "33.0", "People $2.87M · Non-people $3.13M", GREEN)
kpi_card(s, Inches(4.7), Inches(1.35), Inches(4.0), Inches(1.4), "SALES STEP-UP", "21.0", "vs Seed 4.5 · Δ +16.5 FTE", AZURE)
kpi_card(s, Inches(8.9), Inches(1.35), Inches(4.0), Inches(1.4), "COMBINED", "46.7", "Seed 13.7 + Accelerate 33.0", CYAN)

table_block(
    s,
    [
        ("Role family", "Seed", "Accelerate", "Δ", "Combined"),
        ("Product & Engineering", "4.5", "7.0", "+2.5", "11.5"),
        ("Sales & BD", "4.5", "21.0", "+16.5", "25.5"),
        ("Marketing (people)", "2.0", "4.0", "+2.0", "6.0"),
        ("Customer Success", "1.0", "1.0", "—", "2.0"),
        ("Operations & Finance", "1.7", "0*", "—", "1.7"),
        ("Total FTE", "13.7", "33.0", "+19.3", "46.7"),
    ],
    Inches(2.95),
    row_h=0.48,
    col_widths=[Inches(3.4), Inches(2.0), Inches(2.4), Inches(2.0), Inches(2.5)],
)
note = s.shapes.add_textbox(Inches(0.55), Inches(6.35), Inches(12.2), Inches(0.55))
add_text(
    note,
    [
        {
            "text": "* Accelerate Ops = 0 because the $800K Runway line is modeled 100% non-people WC buffer; Seed Ops ~1.7 already standing.",
            "size": 11,
            "color": MUTED,
            "space_after": 0,
        }
    ],
)

# ---- 9 Accelerate terms ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Accelerate (Series A) & capital path", "Named Series A · $5–7M after $2.5M seed · ~33 FTE at $6M mid")
footer(s, 9)
kpi_card(s, Inches(0.5), Inches(1.4), Inches(4.0), Inches(1.55), "SEED", "$2.5M", "Q1–Q2 2026 · SAFE / note", CYAN)
kpi_card(s, Inches(4.7), Inches(1.4), Inches(4.0), Inches(1.55), "ACCELERATE", "$5–7M", "Pre $20–30M · Q3–Q4 2026", GREEN)
kpi_card(s, Inches(8.9), Inches(1.4), Inches(4.0), Inches(1.55), "EXIT TARGET", "$500M–$1B", "2029–2031 · IPO / strategic", AZURE)

table_block(
    s,
    [
        ("Element", "Plan figure"),
        ("Target raise", "$5–7M (mid often $6M)"),
        ("Pre-money valuation", "$20–30M"),
        ("Dilution (illustrative)", "~20–25% at Accelerate"),
        ("Security", "Series A preferred stock"),
        ("Combined seed + Accelerate", "~$8.5M ($2.5M + ~$6M)"),
        ("Entry bar", "~$1M+ ARR · 50–75 B2B · 500–1,000 B2C"),
    ],
    Inches(3.2),
    row_h=0.48,
    col_widths=[Inches(4.5), Inches(7.8)],
)

# ---- 10 Cash & runway ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(
    s,
    "Cash & runway",
    "Seed funds ops until Accelerate closes · combined ~$8.5M through plan profitability",
)
footer(s, 10)

round_rect(s, Inches(0.5), Inches(1.4), Inches(12.3), Inches(1.15), WHITE, LINE)
rect(s, Inches(0.5), Inches(1.4), Inches(0.12), Inches(1.15), GREEN)
vb = s.shapes.add_textbox(Inches(0.85), Inches(1.55), Inches(11.7), Inches(0.9))
add_text(
    vb,
    [
        {"text": "Verdict", "size": 13, "bold": True, "color": GREEN, "space_after": 4},
        {
            "text": "No planned zero-cash gap: Seed bridge (~6–12 mo) reaches Accelerate; Accelerate adds ~18-month WC runway toward profitability. Missing Accelerate on time is the main cash-risk failure mode.",
            "size": 13,
            "color": INK,
            "space_after": 0,
        },
    ],
)

kpi_card(s, Inches(0.5), Inches(2.8), Inches(4.0), Inches(1.55), "SEED BURN (MID)", "~$200K/mo", "People ~$105K · all-in $150–250K", CYAN)
kpi_card(s, Inches(4.7), Inches(2.8), Inches(4.0), Inches(1.55), "SEED-ALONE RUNWAY", "~12 months", "At ~$200K/mo on $2.5M", AZURE)
kpi_card(s, Inches(8.9), Inches(2.8), Inches(4.0), Inches(1.55), "COMBINED RAISE", "~$8.5M", "Covers 2026 −$1.5M EBITDA year", GREEN)

table_block(
    s,
    [
        ("Year", "Revenue", "EBITDA", "Cash implication"),
        ("2026", "$1.04M", "−$1.5M", "Investment year — Seed + early Accelerate"),
        ("2027", "$8.09M", "+$0.5M", "Breakeven ~Q2 2027 — cash turns"),
        ("2028", "$26.15M", "+$7.6M", "Self-funding ops · positive FCF path"),
    ],
    Inches(4.6),
    row_h=0.52,
    col_widths=[Inches(1.8), Inches(2.4), Inches(2.4), Inches(5.7)],
)

# ---- 11 Pricing ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Commercial package pricing", "Three motions on one platform — no per-camera ceiling")
footer(s, 11)
pkgs = [
    (
        "B2C Light",
        "Freemium → self-serve",
        "$20–$300/mo",
        "Events $200–$1,200\nAvg MRR ~$50\nCAC $20–30 · LTV:CAC ~30:1\nPayback 1–2 mo",
        CYAN,
    ),
    (
        "B2B Starter / Pro",
        "Sales-assisted SaaS",
        "$500–$3,000/mo",
        "ACV path ~$12–36K/yr\nStarter $500–1K · Pro $1.5–3K\nMobile/wearable +40–60%\nRetention 85–90% · payback 3–4 mo",
        AZURE,
    ),
    (
        "Enterprise",
        "Strategic accounts",
        "$5,000+/mo",
        "Contracts $6K–$150K+/yr\nAvg ACV often $12–20K+\nLTV ~$144K · CAC $3–5K\nLTV:CAC ~40:1",
        GREEN,
    ),
]
for i, (name, how, price, body, accent) in enumerate(pkgs):
    left = Inches(0.45) + Inches(i * 4.25)
    round_rect(s, left, Inches(1.5), Inches(4.05), Inches(5.3), WHITE, LINE)
    rect(s, left, Inches(1.5), Inches(4.05), Inches(1.35), NAVY)
    rect(s, left, Inches(2.85), Inches(4.05), Inches(0.06), accent)
    n = s.shapes.add_textbox(left + Inches(0.25), Inches(1.6), Inches(3.55), Inches(0.9))
    add_text(
        n,
        [
            {"text": name, "size": 18, "bold": True, "color": WHITE, "space_after": 4},
            {"text": how, "size": 12, "color": CYAN, "space_after": 0},
        ],
    )
    p = s.shapes.add_textbox(left + Inches(0.25), Inches(3.1), Inches(3.55), Inches(0.45))
    add_text(p, [{"text": price, "size": 20, "bold": True, "color": NAVY, "space_after": 0}])
    b = s.shapes.add_textbox(left + Inches(0.25), Inches(3.65), Inches(3.55), Inches(2.8))
    paras = [{"text": "•  " + line, "size": 13, "color": INK, "space_after": 8} for line in body.split("\n")]
    add_text(b, paras)

# ---- 12 Unit economics ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Unit economics by motion", "Same CAC / LTV / payback on Seed and Accelerate")
footer(s, 12)
table_block(
    s,
    [
        ("Motion", "CAC", "LTV / ratio", "Payback / retention"),
        ("B2C", "$20–30", "LTV:CAC ~30:1", "1–2 mo"),
        ("B2B", "Sales-assisted", "Path ACV $12–36K", "Retention 85–90% · payback 3–4 mo"),
        ("Enterprise", "$3–5K", "LTV ~$144K · ~40:1", "Strategic tenure model"),
    ],
    Inches(1.5),
    row_h=0.7,
    col_widths=[Inches(2.5), Inches(2.8), Inches(3.5), Inches(3.5)],
)
round_rect(s, Inches(0.5), Inches(4.2), Inches(12.3), Inches(2.5), WHITE, LINE)
nb = s.shapes.add_textbox(Inches(0.75), Inches(4.4), Inches(11.8), Inches(2.1))
add_text(
    nb,
    [
        {"text": "Hold across rounds", "size": 14, "bold": True, "color": NAVY, "space_after": 8},
        {
            "text": "• Accelerate does not invent different customer math — it buys denser coverage of the same motions.",
            "size": 13,
            "color": INK,
            "space_after": 6,
        },
        {
            "text": "• Scarce object is paying B2B logos (not cheap B2C clicks). 2027’s 50 B2B are the hard win.",
            "size": 13,
            "color": INK,
            "space_after": 6,
        },
        {
            "text": "• Mix must richen: blended B2B ACV ~$13K → $22K → $28K as Pro/Enterprise share rises.",
            "size": 13,
            "color": INK,
            "space_after": 0,
        },
    ],
)

# ---- 13 Market ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Market size & reach", "Conservative EyeNet addressable slices · pockets [1]–[8] · TAM [9]–[12]")
footer(s, 13)
kpi_card(s, Inches(0.45), Inches(1.4), Inches(6.1), Inches(1.55), "B2C TAM (U.S.)", "$0.5–1.5B", "Target share 1–3% → ~$5–45M opportunity", CYAN)
kpi_card(
    s,
    Inches(6.8),
    Inches(1.4),
    Inches(6.1),
    Inches(1.55),
    "B2B / ENTERPRISE TAM (U.S.)",
    "$2–4B",
    "Target share 1–2% → ~$20–80M opportunity",
    AZURE,
)

# B2C pockets
round_rect(s, Inches(0.45), Inches(3.2), Inches(6.1), Inches(3.6), WHITE, LINE)
ht = s.shapes.add_textbox(Inches(0.65), Inches(3.35), Inches(5.7), Inches(0.35))
add_text(ht, [{"text": "B2C reach pockets", "size": 14, "bold": True, "color": NAVY, "space_after": 0}])
b2c = [
    "~52K marketing consulting [1]",
    "~87M owner-occupied homes [2]",
    "~0.8M U.S. Airbnb hosts [3]",
    "~8K contract security cos. [4]",
    "~1.0M+ retail · ~0.6M restaurants [5][6]",
]
bb = s.shapes.add_textbox(Inches(0.65), Inches(3.8), Inches(5.7), Inches(2.8))
add_text(bb, [{"text": "•  " + x, "size": 13, "color": INK, "space_after": 8} for x in b2c])

round_rect(s, Inches(6.8), Inches(3.2), Inches(6.1), Inches(3.6), WHITE, LINE)
ht = s.shapes.add_textbox(Inches(7.0), Inches(3.35), Inches(5.7), Inches(0.35))
add_text(ht, [{"text": "B2B / Enterprise", "size": 14, "bold": True, "color": NAVY, "space_after": 0}])
b2b = [
    "~8K contract security [4]",
    "~99K public K–12 schools [7]",
    "~38K warehousing & storage [8]",
    "Segment map mid: retail $18M · security $9M · education $9M · CRE $18M",
    "Pocket counts = reach context, not near-term targets",
]
bb = s.shapes.add_textbox(Inches(7.0), Inches(3.8), Inches(5.7), Inches(2.8))
add_text(bb, [{"text": "•  " + x, "size": 13, "color": INK, "space_after": 8} for x in b2b])

# ---- 14 Revenue path ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Revenue path & derived mix", "Unit economics unchanged · ACV richens over time")
footer(s, 14)
years = [
    ("2027", "~$1M", "50 B2B", "~600 consumers", "First commercial proof", "~$12.8K", AZURE),
    ("2028", "~$8M", "200 B2B", "6,000+ consumers", "Breakeven", "~$22K", GREEN),
    ("2029", "~$26M", "500 B2B", "20,000+ consumers", "Solidly profitable", "~$28K", NAVY),
]
for i, (yr, rev, b2b, b2c, note, acv, accent) in enumerate(years):
    left = Inches(0.5) + Inches(i * 4.2)
    round_rect(s, left, Inches(1.5), Inches(4.0), Inches(4.2), WHITE, LINE)
    rect(s, left, Inches(1.5), Inches(4.0), Inches(0.7), accent)
    yb = s.shapes.add_textbox(left + Inches(0.25), Inches(1.6), Inches(3.5), Inches(0.5))
    add_text(yb, [{"text": yr, "size": 18, "bold": True, "color": WHITE, "space_after": 0}])
    rb = s.shapes.add_textbox(left + Inches(0.25), Inches(2.45), Inches(3.5), Inches(0.7))
    add_text(rb, [{"text": rev, "size": 36, "bold": True, "color": NAVY, "space_after": 0}])
    db = s.shapes.add_textbox(left + Inches(0.25), Inches(3.3), Inches(3.5), Inches(2.1))
    add_text(
        db,
        [
            {"text": b2b, "size": 16, "bold": True, "color": INK, "space_after": 4},
            {"text": b2c, "size": 16, "bold": True, "color": INK, "space_after": 10},
            {"text": note, "size": 13, "color": MUTED, "space_after": 10},
            {"text": f"Implied blended B2B ACV {acv}", "size": 13, "bold": True, "color": accent, "space_after": 0},
        ],
    )
note = s.shapes.add_textbox(Inches(0.5), Inches(5.95), Inches(12.3), Inches(0.9))
add_text(
    note,
    [
        {
            "text": "Derived mix: peel B2C at ~$50 MRR × users × 12; residual ÷ B2B logos = blended ACV. Exit target $500M–$1B (2029–2031).",
            "size": 13,
            "color": MUTED,
            "space_after": 0,
        }
    ],
)

# ---- 15 Prerequisites ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Financial prerequisites — contract scoreboard", "What marketing & sales must deliver")
footer(s, 15)
table_block(
    s,
    [
        ("Horizon", "Logos / contracts", "Revenue / ARR", "Deal shape"),
        ("Seed $2.5M", "5–10 pilots · 50 leads · 2–3 partners", "$50–100K ARR", "Starter-like B2B"),
        ("Accelerate entry", "50–75 B2B · 500–1,000 B2C", "~$1M+ ARR", "Path toward ~200"),
        ("2027", "50 B2B + ~600 B2C", "~$1M", "B2B ACV ~$12.8K"),
        ("2028", "200 B2B + 6,000+ B2C", "~$8M", "B2B ACV ~$22K"),
        ("2029", "500 B2B + 20,000+ B2C", "~$26M", "B2B ACV ~$28K"),
    ],
    Inches(1.45),
    row_h=0.7,
    col_widths=[Inches(2.4), Inches(4.5), Inches(2.8), Inches(2.6)],
)
note = s.shapes.add_textbox(Inches(0.55), Inches(6.2), Inches(12.2), Inches(0.7))
add_text(
    note,
    [
        {
            "text": "With 85–90% B2B retention, 2028 needs ~160–180 new logos (not just +150) and 2029 ~320–350 new logos to hit ending stock.",
            "size": 13,
            "color": MUTED,
            "space_after": 0,
        }
    ],
)

# ---- 16 Marketing & sales capacity ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Marketing spend & sales capacity", "CAC capacity · scarce objects · FTE productivity")
footer(s, 16)

round_rect(s, Inches(0.45), Inches(1.5), Inches(6.1), Inches(5.3), WHITE, LINE)
rect(s, Inches(0.45), Inches(1.5), Inches(6.1), Inches(0.55), NAVY)
ht = s.shapes.add_textbox(Inches(0.7), Inches(1.58), Inches(5.6), Inches(0.4))
add_text(ht, [{"text": "Marketing must buy", "size": 16, "bold": True, "color": WHITE, "space_after": 0}])
body = s.shapes.add_textbox(Inches(0.7), Inches(2.3), Inches(5.6), Inches(4.2))
add_text(
    body,
    [
        {"text": "1. Fill 50-lead → AE pipeline for B2B", "size": 15, "bold": True, "color": NAVY, "space_after": 8},
        {"text": "2. Convert freemium → paid B2C @ ~$50 MRR", "size": 15, "bold": True, "color": NAVY, "space_after": 8},
        {
            "text": "3. Support land-and-expand (ACV $13→$22→$28K)",
            "size": 15,
            "bold": True,
            "color": NAVY,
            "space_after": 14,
        },
        {"text": "Program CAC capacity (approx.)", "size": 13, "bold": True, "color": MUTED, "space_after": 6},
        {"text": "Seed ~$698K program · Accelerate ~$1.2M demand residual", "size": 14, "color": INK, "space_after": 10},
        {"text": "2027’s 600 consumers ≈ ~$15K CAC @ $25 — cheap.", "size": 13, "color": INK, "space_after": 6},
        {
            "text": "2027’s 50 B2B are the scarce object — sales-assisted, 3–4 mo payback.",
            "size": 13,
            "color": INK,
            "space_after": 0,
        },
    ],
)

round_rect(s, Inches(6.8), Inches(1.5), Inches(6.1), Inches(5.3), WHITE, LINE)
rect(s, Inches(6.8), Inches(1.5), Inches(6.1), Inches(0.55), AZURE)
ht = s.shapes.add_textbox(Inches(7.05), Inches(1.58), Inches(5.6), Inches(0.4))
add_text(ht, [{"text": "Sales capacity (derived FTE)", "size": 16, "bold": True, "color": WHITE, "space_after": 0}])
body = s.shapes.add_textbox(Inches(7.05), Inches(2.3), Inches(5.6), Inches(4.2))
add_text(
    body,
    [
        {"text": "Seed → 4.5 Sales FTE + 1.0 CS", "size": 15, "bold": True, "color": NAVY, "space_after": 8},
        {"text": "Accelerate → 21.0 Sales FTE + 1.0 CS", "size": 15, "bold": True, "color": NAVY, "space_after": 8},
        {"text": "Combined when both live → ~25.5 Sales", "size": 15, "color": INK, "space_after": 14},
        {"text": "Illustrative productivity", "size": 13, "bold": True, "color": MUTED, "space_after": 6},
        {"text": "~3–5 new B2B logos / month per ramped AE", "size": 14, "color": INK, "space_after": 6},
        {"text": "toward 50 logos by 2027 (plus 2–3 partners).", "size": 14, "color": INK, "space_after": 12},
        {
            "text": "Accelerate parallelizes the same logo math — same ACV/CAC rules.",
            "size": 13,
            "color": MUTED,
            "space_after": 0,
        },
    ],
)

# ---- 17 Underwriting + failure modes ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Underwriting checklist & failure modes", "Five holds · what breaks the plan")
footer(s, 17)
checks = [
    ("01", "Price from the shelf", "B2C Lite · B2B Starter/Pro · Enterprise $5K+/mo"),
    ("02", "Unit economics hold", "CAC / LTV / payback unchanged Seed → Accelerate"),
    ("03", "Seed proof first", "$50–100K ARR · 5–10 pilots · 50 leads · 2–3 partners"),
    ("04", "Scale years", "$1M / $8M / $26M with 50→200→500 B2B"),
    ("05", "Contract quality rises", "Blended B2B ACV ~$13K → $22K → $28K · 85–90% retention"),
]
for i, (num, title, body) in enumerate(checks):
    top = Inches(1.35) + Inches(i * 0.7)
    round_rect(s, Inches(0.45), top, Inches(7.5), Inches(0.62), WHITE, LINE)
    nb = s.shapes.add_textbox(Inches(0.6), top + Inches(0.12), Inches(0.55), Inches(0.4))
    add_text(nb, [{"text": num, "size": 14, "bold": True, "color": CYAN, "space_after": 0}])
    tb = s.shapes.add_textbox(Inches(1.25), top + Inches(0.08), Inches(6.5), Inches(0.5))
    add_text(
        tb,
        [
            {"text": title, "size": 13, "bold": True, "color": NAVY, "space_after": 1},
            {"text": body, "size": 11, "color": MUTED, "space_after": 0},
        ],
    )

fails = [
    ("ARR gate miss", "Pilots without $50K+ ARR in-seed"),
    ("ACV too thin", "50 logos but ACV << $12K"),
    ("Churn > 10–15%", "Never compounds to 200 / 500"),
    ("B2C CAC blowout", "CAC > $20–30 or freemium fails"),
    ("Accelerate late", "Seed runway exhausted before Series A"),
]
for i, (title, body) in enumerate(fails):
    top = Inches(1.35) + Inches(i * 0.7)
    round_rect(s, Inches(8.15), top, Inches(4.7), Inches(0.62), WHITE, LINE)
    rect(s, Inches(8.15), top, Inches(0.1), Inches(0.62), AMBER)
    tb = s.shapes.add_textbox(Inches(8.45), top + Inches(0.08), Inches(4.2), Inches(0.5))
    add_text(
        tb,
        [
            {"text": title, "size": 12, "bold": True, "color": NAVY, "space_after": 1},
            {"text": body, "size": 11, "color": MUTED, "space_after": 0},
        ],
    )

note = s.shapes.add_textbox(Inches(0.55), Inches(5.1), Inches(12.2), Inches(1.7))
add_text(
    note,
    [
        {"text": "Why underwritable", "size": 14, "bold": True, "color": NAVY, "space_after": 6},
        {
            "text": "Products built (5/6 apps in beta) · TMA/Talos + NewGen signed · Deloitte Greece/EMEA groundwork · LG International hot lead · Seed then Accelerate on unchanged unit economics.",
            "size": 13,
            "color": INK,
            "space_after": 0,
        },
    ],
)

# ---- 18 Competition answer (after failure modes) ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(
    s,
    "Answer to failure modes — disruptive & adaptable",
    "Rivals win vertical slices · EyeNet’s model bends to each market without rewriting unit economics",
)
footer(s, 18)

round_rect(s, Inches(0.5), Inches(1.4), Inches(12.3), Inches(1.35), WHITE, LINE)
rect(s, Inches(0.5), Inches(1.4), Inches(0.12), Inches(1.35), GREEN)
thesis = s.shapes.add_textbox(Inches(0.85), Inches(1.55), Inches(11.7), Inches(1.1))
add_text(
    thesis,
    [
        {"text": "The competitive fact", "size": 13, "bold": True, "color": GREEN, "space_after": 4},
        {
            "text": "EyeNet has a disruptive model that is aggressively adaptable to any competition market’s specifics — "
            "same on-prem Detect → Decide → Act fabric, any IP camera, no per-camera tax — tuned per vertical rival without inventing a new CAC/LTV story.",
            "size": 14,
            "color": INK,
            "space_after": 0,
        },
    ],
)

answers = [
    ("ARR / ACV risk", "Land with the case that already has a paying rival — prove logos on the same shelf prices"),
    ("Churn / retention", "On-prem action + Matrix mesh = stickier ops truth than cloud-only vertical tools"),
    ("B2C CAC blowout", "Consumer motion stays cheap; denser B2B cases fund scale when freemium is noisy"),
    ("Accelerate timing", "One stack across nine cases → more paths to $50–100K ARR before Series A"),
]
for i, (title, body) in enumerate(answers):
    col = i % 2
    row = i // 2
    left = Inches(0.5) + Inches(col * 6.4)
    top = Inches(3.0) + Inches(row * 1.55)
    round_rect(s, left, top, Inches(6.15), Inches(1.4), WHITE, LINE)
    rect(s, left, top, Inches(6.15), Inches(0.08), CYAN if col == 0 else AZURE)
    tb = s.shapes.add_textbox(left + Inches(0.25), top + Inches(0.25), Inches(5.7), Inches(1.0))
    add_text(
        tb,
        [
            {"text": title, "size": 15, "bold": True, "color": NAVY, "space_after": 6},
            {"text": body, "size": 13, "color": MUTED, "space_after": 0},
        ],
    )

# ---- 19 Competition map by use case ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(
    s,
    "Competition by use case — one fabric, nine rivals",
    "Closest vertical competitor per case · none cover EyeNet’s across-case model",
)
footer(s, 19)
rivals = [
    ("HR presence", "Verkada"),
    ("Mall signage", "Quividi"),
    ("Shop floor", "RetailNext"),
    ("Home / away", "Ring"),
    ("Home care", "SafelyYou"),
    ("Night security", "LVT"),
    ("Shipping", "ShipIn"),
    ("Perimeter", "Senstar"),
    ("Smart city", "Genetec"),
]
for i, (case, rival) in enumerate(rivals):
    col = i % 3
    row = i // 3
    left = Inches(0.45) + Inches(col * 4.25)
    top = Inches(1.35) + Inches(row * 1.35)
    round_rect(s, left, top, Inches(4.05), Inches(1.22), WHITE, LINE)
    rect(s, left, top, Inches(0.1), Inches(1.22), GREEN if row == 2 else (AZURE if row == 1 else CYAN))
    tb = s.shapes.add_textbox(left + Inches(0.3), top + Inches(0.22), Inches(3.5), Inches(0.85))
    add_text(
        tb,
        [
            {"text": case, "size": 13, "bold": True, "color": NAVY, "space_after": 4},
            {"text": "Closest rival: " + rival, "size": 12, "color": MUTED, "space_after": 0},
        ],
    )

round_rect(s, Inches(0.45), Inches(5.55), Inches(12.4), Inches(1.35), WHITE, LINE)
rect(s, Inches(0.45), Inches(5.55), Inches(0.12), Inches(1.35), CYAN)
cta = s.shapes.add_textbox(Inches(0.8), Inches(5.7), Inches(11.8), Inches(1.1))
add_text(
    cta,
    [
        {"text": "CTA — feature analysis", "size": 12, "bold": True, "color": CYAN, "space_after": 4},
        {
            "text": "For the full per-rival feature comparison tables (EyeNet vs each closest competitor), "
            "see the EyeNet Value PDF — section Competition by use case (§06).",
            "size": 14,
            "bold": True,
            "color": NAVY,
            "space_after": 4,
        },
        {
            "text": "Print / Save as PDF from the Value brochure. Adapt the motion — keep the model.",
            "size": 12,
            "color": MUTED,
            "space_after": 0,
        },
    ],
)

# ---- 20 Jargon divider ----
s = prs.slides.add_slide(prs.slide_layouts[6])
rect(s, 0, 0, W, H, NAVY)
rect(s, 0, 0, W, Inches(0.08), CYAN)
t = s.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(2.5))
add_text(
    t,
    [
        {"text": "ADDENDUM", "size": 14, "bold": True, "color": CYAN, "space_after": 12},
        {"text": "Financial jargon in plain English", "size": 36, "bold": True, "color": WHITE, "space_after": 12},
        {
            "text": "For non-financial experts reading this deck or the companion print pack.",
            "size": 18,
            "color": SOFT,
            "space_after": 0,
        },
    ],
)
footer(s, 20)

# ---- 21 Jargon terms ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Jargon — money in, growth math, funding", "Plain-English terms used in this pack")
footer(s, 21)
terms = [
    ("ARR / MRR", "Yearly / monthly subscription run-rate"),
    ("ACV", "Typical yearly value of one B2B contract"),
    ("CAC / LTV", "Cost to win a customer · lifetime value"),
    ("Payback", "Months until payments cover CAC"),
    ("Retention / Churn", "Share who stay / leave"),
    ("Seed", "Early money to launch and prove first sales"),
    ("Accelerate", "This plan’s name for Series A ($5–7M)"),
    ("SAFE / note", "Cash in now; ownership % set later"),
    ("Pre-money", "Company value before new cash"),
    ("Dilution", "Existing owners’ % shrinks at a raise"),
    ("FTE", "One full-time person-year of capacity"),
    ("Runway", "Months you can operate with cash on hand"),
]
y0 = Inches(1.35)
for i, (term, meaning) in enumerate(terms):
    col = i % 3
    row = i // 3
    left = Inches(0.4) + Inches(col * 4.25)
    top = y0 + Inches(row * 1.35)
    round_rect(s, left, top, Inches(4.1), Inches(1.2), WHITE, LINE)
    tb = s.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.7), Inches(0.85))
    add_text(
        tb,
        [
            {"text": term, "size": 14, "bold": True, "color": NAVY, "space_after": 4},
            {"text": meaning, "size": 12, "color": MUTED, "space_after": 0},
        ],
    )

# ---- 22 Master tables ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Master tables", "Canonical dollar and FTE rollups")
footer(s, 22)
table_block(
    s,
    [
        ("Metric ($K)", "Seed $2.5M", "Accelerate $6M mid"),
        ("Marketing / demand", "850", "1,500"),
        ("Sales / GTM", "1,000", "2,500"),
        ("Tech / product", "400", "1,200"),
        ("Ops / runway", "250", "800"),
        ("Total", "2,500", "6,000 mid"),
    ],
    Inches(1.35),
    row_h=0.42,
    col_widths=[Inches(4.5), Inches(3.9), Inches(3.9)],
)
table_block(
    s,
    [
        ("Round", "Eng", "Sales", "Mkt", "CS", "Ops", "FTE", "People $"),
        ("Seed $2.5M", "4.5", "4.5", "2.0", "1.0", "1.7", "13.7", "$1,265K"),
        ("Accelerate mid", "7.0", "21.0", "4.0", "1.0", "—", "33.0", "$2,872K"),
        ("Combined", "11.5", "25.5", "6.0", "2.0", "1.7", "46.7", "$4,137K"),
    ],
    Inches(4.3),
    row_h=0.48,
    col_widths=[Inches(2.4), Inches(1.2), Inches(1.3), Inches(1.1), Inches(1.0), Inches(1.1), Inches(1.4), Inches(2.8)],
)

# ---- 23 Sources ----
s = prs.slides.add_slide(prs.slide_layouts[6])
blank_light(s)
header_band(s, "Sources", "Public references behind TAM bands [9]–[12] and reach pockets [1]–[8]")
footer(s, 23)
sources = [
    ("[1]", "U.S. Census CBP 2023 · NAICS 541613", "~52K marketing consulting"),
    ("[2]", "U.S. Census ACS 2024", "~87M owner-occupied homes"),
    ("[3]", "CRE Daily / industry reports 2024", "~0.8M U.S. Airbnb hosts"),
    ("[4]", "NASCO 2024 white paper", "~8K U.S. contract security cos."),
    ("[5]", "U.S. Census Economic Census", "~1.0M+ retail establishments"),
    ("[6]", "CBP / NAICS 7225", "~0.6M restaurants / eating places"),
    ("[7]", "NCES SY 2024–25", "~99K public K–12 schools"),
    ("[8]", "IBISWorld 2024", "~38K warehousing & storage"),
    ("[9]", "Grand View — Video Analytics", "Global ~$12.7B (2024); NA ~⅓"),
    ("[10]", "MarketsandMarkets — U.S. Video Analytics", "~$2.3B (2023) → ~$5.7B (2028)"),
    ("[11]", "Grand View — U.S. Smart Home Cameras", "U.S. ~$3.68B (2024)"),
    ("[12]", "MarketsandMarkets — U.S. VSaaS", "U.S. ~$1.30B (2026) → ~$2.52B (2031)"),
]
y0 = Inches(1.35)
rect(s, Inches(0.4), y0, Inches(12.5), Inches(0.38), NAVY)
for j, htxt in enumerate(("Ref", "Source", "Figure used")):
    lefts = [Inches(0.5), Inches(1.4), Inches(7.8)]
    widths = [Inches(0.8), Inches(6.2), Inches(4.8)]
    tb = s.shapes.add_textbox(lefts[j], y0 + Inches(0.05), widths[j], Inches(0.28))
    add_text(tb, [{"text": htxt, "size": 11, "bold": True, "color": WHITE, "space_after": 0}])
for i, (ref, src, fig) in enumerate(sources):
    top = y0 + Inches(0.38) + Inches(i * 0.42)
    bg = WHITE if i % 2 == 0 else SOFT
    rect(s, Inches(0.4), top, Inches(12.5), Inches(0.42), bg, LINE)
    for j, cell in enumerate((ref, src, fig)):
        lefts = [Inches(0.5), Inches(1.4), Inches(7.8)]
        widths = [Inches(0.8), Inches(6.2), Inches(4.8)]
        tb = s.shapes.add_textbox(lefts[j], top + Inches(0.05), widths[j], Inches(0.32))
        add_text(
            tb,
            [
                {
                    "text": cell,
                    "size": 11,
                    "bold": j == 0,
                    "color": CYAN if j == 0 else INK,
                    "space_after": 0,
                }
            ],
        )

# ---- 24 Close ----
s = prs.slides.add_slide(prs.slide_layouts[6])
rect(s, 0, 0, W, H, NAVY)
rect(s, 0, 0, W, Inches(0.08), CYAN)
t = s.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.5), Inches(3.5))
add_text(
    t,
    [
        {"text": "Bottom line", "size": 16, "bold": True, "color": CYAN, "space_after": 12},
        {"text": "Seed $2.5M → Accelerate $5–7M", "size": 28, "bold": True, "color": WHITE, "space_after": 10},
        {"text": "Rising B2B book 50 → 200 → 500", "size": 22, "color": SOFT, "space_after": 6},
        {"text": "with rising ACV ~$13K → $22K → $28K,", "size": 20, "color": SOFT, "space_after": 6},
        {"text": "plus B2C 600 → 6K → 20K at ~$50 MRR —", "size": 20, "color": SOFT, "space_after": 6},
        {"text": "gated by 5–10 pilots and $50–100K ARR in seed.", "size": 20, "color": WHITE, "space_after": 0},
    ],
)
b = s.shapes.add_textbox(Inches(0.8), Inches(5.5), Inches(11.5), Inches(1.3))
add_text(
    b,
    [
        {
            "text": "Combined ~$8.5M · Seed ~13.7 FTE + Accelerate ~33 FTE → ~46.7 when both live.",
            "size": 15,
            "color": CYAN,
            "space_after": 8,
        },
        {
            "text": "Disruptive & adaptable vs vertical rivals — capital still buys scale on the same unit economics.",
            "size": 14,
            "color": SOFT,
            "space_after": 0,
        },
    ],
)
footer(s, 24)

actual = len(prs.slides)
if actual != TOTAL:
    print(f"WARNING: slide count {actual} != TOTAL {TOTAL}")

try:
    prs.save(OUT)
    print("Wrote", OUT)
except PermissionError:
    prs.save(OUT_TMP)
    print("Target locked — wrote", OUT_TMP)
    print("Close the PPTX and re-run, or replace the original with the .new file.")
print("Slides:", actual)
