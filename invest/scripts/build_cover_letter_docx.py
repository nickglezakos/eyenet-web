#!/usr/bin/env python3
"""Build Talos Group letterhead investor cover letter for EyeNet (.docx / .doc)."""

from datetime import date
from pathlib import Path
import shutil
import subprocess

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "EyeNet_Investor_Cover_Letter_Talos_Group.docx"
LOGO = ROOT / "assets" / "talos-group-logo.png"
EYENET = ROOT / "assets" / "eyenet-logo-letterhead.png"

NAVY = RGBColor(0x04, 0x0D, 0x18)
CYAN = RGBColor(0x00, 0xA8, 0xCC)
INK = RGBColor(0x1A, 0x23, 0x32)
MUTED = RGBColor(0x4A, 0x55, 0x68)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HEADER_BG = "0A1628"


def set_run_font(run, *, size=11, bold=False, color=INK, italic=False):
    run.font.name = "Calibri"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def shade_cell(cell, hex_color: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tc_pr.append(shd)


def set_cell_borders(cell, color="C5D0DC", sz="4") -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:color"), color)
        borders.append(el)
    tc_pr.append(borders)


def add_h_line(paragraph, color="00A8CC", weight="24") -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), weight)
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    p_bdr.append(bottom)
    p_pr.append(p_bdr)


def body_p(doc, text="", *, size=9.5, bold=False, color=INK, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.18
    if text:
        r = p.add_run(text)
        set_run_font(r, size=size, bold=bold, color=color)
    return p


def section_title(doc, text: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    add_h_line(p, "00A8CC", "12")
    r = p.add_run(text.upper())
    set_run_font(r, size=9.5, bold=True, color=NAVY)
    return p


def main() -> None:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(1.35)
    section.bottom_margin = Cm(1.5)
    section.left_margin = Cm(1.9)
    section.right_margin = Cm(1.9)
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.header_distance = Cm(0.6)
    section.footer_distance = Cm(0.55)

    header = section.header
    header.is_linked_to_previous = False

    brand = header.paragraphs[0]
    brand.alignment = WD_ALIGN_PARAGRAPH.CENTER
    brand.paragraph_format.space_after = Pt(2)
    if LOGO.exists():
        brand.add_run().add_picture(str(LOGO), height=Cm(1.2))

    if EYENET.exists():
        eyenet_p = header.add_paragraph()
        eyenet_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        eyenet_p.paragraph_format.space_before = Pt(3)
        eyenet_p.paragraph_format.space_after = Pt(2)
        eyenet_p.add_run().add_picture(str(EYENET), height=Cm(0.42))

    meta = header.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.paragraph_format.space_before = Pt(2)
    meta.paragraph_format.space_after = Pt(0)
    set_run_font(
        meta.add_run("Confidential — Investor Correspondence  ·  philsot@talosgroup.eu"),
        size=8,
        bold=True,
        color=CYAN,
    )

    hline = header.add_paragraph()
    add_h_line(hline, "00A8CC", "18")
    hline.paragraph_format.space_before = Pt(3)
    hline.paragraph_format.space_after = Pt(0)

    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_h_line(fp, "C5D0DC", "8")
    set_run_font(
        fp.add_run(
            "Talos Group  ·  EyeNet Vision  ·  Confidential for investor discussion only  ·  © 2026"
        ),
        size=7.5,
        color=MUTED,
    )
    fp2 = footer.add_paragraph()
    fp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(
        fp2.add_run(
            "Illustrative financials are planned estimates based on market standards. "
            "Dilution from later rounds and actual ownership are not modeled."
        ),
        size=7,
        italic=True,
        color=MUTED,
    )

    body_p(doc, date(2026, 11, 7).strftime("%-d %B %Y"), size=9.5, color=MUTED, space_after=2)
    body_p(
        doc,
        "Ref: EyeNet — Seed investor introduction",
        size=9,
        bold=True,
        color=CYAN,
        space_after=8,
    )
    body_p(doc, "Dear Investor,", size=9.5, space_after=6)

    p = body_p(doc, space_after=8)
    set_run_font(p.add_run("EyeNet"), size=9.5, bold=True, color=NAVY)
    set_run_font(
        p.add_run(
            " is on-premises computer vision that turns ordinary cameras into vision nodes — "
            "they detect, decide, and act on site. Video stays local by default. We are raising "
        ),
        size=9.5,
        color=INK,
    )
    set_run_font(p.add_run("$500K"), size=9.5, bold=True, color=NAVY)
    set_run_font(
        p.add_run(" burn floor, with "),
        size=9.5,
        color=INK,
    )
    set_run_font(p.add_run("$1M"), size=9.5, bold=True, color=NAVY)
    set_run_font(p.add_run(" / "), size=9.5, color=INK)
    set_run_font(p.add_run("$2.5M"), size=9.5, bold=True, color=NAVY)
    set_run_font(
        p.add_run(
            " above that for speed. Same product and unit economics. Extra capital buys "
            "GTM and footprint — not a rebuild."
        ),
        size=9.5,
        color=INK,
    )

    section_title(doc, "Where EyeNet begins — where incumbents stop")
    p = body_p(doc, space_after=4)
    set_run_font(p.add_run("EyeNet Vision"), size=9.5, bold=True, color=NAVY)
    set_run_font(
        p.add_run(
            " has an aggressive business model: it begins where incumbents stop. "
            "Six wedges on one platform — any camera, hardware-bound scale, no per-camera "
            "blockers, detect → decide → act. Incumbents lack that model."
        ),
        size=9.5,
        color=INK,
    )
    for label, text in [
        (
            "Vision-adaptive intelligent signage",
            "Locked players / per-screen SaaS stop short of any-camera playlist scale — "
            "EyeNet switches age / gender / group in ms and proves impressions.",
        ),
        (
            "Home care / Virtual Ward",
            "Vitals-only RPM and cloud vision stop short of a safety layer — "
            "EyeNet turns fall / help-call / zone events into the clinical stack without shipping video.",
        ),
        (
            "Peace of mind at home — and away",
            "Cloud cams and guard contracts stop short for empty houses, cottages, and students living away — "
            "EyeNet gives presence + unknown-person alerts, phone pings only, footage on premises.",
        ),
        (
            "Shipping and industrial fleets",
            "Cloud VMS stops when the link drops — EyeNet keeps who’s onboard / in zone local; "
            "Matrix syncs on thin links across ships and plants.",
        ),
        (
            "HR presence · night & perimeter",
            "Badge sheets and per-camera seats stop short of coverage — EyeNet checks people in to the ERP/CRM "
            "and runs vigilance without 1:1 headcount.",
        ),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0.15)
        set_run_font(p.add_run(f"•  {label} — "), size=9.0, bold=True, color=NAVY)
        set_run_font(p.add_run(text), size=9.0, color=INK)

    section_title(doc, "Why EyeNet disrupts the market")
    for label, text in [
        (
            "Product",
            "Sovereignty + operational action vs. cloud storage, bandwidth, and recordings.",
        ),
        (
            "Cameras",
            "Any IP / Wi‑Fi / phone camera as a vision node on a ~16 GB PC vs. locked kits.",
        ),
        (
            "Licensing",
            "No per-camera licenses vs. per-camera seats that tax scale.",
        ),
        (
            "Outcome",
            "Detect → decide → act (mobile, email, webhooks, signage, gates, ERP/CRM) vs. passive VMS.",
        ),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0.15)
        set_run_font(p.add_run(f"•  {label} — "), size=9.5, bold=True, color=NAVY)
        set_run_font(p.add_run(text), size=9.5, color=INK)

    section_title(doc, "Why invest")
    for label, text in [
        (
            "1. Clear wedge",
            "Incumbents sell cloud storage on locked hardware; EyeNet sells sovereignty and action on cameras buyers already have.",
        ),
        (
            "2. Product already ships",
            "Five of six products beta-ready (Presence, Signage, Vradar, Gate, Matrix); Sentinel in active build. Capital buys selling what works.",
        ),
        (
            "3. Tight path to revenue",
            "U.S. TAM bands $0.5–1.5B B2C and $2–4B B2B/Enterprise; plan share → $5–45M B2C and $20–80M enterprise. Path: ~$1M (2027) → ~$8M (2028) → ~$26M (2029).",
        ),
        (
            "4. Seed ladder, not a rewrite",
            "Underwrite $500K ops first; $1M or $2.5M only accelerates the same motions. CAC, LTV, and payback hold across scenarios.",
        ),
        (
            "5. SaaS motions",
            "B2C Light $20–$300/mo · B2B Starter/Pro $500–$3,000/mo · Enterprise $5,000+/mo — partners already signed (TMA / Talos, NewGen).",
        ),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0.15)
        set_run_font(p.add_run(f"{label} — "), size=9.5, bold=True, color=NAVY)
        set_run_font(p.add_run(text), size=9.5, color=INK)

    section_title(doc, "Market · Revenue · Multiples · IRR")
    p = body_p(doc, space_after=4)
    set_run_font(
        p.add_run(
            "Illustrative 25% ownership on base-seed terms (~$3M pre). Exit on plan revenue at "
            "SaaS multiples 5× / 7× / 10×. Accelerate row uses the same ownership assumption "
            "for comparison; actual ownership scales with check size."
        ),
        size=8,
        italic=True,
        color=MUTED,
    )

    headers = [
        "Case",
        "U.S. TAM",
        "Plan revenue",
        "Exit multiple",
        "Stake value",
        "MOIC",
        "IRR",
    ]
    rows = [
        [
            "Base seed\n$1M · 2028 · Y3",
            "B2C $0.5–1.5B\nB2B $2–4B",
            "~$8M",
            "5× / 7× / 10×",
            "$10M / $14M / $20M",
            "~10× / ~14× / ~20×",
            "~115% / ~141% / ~171%",
        ],
        [
            "Accelerate\n$2.5M · 2029 · Y4",
            "B2C $0.5–1.5B\nB2B $2–4B",
            "~$26M",
            "5× / 7× / 10×",
            "$32.5M / $45.5M / $65M",
            "~13× / ~18× / ~26×",
            "~90% / ~107% / ~126%",
        ],
    ]

    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.paragraphs[0].clear()
        shade_cell(cell, HEADER_BG)
        set_cell_borders(cell, "0A1628", "4")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run_font(p.add_run(h), size=7, bold=True, color=WHITE)

    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = table.rows[ri + 1].cells[ci]
            cell.paragraphs[0].clear()
            shade_cell(cell, "F0F7FA" if ri % 2 == 0 else "FFFFFF")
            set_cell_borders(cell, "C5D0DC", "4")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci else WD_ALIGN_PARAGRAPH.LEFT
            bold = ci >= 5 or ci == 0
            set_run_font(
                p.add_run(val),
                size=7,
                bold=bold,
                color=NAVY if bold else INK,
            )

    body_p(doc, "", space_after=3)
    p = body_p(doc, space_after=8)
    set_run_font(
        p.add_run(
            "The full investor primer is available upon request. I would welcome a short call "
            "to walk through the seed ladder, use of proceeds, and the path from burn floor to Series A."
        ),
        size=9.5,
        color=INK,
    )

    body_p(doc, "Yours sincerely,", size=9.5, space_after=16)
    p = body_p(doc, space_after=2)
    set_run_font(p.add_run("Dr. Philip Sotiriades"), size=10.5, bold=True, color=NAVY)
    for line in (
        "EyeNet Vision  ·  Talos Group",
        "philsot@talosgroup.eu",
        "talosgroup.eu  ·  eyenet-vision.com",
    ):
        p = body_p(doc, space_after=0)
        set_run_font(p.add_run(line), size=9 if "@" in line or "·" in line else 9.5, color=MUTED)

    doc.save(OUT)
    print(f"wrote {OUT}")

    # Word-compatible .doc via macOS textutil when available
    textutil = shutil.which("textutil")
    if textutil:
        doc_out = OUT.with_suffix(".doc")
        subprocess.run(
            [textutil, "-convert", "doc", "-output", str(doc_out), str(OUT)],
            check=False,
        )
        if doc_out.exists():
            print(f"wrote {doc_out}")


if __name__ == "__main__":
    main()
