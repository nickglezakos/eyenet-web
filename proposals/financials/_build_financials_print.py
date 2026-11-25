#!/usr/bin/env python3
"""Build full detailed EyeNet Financials print HTML (invest/print UX)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSS = (ROOT / "_print_css_excerpt.css").read_text(encoding="utf-8")
OUT = ROOT / "print" / "index.html"
LOGO = "../../../invest/assets/eyenet-light.svg"

EXTRA_CSS = r"""
    /* No forced page breaks — continuous flow */
    .cover {
      break-after: auto !important;
      page-break-after: auto !important;
    }
    .section.page-start,
    .section.flow.page-start {
      break-before: auto !important;
      page-break-before: auto !important;
    }
    .section,
    .panel,
    .chart-block,
    .notify,
    .flow-node,
    .jargon-item,
    .print-toc-card,
    .group-cat,
    .def-block,
    table,
    tr,
    thead,
    tbody {
      break-inside: auto !important;
      page-break-inside: auto !important;
      break-after: auto !important;
      page-break-after: auto !important;
      break-before: auto !important;
      page-break-before: auto !important;
    }
    .print-toc { display: grid; gap: 10px; margin: 14px 0; }
    .print-toc-card {
      display: grid; grid-template-columns: 36px 1fr; gap: 10px; align-items: start;
      padding: 12px 14px; background: var(--band); border: 1px solid var(--line);
      text-decoration: none; color: inherit; break-inside: avoid;
    }
    .print-toc-card .num { color: var(--brand); font-weight: 800; font-size: 12px; }
    .print-toc-card strong { display: block; color: var(--brand-dark); font-size: 11pt; margin-bottom: 2px; }
    .print-toc-card span { color: var(--muted); font-size: 9pt; }
    .sheet { padding-bottom: 110px; }
    @media print { .sheet { padding-bottom: 0; } }
    .jargon-grid { display: grid; gap: 8px; margin: 12px 0; }
    @media (min-width: 700px) { .jargon-grid { grid-template-columns: 1fr 1fr; } }
    .jargon-item {
      padding: 10px 12px; background: var(--band); border: 1px solid var(--line);
      break-inside: avoid;
    }
    .jargon-item strong { display: block; margin-bottom: 4px; color: var(--brand-dark); }
    .jargon-item p { margin: 0; font-size: 9pt; }
    .flow-rail {
      display: flex; flex-wrap: wrap; gap: 8px; align-items: stretch; margin: 14px 0;
    }
    .flow-node {
      flex: 1 1 140px; min-width: 120px; padding: 12px 14px;
      background: var(--band); border: 1px solid var(--line); break-inside: avoid;
    }
    .flow-node.alt { background: var(--band-alt); }
    .flow-node.ok { border-color: #86efac; }
    .flow-node strong { display: block; color: var(--brand-dark); margin-bottom: 4px; font-size: 10pt; }
    .flow-node span { font-size: 9pt; color: var(--muted); }
    .flow-arrow {
      display: flex; align-items: center; color: var(--brand); font-weight: 700; font-size: 14px;
      padding: 0 2px;
    }
    .group-chart { display: grid; gap: 12px; margin: 12px 0 16px; }
    .group-cat { break-inside: avoid; }
    .group-cat > .cat-label {
      font-size: 9pt; font-weight: 700; color: var(--brand-dark); margin-bottom: 4px;
    }
    .mini-row {
      display: grid; grid-template-columns: 72px 1fr 52px; gap: 8px; align-items: center;
      margin: 3px 0; font-size: 8.5pt;
    }
    .mini-row .who { color: var(--muted); }
    .mini-row .track {
      height: 10px; background: #e2e8f0; border-radius: 2px; overflow: hidden;
    }
    .mini-row .fill {
      height: 100%; background: linear-gradient(90deg, #1e3a5f, #3b82c4);
    }
    .mini-row .fill.peak { background: linear-gradient(90deg, #0b6e4f, #1faa6e); }
    .mini-row .fill.burn { background: linear-gradient(90deg, #64748b, #94a3b8); }
    .mini-row .val { text-align: right; font-variant-numeric: tabular-nums; }
    .share-pies { display: grid; gap: 12px; margin: 12px 0; }
    @media (min-width: 800px) { .share-pies { grid-template-columns: 1fr 1fr 1fr; } }
    .def-block { margin: 10px 0 14px; break-inside: avoid; }
    .def-block h4 { margin: 0 0 4px; font-size: 10.5pt; color: var(--brand-dark); }
    .def-block p { margin: 0; font-size: 9.5pt; }
    h3.sub { margin-top: 22px; }
"""


def bars(rows, accent=False):
    """rows: list of (label, value_str, width_pct, peak?)"""
    cls = "bar-chart bar-chart-compact"
    if accent:
        cls += " bar-chart-accent"
    parts = [f'<div class="{cls}" role="img">']
    for label, value, width, *rest in rows:
        peak = " is-peak" if (rest and rest[0]) else ""
        parts.append(
            f'<div class="bar-row"><span class="bar-label">{label}</span>'
            f'<div class="bar-track"><div class="bar-fill{peak}" style="width:{width}%"></div></div>'
            f'<span class="bar-value">{value}</span></div>'
        )
    parts.append("</div>")
    return "\n".join(parts)


def group_bars(categories, series_max):
    """categories: [(cat, [(who, val, css_class), ...]), ...] val numeric for width."""
    out = ['<div class="group-chart">']
    for cat, series in categories:
        out.append('<div class="group-cat">')
        out.append(f'<div class="cat-label">{cat}</div>')
        for who, val, css in series:
            w = 0 if series_max <= 0 else min(100, round(100 * val / series_max))
            out.append(
                f'<div class="mini-row"><span class="who">{who}</span>'
                f'<div class="track"><div class="fill {css}" style="width:{w}%"></div></div>'
                f'<span class="val">{val}</span></div>'
            )
        out.append("</div>")
    out.append("</div>")
    return "\n".join(out)


NAV_JS = r"""
<script>
(function () {
  var pages = Array.prototype.slice.call(document.querySelectorAll(".sheet > section[data-nav-label]"));
  if (!pages.length) return;
  var prevBtn = document.querySelector(".doc-nav-prev");
  var nextBtn = document.querySelector(".doc-nav-next");
  var labelEl = document.querySelector(".doc-nav-label");
  var index = 0;

  function currentIndex() {
    var mid = window.scrollY + window.innerHeight * 0.28;
    var best = 0;
    for (var i = 0; i < pages.length; i++) {
      if (pages[i].offsetTop <= mid) best = i;
    }
    return best;
  }

  function sync() {
    index = currentIndex();
    var page = pages[index];
    labelEl.textContent = (index + 1) + " / " + pages.length + " · " + page.getAttribute("data-nav-label");
    prevBtn.disabled = index <= 0;
    nextBtn.disabled = index >= pages.length - 1;
  }

  function go(delta) {
    var next = Math.max(0, Math.min(pages.length - 1, currentIndex() + delta));
    pages[next].scrollIntoView({ behavior: "smooth", block: "start" });
  }

  prevBtn.addEventListener("click", function () { go(-1); });
  nextBtn.addEventListener("click", function () { go(1); });
  window.addEventListener("scroll", sync, { passive: true });
  window.addEventListener("resize", sync);
  sync();
})();
</script>
"""

# --- chart fragments ---
SEED_BARS = bars(
    [
        ("Marketing", "$850K", 100, True),
        ("Personnel", "$550K", 65),
        ("Sales / footprint", "$450K", 53),
        ("Tech", "$400K", 47),
        ("Ops / R&D", "$250K", 29),
    ]
)

ACCELERATE_BARS = bars(
    [
        ("Sales team", "$2.5M", 100, True),
        ("Marketing", "$1.5M", 60),
        ("Product", "$1.2M", 48),
        ("Runway", "$0.8M", 32),
    ],
    accent=True,
)

# Same-metric compare: Seed $2.5M vs Accelerate (Series A) at $6M mid of $5–7M
ROUND_COMPARE = group_bars(
    [
        ("Marketing / demand ($K)", [("Seed", 850, "burn"), ("Accelerate", 1500, "peak")]),
        ("Sales / GTM capacity ($K)", [("Seed", 1000, "burn"), ("Accelerate", 2500, "peak")]),
        ("Tech / product ($K)", [("Seed", 400, "burn"), ("Accelerate", 1200, "peak")]),
        ("Ops / runway ($K)", [("Seed", 250, "burn"), ("Accelerate", 800, "peak")]),
        ("Total raise ($K)", [("Seed", 2500, "burn"), ("Accelerate", 6000, "peak")]),
    ],
    6000,
)

FTE_RATE_BARS = bars(
    [("Sales", "$82K", 75), ("Marketing", "$76K", 70), ("Eng", "$109K", 100, True), ("CS", "$83K", 76), ("Ops", "$100K", 92)],
    accent=True,
)

FTE_SEED = bars(
    [
        ("Eng", "4.5", 100, True),
        ("Sales", "4.5", 100, True),
        ("Marketing", "2.0", 44),
        ("CS", "1.0", 22),
        ("Ops", "1.7", 38),
    ],
    accent=True,
)

# Accelerate $6M mid — same rates; people shares: Sales ~70%, Mkt ~20%, Product ~70%, Runway ~0%
FTE_ACCEL = bars(
    [
        ("Eng", "7.0", 33),
        ("Sales", "21.0", 100, True),
        ("Marketing", "4.0", 19),
        ("CS", "1.0", 5),
        ("Ops", "0", 0),
    ],
    accent=True,
)

FTE_COMPARE = group_bars(
    [
        ("Eng FTE", [("Seed", 4.5, "burn"), ("Accelerate", 7.0, "peak")]),
        ("Sales FTE", [("Seed", 4.5, "burn"), ("Accelerate", 21.0, "peak")]),
        ("Marketing people", [("Seed", 2.0, "burn"), ("Accelerate", 4.0, "peak")]),
        ("CS FTE", [("Seed", 1.0, "burn"), ("Accelerate", 1.0, "peak")]),
        ("Ops FTE", [("Seed", 1.7, "burn"), ("Accelerate", 0.0, "")]),
        ("Total FTE", [("Seed", 13.7, "burn"), ("Accelerate", 33.0, "peak")]),
    ],
    33,
)

B2C_PRICE = group_bars(
    [
        ("Home Security Lite", [("Low", 20, "burn"), ("High", 50, "peak")]),
        ("Signage Lite", [("Low", 30, "burn"), ("High", 100, "peak")]),
        ("Retail Compliance Lite", [("Low", 50, "burn"), ("High", 100, "peak")]),
        ("Event Security (per event)", [("Low", 200, "burn"), ("High", 1200, "peak")]),
    ],
    1200,
)

B2B_PRICE = group_bars(
    [
        ("Starter $/mo", [("Low", 500, "burn"), ("High", 1000, "peak")]),
        ("Professional $/mo", [("Low", 1500, "burn"), ("High", 3000, "peak")]),
    ],
    3000,
)

CAC_BARS = bars(
    [("B2C low", "$20", 1), ("B2C high", "$30", 1), ("Ent low", "$3K", 60), ("Ent high", "$5K", 100, True)]
)

TAM_OPP = bars(
    [("B2C low", "$5M", 6), ("B2C high", "$45M", 56), ("B2B/Ent low", "$20M", 25), ("B2B/Ent high", "$80M", 100, True)],
    accent=True,
)

SEG_MAP = bars(
    [("Large retail", "$18M mid", 100, True), ("Security", "$9M mid", 50), ("Education", "$9M mid", 50), ("CRE", "$18M mid", 100, True)]
)

REV_PATH = bars(
    [("2027", "~$1M", 4), ("2028", "~$8M", 31), ("2029", "~$26M", 100, True)],
    accent=True,
)

CUST_PATH = group_bars(
    [
        ("B2B customers", [("2027", 50, "burn"), ("2028", 200, ""), ("2029", 500, "peak")]),
        ("Consumer users", [("2027", 600, "burn"), ("2028", 6000, ""), ("2029", 20000, "peak")]),
    ],
    20000,
)

MIX_PATH = group_bars(
    [
        ("Derived B2C $M", [("2027", 0.36, "burn"), ("2028", 3.6, ""), ("2029", 12.0, "peak")]),
        ("Derived B2B+Ent $M", [("2027", 0.64, "burn"), ("2028", 4.4, ""), ("2029", 14.0, "peak")]),
    ],
    14,
)

B2B_STOCK = bars(
    [("Seed ARR gate ~", "8", 2), ("2027", "50", 10), ("2028", "200", 40), ("2029", "500", 100, True)]
)

ACV_PATH = bars(
    [("2027", "~$12.8K", 46), ("2028", "~$22K", 79), ("2029", "~$28K", 100, True)],
    accent=True,
)

RAISE_COMPARE = bars(
    [("Seed", "$2.5M", 42), ("Accelerate ($6M mid)", "$5–7M", 100, True)],
    accent=True,
)

PEOPLE_SEED = bars([("People $1.27M", "13.7 FTE", 51, True), ("Non-people", "$1.23M", 49)])
PEOPLE_ACCEL = bars([("People $2.87M", "33 FTE", 48, True), ("Non-people", "$3.13M", 52)], accent=True)

# Cash / runway (plan cash model — Investment Opportunity baseline)
EBITDA_BARS = bars(
    [("2026", "−$1.5M", 20), ("2027", "+$0.5M", 7), ("2028", "+$7.6M", 100, True)],
    accent=True,
)

CASH_BRIDGE = group_bars(
    [
        ("Capital in ($M)", [("Seed", 2.5, "burn"), ("Accelerate mid", 6.0, "peak"), ("Combined", 8.5, "")]),
        ("Cash need vs raise", [("2026 EBITDA gap", 1.5, "burn"), ("WC / runway pool", 5.6, ""), ("Total planned raise", 8.5, "peak")]),
    ],
    8.5,
)

MONTHLY_BURN = bars(
    [
        ("Seed people ~", "$105K/mo", 53),
        ("Seed all-in mid", "$200K/mo", 100, True),
        ("Seed alone runway", "~12 mo", 60),
    ]
)


body = f"""
  <div class="no-print toolbar">
    <p class="toolbar-back"><a href="../">← Financials</a></p>
    <button type="button" class="toolbar-pdf" onclick="window.print()">PDF</button>
  </div>
<div class="sheet">

  <!-- COVER -->
  <section class="cover" id="page-0" data-nav-label="Cover">
    <div>
      <div class="cover-top">
        <div class="cover-brand">
          <img class="cover-logo" src="{LOGO}" alt="EyeNet" width="168" height="42" />
          <span class="cover-chip">Financials</span>
        </div>
      </div>
      <p class="cover-eyebrow">Seed $2.5M · Accelerate $5–7M · Pricing · Revenue · Prerequisites</p>
      <h1>EyeNet financials</h1>
      <p class="cover-lead">Seed financial plan at <strong>$2.5M</strong>, compared on the same metrics to <strong>Accelerate</strong> (Series A, $5–7M) — plus pricing, market, revenue path, and the contract results marketing and sales must deliver.</p>
      <div class="cover-meta">
        <div><span>Document</span><strong>Financials</strong></div>
        <div><span>Seed ask</span><strong>$2.5M</strong></div>
        <div><span>Accelerate</span><strong>$5–7M Series A</strong></div>
        <div><span>Revenue path</span><strong>~$1M → $8M → $26M</strong></div>
      </div>
    </div>
    <div class="cover-foot">
      <span>eyenet-vision.com</span>
      <span>Confidential — for investor discussion</span>
    </div>
  </section>

  <!-- 01 TOC -->
  <section class="section flow" id="page-toc" data-nav-label="01 · Contents">
    <div class="section-head"><span class="section-num">01</span><h2>Contents</h2></div>
    <p class="page-lead">Seed ask is <strong>$2.5M</strong>. <strong>Accelerate</strong> is the Series A round at <strong>$5–7M</strong>. Unit economics hold across both rounds.</p>
    <div class="print-toc">
      <a class="print-toc-card" href="#page-2"><span class="num">02</span><div><strong>Executive verdict</strong><span>Seed $2.5M · Accelerate $5–7M · capital path</span></div></a>
      <a class="print-toc-card" href="#page-3"><span class="num">03</span><div><strong>Use of proceeds — Seed vs Accelerate</strong><span>Same metrics · dollar bars · compare</span></div></a>
      <a class="print-toc-card" href="#page-4"><span class="num">04</span><div><strong>Speed framework &amp; footprint</strong><span>Seed buys · KPIs · Greece / U.S. / London</span></div></a>
      <a class="print-toc-card" href="#page-5"><span class="num">05</span><div><strong>FTE granulation</strong><span>Seed $2.5M · Accelerate $5–7M · compare</span></div></a>
      <a class="print-toc-card" href="#page-6"><span class="num">06</span><div><strong>Accelerate &amp; capital path</strong><span>Series A $5–7M · growth years</span></div></a>
      <a class="print-toc-card" href="#page-cash"><span class="num">07</span><div><strong>Cash &amp; runway</strong><span>Will not run out of cash while operating</span></div></a>
      <a class="print-toc-card" href="#page-7"><span class="num">08</span><div><strong>Package pricing</strong><span>B2C Lite · B2B · Enterprise SKUs</span></div></a>
      <a class="print-toc-card" href="#page-8"><span class="num">09</span><div><strong>Unit economics</strong><span>CAC · LTV · payback · derived tenure</span></div></a>
      <a class="print-toc-card" href="#page-9"><span class="num">10</span><div><strong>Market size &amp; reach</strong><span>TAM · pockets · segment map</span></div></a>
      <a class="print-toc-card" href="#page-10"><span class="num">11</span><div><strong>Revenue path &amp; mix</strong><span>~$1M → $8M → $26M · derived ACV</span></div></a>
      <a class="print-toc-card" href="#page-11"><span class="num">12</span><div><strong>Financial prerequisites</strong><span>Contract scoreboard · retention math</span></div></a>
      <a class="print-toc-card" href="#page-12"><span class="num">13</span><div><strong>Marketing &amp; sales capacity</strong><span>CAC capacity · FTE productivity</span></div></a>
      <a class="print-toc-card" href="#page-13"><span class="num">14</span><div><strong>Underwriting checklist</strong><span>Holds · failure modes · playbook</span></div></a>
      <a class="print-toc-card" href="#page-14"><span class="num">15</span><div><strong>Jargon in plain English</strong><span>For non-experts</span></div></a>
      <a class="print-toc-card" href="#page-15"><span class="num">16</span><div><strong>Master tables</strong><span>Dollars · FTE · packages · path</span></div></a>
      <a class="print-toc-card" href="#page-16"><span class="num">17</span><div><strong>Sources</strong><span>Market references [1]–[12]</span></div></a>
    </div>
  </section>

  <!-- 02 EXEC -->
  <section class="section flow" id="page-2" data-nav-label="02 · Verdict">
    <div class="section-head"><span class="section-num">02</span><h2>Executive verdict</h2></div>
    <p class="page-lead">This plan asks for a single <strong>seed of $2.5M</strong>. The following round is named <strong>Accelerate</strong> — Series A at <strong>$5–7M</strong>. Accelerate does <strong>not</strong> rewrite CAC, LTV, or payback — it scales denser GTM, sales, and footprint on the same unit economics.</p>

    <div class="cols-2">
      <div class="panel">
        <span class="stat brand">$2.5M</span>
        <span class="stat-label">Seed ask · ~13.7 FTE</span>
        <p>Mkt 850 · Pers 550 · Sales/ft 450 · Tech 400 · Ops 250. People ~$1.27M / non-people ~$1.23M. Q1–Q2 2026. Instrument: convertible note or SAFE.</p>
      </div>
      <div class="panel alt">
        <span class="stat ok">$5–7M</span>
        <span class="stat-label">Accelerate (Series A)</span>
        <p>Sales $2.5M · Marketing $1.5M · Product $1.2M · Runway $0.8M (at $6M mid). Pre-money $20–30M. Q3–Q4 2026. Preferred stock.</p>
      </div>
    </div>

    <div class="chart-block" style="max-width:480px;margin-top:14px"><h4>Raise size — Seed vs Accelerate</h4>{RAISE_COMPARE}</div>

    <h3 class="sub">Capital path (seed → Accelerate → growth → exit)</h3>
    <div class="flow-rail">
      <div class="flow-node"><strong>Seed $2.5M</strong><span>launch · pilots · footprint</span></div>
      <div class="flow-arrow">→</div>
      <div class="flow-node ok"><strong>Accelerate $5–7M</strong><span>Series A · $20–30M pre</span></div>
      <div class="flow-arrow">→</div>
      <div class="flow-node ok"><strong>~$1M → $8M → $26M</strong><span>2027–2029</span></div>
      <div class="flow-arrow">→</div>
      <div class="flow-node ok"><strong>Exit $500M–$1B</strong><span>2029–2031</span></div>
    </div>
    <p class="side-note">Combined base case ~<strong>$8.5M</strong> ($2.5M seed + ~$6M Accelerate). Compare both rounds on the same spend metrics in §03.</p>

    <h3 class="sub">Three motions — unit economics hold across Seed and Accelerate</h3>
    <table class="table-stack">
      <thead><tr><th>Motion</th><th>How sold</th><th>Price band</th><th>Core unit economics</th></tr></thead>
      <tbody>
        <tr><td><strong>B2C Light</strong></td><td>Freemium → self-serve</td><td>$20–$300/mo · events $200–$1,200</td><td>Avg MRR ~$50 · CAC $20–30 · LTV:CAC ~30:1 · payback 1–2 mo</td></tr>
        <tr class="row-accent"><td><strong>B2B Starter / Pro</strong></td><td>Sales-assisted SaaS</td><td>$500–$3,000/mo · ACV ~$12–36K/yr</td><td>Retention 85–90% · CAC payback ~3–4 mo</td></tr>
        <tr><td><strong>Enterprise</strong></td><td>Strategic accounts</td><td>$5,000+/mo · contracts $6K–$150K+/yr</td><td>LTV ~$144K · CAC $3–5K · LTV:CAC ~40:1</td></tr>
      </tbody>
    </table>
  </section>

  <!-- 03 PROCEEDS -->
  <section class="section flow" id="page-3" data-nav-label="03 · Proceeds">
    <div class="section-head"><span class="section-num">03</span><h2>Use of proceeds — Seed vs Accelerate</h2></div>
    <p class="page-lead">Same metric frame for both rounds: marketing / demand, sales / GTM capacity, tech / product, ops / runway, and total raise. <strong>Seed = $2.5M</strong>. <strong>Accelerate = Series A $5–7M</strong> (bars use $6M mid).</p>

    <h3>3.1 Seed — $2.5M</h3>
    <div class="cols-2">
      <div>
        <table>
          <thead><tr><th>Category</th><th>Amount</th><th>Share</th></tr></thead>
          <tbody>
            <tr><td>Marketing</td><td>$850K</td><td>34%</td></tr>
            <tr class="row-accent"><td>Personnel</td><td>$550K</td><td>22%</td></tr>
            <tr><td>Sales / footprint</td><td>$450K</td><td>18%</td></tr>
            <tr class="row-accent"><td>Tech</td><td>$400K</td><td>16%</td></tr>
            <tr><td>Ops / R&amp;D</td><td>$250K</td><td>10%</td></tr>
            <tr class="row-accent"><td><strong>Total</strong></td><td><strong>$2,500K</strong></td><td><strong>100%</strong></td></tr>
          </tbody>
        </table>
        <p class="side-note"><strong>Buys:</strong> denser sales/marketing + multi-site footprint in-seed; London representation (UK / NW Europe; not a second R&amp;D center). <strong>Proof:</strong> 5–10 pilots · $50–100K ARR · 50-lead pipeline · 2–3 partners. <strong>Next:</strong> Accelerate $5–7M.</p>
      </div>
      <div class="chart-block">{SEED_BARS}</div>
    </div>

    <h3 class="sub">3.2 Accelerate (Series A) — $5–7M</h3>
    <div class="cols-2">
      <div>
        <table>
          <thead><tr><th>Category</th><th>Allocation (at $6M mid)</th><th>Share</th></tr></thead>
          <tbody>
            <tr><td>Sales team expansion</td><td>$2.5M</td><td>42%</td></tr>
            <tr class="row-accent"><td>Marketing acceleration</td><td>$1.5M</td><td>25%</td></tr>
            <tr><td>Product scaling</td><td>$1.2M</td><td>20%</td></tr>
            <tr class="row-accent"><td>Runway &amp; contingency</td><td>$800K</td><td>13%</td></tr>
            <tr><td><strong>Total</strong></td><td><strong>$6.0M mid of $5–7M</strong></td><td><strong>100%</strong></td></tr>
          </tbody>
        </table>
        <p class="side-note"><strong>Buys:</strong> enterprise AEs/SDRs, demand gen, engineering + CS tools, working-capital buffer. Pre-money <strong>$20–30M</strong>. Timing Q3–Q4 2026.</p>
      </div>
      <div class="chart-block">{ACCELERATE_BARS}</div>
    </div>

    <h3 class="sub">3.3 Same-metric comparison</h3>
    <p class="page-lead">Mapped to comparable buckets. Seed “Sales / GTM” = Personnel + Sales/footprint ($550K + $450K). Accelerate sales team = $2.5M.</p>
    {ROUND_COMPARE}

    <table class="table-stack">
      <thead><tr><th>Metric</th><th>Seed $2.5M</th><th>Accelerate $5–7M ($6M mid)</th><th>Δ (mid)</th></tr></thead>
      <tbody>
        <tr><td>Marketing / demand</td><td>$850K</td><td>$1.5M</td><td>+$650K</td></tr>
        <tr class="row-accent"><td>Sales / GTM capacity</td><td>$1.0M</td><td>$2.5M</td><td>+$1.5M</td></tr>
        <tr><td>Tech / product</td><td>$400K</td><td>$1.2M</td><td>+$800K</td></tr>
        <tr class="row-accent"><td>Ops / runway</td><td>$250K</td><td>$800K</td><td>+$550K</td></tr>
        <tr><td><strong>Total raise</strong></td><td><strong>$2.5M</strong></td><td><strong>$5–7M</strong></td><td><strong>+$3.5M mid</strong></td></tr>
        <tr class="row-accent"><td>Timing</td><td>Q1–Q2 2026</td><td>Q3–Q4 2026</td><td>—</td></tr>
        <tr><td>Instrument</td><td>SAFE / convertible note</td><td>Series A preferred</td><td>—</td></tr>
        <tr class="row-accent"><td>Valuation frame</td><td>Seed (early)</td><td>$20–30M pre</td><td>—</td></tr>
      </tbody>
    </table>
  </section>

  <!-- 04 SPEED -->
  <section class="section flow" id="page-4" data-nav-label="04 · Speed &amp; footprint">
    <div class="section-head"><span class="section-num">04</span><h2>Speed framework &amp; footprint</h2></div>
    <p class="page-lead"><strong>Seed ($2.5M)</strong> stands up GTM and footprint. <strong>Accelerate ($5–7M)</strong> scales the same motions — never a new CAC/LTV story.</p>

    <div class="cols-3">
      <div class="panel argument-card">
        <span class="stat brand">Seed $2.5M</span>
        <span class="stat-claim">Launch · pilots · footprint</span>
        <p class="stat-method">Personnel, CAC, tech, sales/footprint, and ops — Greek + U.S. units and London representation in-seed.</p>
      </div>
      <div class="panel alt argument-card">
        <span class="stat ok">Accelerate $5–7M</span>
        <span class="stat-claim">Series A scale-up</span>
        <p class="stat-method">Denser sales team, marketing acceleration, product scaling, runway — same unit economics, faster path to ~200 customers.</p>
      </div>
      <div class="panel argument-card">
        <span class="stat cyan">Exit logic</span>
        <span class="stat-claim">Sooner · bigger</span>
        <p class="stat-method">Seed proof then Accelerate compresses the path to growth years and exit.</p>
      </div>
    </div>

    <table class="table-stack">
      <thead><tr><th>Bucket</th><th>What Seed buys</th><th>What Accelerate adds</th></tr></thead>
      <tbody>
        <tr><td><strong>Sales coverage</strong></td><td>AE / SE / partner capacity · Sales/footprint line</td><td>Enterprise AEs, SDRs, solution consultants ($2.5M)</td></tr>
        <tr class="row-accent"><td><strong>Marketing / CAC</strong></td><td>$850K demand + people</td><td>$1.5M demand gen, content, events, SEO/SEM</td></tr>
        <tr><td><strong>Customer success / pilots</strong></td><td>Deploy-to-value on any-camera installs</td><td>CS tools inside product scaling</td></tr>
        <tr class="row-accent"><td><strong>Product finish</strong></td><td>Sentinel + packaging · Tech $400K</td><td>Engineering expansion · Product $1.2M</td></tr>
        <tr><td><strong>Footprint stand-up</strong></td><td>Greek + U.S. + London in seed</td><td>Geographic expansion (e.g. Canada + EU pilots) on Accelerate bar</td></tr>
        <tr class="row-accent"><td><strong>Working capital</strong></td><td>Edge-kit · Ops $250K</td><td>Runway buffer $800K</td></tr>
      </tbody>
    </table>

    <div class="cols-2">
      <div class="panel">
        <h4>What we will not spend on</h4>
        <ul>
          <li>Cloud-VMS rebuild</li>
          <li>Proprietary camera estate</li>
          <li>Second R&amp;D center</li>
          <li>Per-camera license chase</li>
        </ul>
      </div>
      <div class="panel alt">
        <h4>Seed → Accelerate KPIs</h4>
        <ul>
          <li>Seed: 5–10 pilots · $50–100K ARR · 50 leads · 2–3 partners</li>
          <li>Accelerate entry: ~$1M+ ARR · 50–75 B2B · 500–1,000 B2C</li>
          <li>Path toward ~200 customers / ~$8M</li>
          <li>Unit economics unchanged</li>
        </ul>
      </div>
    </div>

    <h3 class="sub">Footprint — Seed vs Accelerate</h3>
    <table>
      <thead><tr><th>Step</th><th>Seed $2.5M</th><th>Accelerate $5–7M</th></tr></thead>
      <tbody>
        <tr><td><strong>1 · Greek unit</strong></td><td>Yes — EU operating base</td><td>Yes — deepen EU presence</td></tr>
        <tr class="row-accent"><td><strong>2 · U.S. business unit</strong></td><td>Yes — denser sales + partners</td><td>Yes — enterprise AE machine</td></tr>
        <tr><td><strong>3 · London / NW Europe</strong></td><td>Yes — representation (not a second R&amp;D center)</td><td>Yes — expand coverage</td></tr>
      </tbody>
    </table>
  </section>

  <!-- 05 FTE -->
  <section class="section flow" id="page-5" data-nav-label="05 · FTE">
    <div class="section-head"><span class="section-num">05</span><h2>FTE granulation — Seed &amp; Accelerate</h2></div>
    <p class="page-lead">Same planning rates for both rounds. <strong>Seed $2.5M → ~13.7 FTE</strong>. <strong>Accelerate (Series A) $5–7M</strong> (roster at <strong>$6M mid</strong>) → <strong>~33 FTE</strong>. Rates are planning assumptions used to map dollars to headcount.</p>

    <h3>5.1 Standard fully-loaded cost per FTE</h3>
    <div class="cols-2">
      <table>
        <thead><tr><th>Role family</th><th>Rate / FTE / yr</th><th>Maps to</th></tr></thead>
        <tbody>
          <tr><td>Sales &amp; BD</td><td><strong>$82K</strong></td><td>AE / SE / SDR / partner; Sales team</td></tr>
          <tr class="row-accent"><td>Marketing (people)</td><td><strong>$76K</strong></td><td>Marketing / demand (people portion)</td></tr>
          <tr><td>Product &amp; Engineering</td><td><strong>$109K</strong></td><td>Product finish / scaling; Tech</td></tr>
          <tr class="row-accent"><td>Customer Success</td><td><strong>$83K</strong></td><td>Customer success / pilots</td></tr>
          <tr><td>Operations &amp; Finance</td><td><strong>$100K</strong></td><td>Ops / R&amp;D; footprint support</td></tr>
        </tbody>
      </table>
      <div class="chart-block"><h4>Planning fully-loaded cost per FTE</h4>{FTE_RATE_BARS}</div>
    </div>

    <h3 class="sub">5.2 People vs non-people split (planning)</h3>
    <table class="table-stack">
      <thead><tr><th>Spend bucket</th><th>People share</th><th>Non-people share</th><th>Non-people examples</th></tr></thead>
      <tbody>
        <tr><td>Seed · Personnel</td><td><strong>100%</strong></td><td>0%</td><td>—</td></tr>
        <tr class="row-accent"><td>Seed · Marketing</td><td><strong>~18%</strong></td><td>Remainder</td><td>CAC / demand programs</td></tr>
        <tr><td>Seed · Tech / Sales/ft / Ops</td><td><strong>~55–60% / ~50%</strong></td><td>Remainder</td><td>Footprint, infra, legal, tools</td></tr>
        <tr class="row-accent"><td>Accelerate · Sales team ($2.5M)</td><td><strong>~70%</strong></td><td>~30%</td><td>Salesforce, tools, travel, enablement</td></tr>
        <tr><td>Accelerate · Marketing ($1.5M)</td><td><strong>~20%</strong></td><td>~80%</td><td>Demand gen, content, events, SEO/SEM</td></tr>
        <tr class="row-accent"><td>Accelerate · Product ($1.2M)</td><td><strong>~70%</strong></td><td>~30%</td><td>Tooling, mobile infra, CS systems</td></tr>
        <tr><td>Accelerate · Runway ($0.8M)</td><td><strong>0%</strong></td><td>100%</td><td>Working capital buffer</td></tr>
      </tbody>
    </table>

    <h3 class="sub">5.3 Seed — $2.5M → ~13.7 FTE</h3>
    <table class="table-stack">
      <thead><tr><th>Role</th><th>FTE</th><th>Rate</th><th>Cost</th><th>Spend bucket</th></tr></thead>
      <tbody>
        <tr><td>Product &amp; Engineering</td><td>2.5</td><td>$109K</td><td>$273K</td><td>Personnel</td></tr>
        <tr class="row-accent"><td>Sales &amp; BD</td><td>1.5</td><td>$82K</td><td>$123K</td><td>Personnel</td></tr>
        <tr><td>Customer Success</td><td>1.0</td><td>$83K</td><td>$83K</td><td>Personnel</td></tr>
        <tr class="row-accent"><td>Operations &amp; Finance</td><td>0.7</td><td>$100K</td><td>$70K</td><td>Personnel</td></tr>
        <tr><td><em>Personnel subtotal</em></td><td><em>5.7</em></td><td></td><td><em>$549K</em></td><td><em>+$1K plug → $550K</em></td></tr>
        <tr class="row-accent"><td>Marketing (people)</td><td>2.0</td><td>$76K</td><td>$152K</td><td>Marketing</td></tr>
        <tr><td>Sales &amp; BD (AE / SE / partner)</td><td>3.0</td><td>$82K</td><td>$246K</td><td>Sales / footprint</td></tr>
        <tr class="row-accent"><td>Product &amp; Engineering</td><td>2.0</td><td>$109K</td><td>$218K</td><td>Tech</td></tr>
        <tr><td>Operations &amp; Finance</td><td>1.0</td><td>$100K</td><td>$100K</td><td>Ops / R&amp;D</td></tr>
        <tr class="row-accent"><td><strong>People subtotal</strong></td><td><strong>13.7</strong></td><td></td><td><strong>$1,265K</strong></td><td></td></tr>
        <tr><td>Marketing / CAC programs</td><td>—</td><td>—</td><td>$698K</td><td>Marketing ($850−$152)</td></tr>
        <tr class="row-accent"><td>Footprint stand-up (GR / US / London)</td><td>—</td><td>—</td><td>$204K</td><td>Sales/ft ($450−$246)</td></tr>
        <tr><td>Tech infra / contractors</td><td>—</td><td>—</td><td>$182K</td><td>Tech ($400−$218)</td></tr>
        <tr class="row-accent"><td>Ops / legal / entity / R&amp;D</td><td>—</td><td>—</td><td>$150K</td><td>Ops ($250−$100)</td></tr>
        <tr><td>Personnel rounding plug</td><td>—</td><td>—</td><td>$1K</td><td>Aligns Personnel to $550K</td></tr>
        <tr class="row-accent"><td><strong>Non-people + plug</strong></td><td></td><td></td><td><strong>$1,235K</strong></td><td></td></tr>
        <tr><td><strong>Seed total</strong></td><td></td><td></td><td><strong>$2,500K</strong></td><td></td></tr>
      </tbody>
    </table>
    <div class="cols-2">
      <div class="chart-block">{PEOPLE_SEED}</div>
      <div class="chart-block"><h4>Seed FTE by role</h4>{FTE_SEED}</div>
    </div>
    <table class="table-stack">
      <thead><tr><th>Role family</th><th>Seed FTE</th><th>Rate</th></tr></thead>
      <tbody>
        <tr><td>Product &amp; Engineering</td><td>4.5</td><td>$109K</td></tr>
        <tr class="row-accent"><td>Sales &amp; BD</td><td>4.5</td><td>$82K</td></tr>
        <tr><td>Marketing (people)</td><td>2.0</td><td>$76K</td></tr>
        <tr class="row-accent"><td>Customer Success</td><td>1.0</td><td>$83K</td></tr>
        <tr><td>Operations &amp; Finance</td><td>1.7</td><td>$100K</td></tr>
        <tr class="row-accent"><td><strong>Total FTE</strong></td><td><strong>13.7</strong></td><td></td></tr>
      </tbody>
    </table>

    <h3 class="sub">5.4 Accelerate (Series A) — $5–7M → ~33 FTE at $6M mid</h3>
    <p class="page-lead">Same rates as Seed. Roster sized on the <strong>$6M</strong> midpoint of the $5–7M ask. At the $5M low end, scale people ~proportionally (~27.5 FTE); at $7M high end (~38.5 FTE).</p>
    <table class="table-stack">
      <thead><tr><th>Role</th><th>FTE</th><th>Rate</th><th>Cost</th><th>Spend bucket</th></tr></thead>
      <tbody>
        <tr><td>Sales &amp; BD (AE / SE / SDR / consultants)</td><td>21.0</td><td>$82K</td><td>$1,722K</td><td>Sales team ($2.5M)</td></tr>
        <tr class="row-accent"><td>Salesforce / tools / travel / enablement</td><td>—</td><td>—</td><td>$778K</td><td>Sales residual ($2.5M − $1,722K)</td></tr>
        <tr><td>Marketing (people)</td><td>4.0</td><td>$76K</td><td>$304K</td><td>Marketing ($1.5M)</td></tr>
        <tr class="row-accent"><td>Demand gen / content / events / SEO/SEM</td><td>—</td><td>—</td><td>$1,196K</td><td>Marketing residual</td></tr>
        <tr><td>Product &amp; Engineering</td><td>7.0</td><td>$109K</td><td>$763K</td><td>Product ($1.2M)</td></tr>
        <tr class="row-accent"><td>Customer Success</td><td>1.0</td><td>$83K</td><td>$83K</td><td>Product ($1.2M)</td></tr>
        <tr><td>Product tooling / mobile infra / CS systems</td><td>—</td><td>—</td><td>$354K</td><td>Product residual</td></tr>
        <tr class="row-accent"><td>Working capital buffer</td><td>—</td><td>—</td><td>$800K</td><td>Runway ($0.8M)</td></tr>
        <tr><td><strong>People subtotal</strong></td><td><strong>33.0</strong></td><td></td><td><strong>$2,872K</strong></td><td></td></tr>
        <tr class="row-accent"><td><strong>Non-people subtotal</strong></td><td></td><td></td><td><strong>$3,128K</strong></td><td></td></tr>
        <tr><td><strong>Accelerate total (mid)</strong></td><td></td><td></td><td><strong>$6,000K</strong></td><td>of $5–7M ask</td></tr>
      </tbody>
    </table>
    <div class="cols-2">
      <div class="chart-block">{PEOPLE_ACCEL}</div>
      <div class="chart-block"><h4>Accelerate FTE by role ($6M mid)</h4>{FTE_ACCEL}</div>
    </div>
    <p class="side-note">BP language names “4 enterprise AEs, 2 SDRs, solution consultants” as the core sales shape; the <strong>~21 Sales FTE</strong> planning view is the full-year capacity funded by the $2.5M sales line (AEs/SDRs/SEs/partners + ramped coverage), not a headcount ceiling printed as six named seats only.</p>

    <h3 class="sub">5.5 Seed vs Accelerate FTE rollup</h3>
    {FTE_COMPARE}
    <table class="table-stack">
      <thead><tr><th>Role family</th><th>Seed FTE</th><th>Accelerate FTE ($6M mid)</th><th>Δ</th><th>Rate</th></tr></thead>
      <tbody>
        <tr><td>Product &amp; Engineering</td><td>4.5</td><td>7.0</td><td>+2.5</td><td>$109K</td></tr>
        <tr class="row-accent"><td>Sales &amp; BD</td><td>4.5</td><td>21.0</td><td>+16.5</td><td>$82K</td></tr>
        <tr><td>Marketing (people)</td><td>2.0</td><td>4.0</td><td>+2.0</td><td>$76K</td></tr>
        <tr class="row-accent"><td>Customer Success</td><td>1.0</td><td>1.0</td><td>—</td><td>$83K</td></tr>
        <tr><td>Operations &amp; Finance</td><td>1.7</td><td>—</td><td>(seed OpEx; Accelerate runway is non-people)</td><td>$100K</td></tr>
        <tr class="row-accent"><td><strong>Total FTE (per round)</strong></td><td><strong>13.7</strong></td><td><strong>33.0</strong></td><td><strong>+19.3</strong></td><td>Accelerate is incremental — does not include Seed</td></tr>
        <tr><td><strong>Combined FTE (Seed + Accelerate)</strong></td><td><strong>13.7</strong></td><td><strong>33.0</strong></td><td><strong>46.7</strong></td><td>Both rounds live · 13.7 + 33.0</td></tr>
        <tr class="row-accent"><td>People $</td><td>$1,265K</td><td>$2,872K</td><td>+$1,607K</td><td></td></tr>
        <tr><td>Non-people $</td><td>$1,235K</td><td>$3,128K</td><td>+$1,893K</td><td></td></tr>
        <tr class="row-accent"><td><strong>Round total $</strong></td><td><strong>$2,500K</strong></td><td><strong>$6,000K mid</strong></td><td><strong>$8,500K</strong></td><td>Seed + Accelerate mid</td></tr>
      </tbody>
    </table>
    <div class="kicker">Per-round totals are separate raises. Combined FTE = Seed standing (~13.7) + Accelerate new capacity (~33) → <strong>~46.7 FTE</strong> when both are live. Sales is the main step-up (+16.5 FTE on the Accelerate line alone).</div>
  </section>

  <!-- 06 ACCELERATE -->
  <section class="section flow" id="page-6" data-nav-label="06 · Accelerate">
    <div class="section-head"><span class="section-num">06</span><h2>Accelerate (Series A) &amp; capital path</h2></div>
    <p class="page-lead"><strong>Accelerate</strong> is the name for Series A in this plan: <strong>$5–7M</strong> after the <strong>$2.5M seed</strong>. Same motions, larger GTM — dollars in §03, headcount in §05 (~33 FTE at $6M mid).</p>

    <div class="cols-3">
      <div class="panel">
        <span class="stat brand">$2.5M</span>
        <span class="stat-label">Seed ask</span>
        <p>Timing: Q1–Q2 2026. SAFE / note. Proof: 5–10 pilots · $50–100K ARR · 50 leads · 2–3 partners.</p>
      </div>
      <div class="panel alt">
        <span class="stat ok">$5–7M</span>
        <span class="stat-label">Accelerate (Series A)</span>
        <p>Pre-money <strong>$20–30M</strong>. Mid often <strong>$6M</strong>. Timing: Q3–Q4 2026. Preferred stock.</p>
      </div>
      <div class="panel">
        <span class="stat">$500M–$1B</span>
        <span class="stat-label">Target exit</span>
        <p>IPO or strategic acquisition (2029–2031). Accelerate modeled ~13x / ~65% IRR at a $750M exit case.</p>
      </div>
    </div>

    <div class="chart-block" style="max-width:480px"><h4>Raise — Seed vs Accelerate</h4>{RAISE_COMPARE}</div>

    <h3 class="sub">Accelerate terms</h3>
    <table class="table-stack">
      <thead><tr><th>Element</th><th>Plan figure</th></tr></thead>
      <tbody>
        <tr><td>Target raise</td><td><strong>$5–7M</strong> (mid often <strong>$6M</strong>)</td></tr>
        <tr class="row-accent"><td>Pre-money valuation</td><td><strong>$20–30M</strong></td></tr>
        <tr><td>Dilution (illustrative)</td><td>~20–25% at Accelerate</td></tr>
        <tr class="row-accent"><td>Security</td><td>Series A preferred stock</td></tr>
        <tr><td>Timing</td><td>Q3–Q4 2026 (after seed Q1–Q2 2026)</td></tr>
        <tr class="row-accent"><td>Combined seed + Accelerate</td><td>~$8.5M ($2.5M + ~$6M)</td></tr>
        <tr><td>Entry bar</td><td>~$1M+ ARR · 50–75 B2B · 500–1,000 B2C</td></tr>
      </tbody>
    </table>

    <h3 class="sub">Accelerate use of funds (same metric frame as Seed)</h3>
    <div class="cols-2">
      <table>
        <thead><tr><th>Category</th><th>Allocation</th><th>Purpose</th></tr></thead>
        <tbody>
          <tr><td>Sales / GTM</td><td><strong>$2.5M (42%)</strong></td><td>Enterprise AEs, SDRs, consultants, Salesforce</td></tr>
          <tr class="row-accent"><td>Marketing / demand</td><td><strong>$1.5M (25%)</strong></td><td>Demand gen, content, events, SEO/SEM</td></tr>
          <tr><td>Tech / product</td><td><strong>$1.2M (20%)</strong></td><td>Engineering, mobile, CS tools</td></tr>
          <tr class="row-accent"><td>Ops / runway</td><td><strong>$800K (13%)</strong></td><td>Working capital buffer</td></tr>
        </tbody>
      </table>
      <div class="chart-block"><h4>Accelerate mix ($6M mid)</h4>{ACCELERATE_BARS}</div>
    </div>

    <h3 class="sub">Growth path &amp; why underwritable</h3>
    <table class="table-stack">
      <thead><tr><th>Horizon</th><th>Plan outcome</th></tr></thead>
      <tbody>
        <tr><td><strong>Seed · $2.5M</strong></td><td>Denser sales + multi-site footprint; London rep; 5–10 pilots · $50–100K ARR · 50 leads · 2–3 partners.</td></tr>
        <tr class="row-accent"><td><strong>Accelerate · $5–7M</strong></td><td>Sales, marketing, product, runway — path toward ~200 customers / ~$8M.</td></tr>
        <tr><td><strong>2027</strong></td><td>~$1M · 50 B2B · ~600 consumers</td></tr>
        <tr class="row-accent"><td><strong>2028</strong></td><td>~$8M · 200 B2B · 6,000+ consumers — breakeven</td></tr>
        <tr><td><strong>2029</strong></td><td>~$26M · 500 B2B · 20,000+ consumers</td></tr>
        <tr class="row-accent"><td><strong>2029–2031</strong></td><td>Exit $500M–$1B</td></tr>
      </tbody>
    </table>
    <ul>
      <li><strong>Products are built, not imagined:</strong> Five of six apps exist as working beta (Sentinel still in active build).</li>
      <li><strong>Distribution is already on board:</strong> TMA / Talos (TMAIX) and NewGen are signed partners pursuing leads.</li>
      <li><strong>Deloitte is a force multiplier in waiting:</strong> Groundwork for Deloitte Greece / EMEA Cyber Security Committee is in place.</li>
      <li><strong>LG International is a global-scale multiplier:</strong> Early-stage hot lead — manufacturing, logistics, retail, government supply-chain doors.</li>
      <li><strong>Seed then Accelerate:</strong> CAC, LTV, and payback hold; Accelerate scales the same motions.</li>
    </ul>
  </section>

  <!-- 07 CASH & RUNWAY -->
  <section class="section flow" id="page-cash" data-nav-label="07 · Cash &amp; runway">
    <div class="section-head"><span class="section-num">07</span><h2>Cash &amp; runway</h2></div>
    <p class="page-lead">Plan cash model: <strong>Seed $2.5M</strong> funds operations until <strong>Accelerate ($5–7M, mid $6M)</strong> closes; combined ~<strong>$8.5M</strong> covers the investment phase through profitability. Unit economics stay the same.</p>

    <div class="notify">
      <h5>Verdict</h5>
      <p>Under the baseline plan the company does <strong>not</strong> operate into a zero-cash gap: Seed bridge (~6–12 months) is sized to reach Accelerate, and Accelerate replenishes cash with an ~<strong>18-month working-capital runway</strong> toward profitability. Missing Accelerate on time is the main cash-risk failure mode.</p>
    </div>

    <h3 class="sub">7.1 Funding calendar (cash in)</h3>
    <table class="table-stack">
      <thead><tr><th>When</th><th>Round</th><th>Cash in</th><th>Job for cash</th></tr></thead>
      <tbody>
        <tr><td>Q1–Q2 2026</td><td><strong>Seed</strong></td><td><strong>$2.5M</strong></td><td>Stand up ~13.7 FTE GTM + programs; hit seed proof; keep cash until Accelerate</td></tr>
        <tr class="row-accent"><td>Q3–Q4 2026</td><td><strong>Accelerate</strong> (Series A)</td><td><strong>$5–7M</strong> (mid <strong>$6M</strong>)</td><td>Scale sales/marketing/product; refill runway buffer</td></tr>
        <tr><td>Combined</td><td>Seed + Accelerate</td><td><strong>~$8.5M</strong> base case</td><td>Fund growth through plan profitability</td></tr>
      </tbody>
    </table>
    <div class="chart-block" style="max-width:520px"><h4>Capital in — Seed · Accelerate · combined</h4>{CASH_BRIDGE}</div>

    <h3 class="sub">7.2 Seed-period burn (derived from this pack’s FTE)</h3>
    <p class="side-note">People cost on the seed roster is ~$1.265M/yr ≈ <strong>~$105K/month</strong>. With marketing/tech/ops non-people programs, an all-in seed burn on the order of <strong>~$150–250K/month</strong> (mid ~$200K) is the planning band. At ~$200K/mo, <strong>$2.5M alone ≈ ~12 months</strong> of runway — enough to cover Q1–Q2 2026 seed spend and still leave months of cushion into the Accelerate window (Q3–Q4 2026).</p>
    <div class="cols-2">
      <div class="chart-block"><h4>Illustrative monthly burn (seed)</h4>{MONTHLY_BURN}</div>
      <table>
        <thead><tr><th>Check</th><th>Figure</th></tr></thead>
        <tbody>
          <tr><td>Seed cash in</td><td><strong>$2.5M</strong></td></tr>
          <tr class="row-accent"><td>People burn (planning)</td><td>~$105K/mo</td></tr>
          <tr><td>All-in burn band</td><td>~$150–250K/mo</td></tr>
          <tr class="row-accent"><td>Seed-alone runway @ ~$200K/mo</td><td><strong>~12 months</strong></td></tr>
          <tr><td>Months to Accelerate close (plan)</td><td>~6–9 months after seed</td></tr>
          <tr class="row-accent"><td>Cash left at Accelerate if burn ~$200K × 7 mo</td><td>~$1.1M still on hand + new $5–7M</td></tr>
        </tbody>
      </table>
    </div>
    <p class="side-note"><strong>Rule:</strong> Accelerate must close while seed cash remaining + committed inflows still cover &gt;3 months of burn. Do not schedule Accelerate after seed cash is exhausted.</p>

    <h3 class="sub">7.3 Operating P&amp;L cash need (baseline plan model)</h3>
    <p class="page-lead">Investment Opportunity baseline cash requirements (plan model). Years here are the cash model’s calendar; commercial logo path in this pack still uses 2027–2029 proof years — both share the same raise: Seed then Accelerate.</p>
    <table class="table-stack">
      <thead><tr><th>Year</th><th>Revenue</th><th>Total cost (COGS + OpEx)</th><th>EBITDA</th><th>Cash implication</th></tr></thead>
      <tbody>
        <tr><td><strong>2026</strong></td><td>$1.04M</td><td>$2.54M</td><td><strong>−$1.5M</strong></td><td>Investment year — funded by Seed + early Accelerate</td></tr>
        <tr class="row-accent"><td><strong>2027</strong></td><td>$8.09M</td><td>$7.59M</td><td><strong>+$0.5M</strong></td><td>Breakeven ~Q2 2027 on this model — cash turns</td></tr>
        <tr><td><strong>2028</strong></td><td>$26.15M</td><td>$18.55M</td><td><strong>+$7.6M</strong></td><td>Self-funding ops; positive free-cash trajectory</td></tr>
      </tbody>
    </table>
    <div class="chart-block" style="max-width:480px"><h4>Baseline EBITDA path (plan cash model)</h4>{EBITDA_BARS}</div>

    <h3 class="sub">7.4 Why ~$8.5M keeps the lights on</h3>
    <table class="table-stack">
      <thead><tr><th>Pool</th><th>Amount</th><th>Role</th></tr></thead>
      <tbody>
        <tr><td>Seed</td><td>$2.5M</td><td>Bridge to Accelerate; first pilots and footprint without a cash gap</td></tr>
        <tr class="row-accent"><td>Accelerate (mid)</td><td>$6.0M of $5–7M</td><td>Scale GTM; refill runway after seed spend</td></tr>
        <tr><td>Of which working-capital framing</td><td>~$5.6M of the combined plan</td><td>Stated as <strong>~18-month runway to profitability</strong> in the Investment Opportunity cash model</td></tr>
        <tr class="row-accent"><td><strong>Total planned raise</strong></td><td><strong>~$8.5M</strong></td><td>Covers 2026 −$1.5M EBITDA year + scale-up into 2027 breakeven</td></tr>
      </tbody>
    </table>

    <h3 class="sub">7.5 Scenario stress (cash)</h3>
    <table class="table-stack">
      <thead><tr><th>Scenario</th><th>What changes</th><th>Cash outcome</th></tr></thead>
      <tbody>
        <tr><td><strong>Pessimistic</strong></td><td>Slower penetration; lower headcount; longer to profit</td><td>Plan still treats <strong>Seed $2.5M</strong> as able to reach profitability in the stress case — Accelerate optional for speed, not survival</td></tr>
        <tr class="row-accent"><td><strong>Baseline (this plan)</strong></td><td>Seed + Accelerate ~$8.5M</td><td>Funds trajectory through ~Q2 2027 EBITDA breakeven; no planned cash cliff</td></tr>
        <tr><td><strong>Optimistic</strong></td><td>Faster revenue; earlier cash turn</td><td>Accelerate still used for share capture; cash risk falls further</td></tr>
        <tr class="row-accent"><td><strong>Failure mode</strong></td><td>Accelerate delayed past seed runway</td><td>Must cut burn or bridge — this is the cash-break case to underwrite against</td></tr>
      </tbody>
    </table>

    <div class="kicker">Cash discipline: close Seed → spend inside the ~$150–250K/mo band → close Accelerate while &gt;3 months of burn remain → use Accelerate runway (~18 months framing) through plan profitability. The company is not designed to operate into empty cash between rounds.</div>
  </section>

  <!-- 08 PRICING -->
  <section class="section flow" id="page-7" data-nav-label="08 · Pricing">
    <div class="section-head"><span class="section-num">08</span><h2>Commercial package pricing</h2></div>
    <p class="page-lead">Three motions on one platform — no per-camera ceiling.</p>

    <div class="flow-rail">
      <div class="flow-node"><strong>B2C Light</strong><span>volume · self-serve</span></div>
      <div class="flow-node alt"><strong>B2B Starter / Pro</strong><span>land &amp; expand</span></div>
      <div class="flow-node"><strong>Enterprise</strong><span>strategic ACV</span></div>
      <div class="flow-arrow">→</div>
      <div class="flow-node ok"><strong>Same platform</strong><span>~$1M → $8M → $26M</span></div>
    </div>

    <h3>7.1 B2C Light</h3>
    <table>
      <thead><tr><th>SKU</th><th>Price</th><th>Buyer</th></tr></thead>
      <tbody>
        <tr><td>Signage Lite</td><td>$30–$100/mo</td><td>Marketing consultants, small agencies</td></tr>
        <tr class="row-accent"><td>Home Security Lite</td><td>$20–$50/mo</td><td>Homeowners, small property managers</td></tr>
        <tr><td>Retail Compliance Lite</td><td>$50–$100/mo</td><td>Small retail, bars, restaurants</td></tr>
        <tr class="row-accent"><td>Event Security Lite</td><td>$200–$1,200/event</td><td>Contractors, venue managers</td></tr>
        <tr><td>Band (overall)</td><td>$20–$300/mo</td><td>Freemium + self-serve</td></tr>
        <tr class="row-accent"><td>Funnel</td><td>Free 60–90 days → Lite / Pro</td><td>Web signup, app-first</td></tr>
      </tbody>
    </table>
    <p class="side-note"><strong>Modeled blend:</strong> avg MRR ~$50.</p>
    <div class="chart-block"><h4>B2C Lite monthly price bands (low–high; events = per event)</h4>{B2C_PRICE}</div>

    <h3 class="sub">7.2 B2B — Starter &amp; Professional</h3>
    <table>
      <thead><tr><th>Tier</th><th>Monthly</th><th>Scope</th></tr></thead>
      <tbody>
        <tr><td><strong>Starter</strong></td><td>$500–$1,000</td><td>1–5 locations · 5 cameras · single app · basic support</td></tr>
        <tr class="row-accent"><td><strong>Professional</strong></td><td>$1,500–$3,000</td><td>5–20 locations · 25 cameras · multi-app · priority support</td></tr>
        <tr><td><strong>Typical ACV path</strong></td><td>~$12K–$36K/year</td><td>Per account</td></tr>
        <tr class="row-accent"><td><strong>Mobile / wearable</strong></td><td>+40–60% premium</td><td>Where needed</td></tr>
      </tbody>
    </table>
    <div class="chart-block" style="max-width:520px"><h4>B2B monthly price bands</h4>{B2B_PRICE}</div>

    <h3 class="sub">7.3 Enterprise</h3>
    <table>
      <thead><tr><th>Element</th><th>Plan figure</th></tr></thead>
      <tbody>
        <tr><td>Monthly floor</td><td>$5,000+/mo</td></tr>
        <tr class="row-accent"><td>Contract band</td><td>$6K–$150K+/year</td></tr>
        <tr><td>Planned avg ACV</td><td>Often $12K–$20K+</td></tr>
        <tr class="row-accent"><td>Scope</td><td>Unlimited sites / cameras · Matrix · VPN fleets · custom ERP / CRM / eHealth / SIEM</td></tr>
        <tr><td>Verticals named</td><td>Home care / Virtual Ward, maritime, municipal, multi-brand retail</td></tr>
      </tbody>
    </table>
  </section>

  <!-- 08 UNIT ECON -->
  <section class="section flow" id="page-8" data-nav-label="09 · Unit economics">
    <div class="section-head"><span class="section-num">09</span><h2>Unit economics by motion</h2></div>
    <p class="page-lead">CAC, LTV, and payback are plan models (not yet cohort-backed). Moving from Seed $2.5M to Accelerate $5–7M does <strong>not</strong> rewrite these metrics — Accelerate only buys scale.</p>

    <table class="table-stack">
      <thead><tr><th>Metric</th><th>B2C Light</th><th>B2B Starter / Pro</th><th>Enterprise</th></tr></thead>
      <tbody>
        <tr><td>Revenue unit</td><td>Avg MRR ~$50</td><td>ACV ~$12–36K/yr</td><td>Avg ACV often $12–20K+ (band to $150K+)</td></tr>
        <tr class="row-accent"><td>CAC</td><td>$20–30</td><td>(payback stated; CAC $ not separately tagged)</td><td>$3K–5K</td></tr>
        <tr><td>LTV / ratio</td><td>LTV:CAC ~30:1</td><td>Retention 85–90%</td><td>LTV ~$144K · LTV:CAC ~40:1</td></tr>
        <tr class="row-accent"><td>Payback</td><td>1–2 months</td><td>~3–4 months</td><td>(implied by high LTV:CAC)</td></tr>
        <tr><td>Motion</td><td>High volume, shorter LTV</td><td>Land-and-expand</td><td>Strategic / multi-vertical</td></tr>
      </tbody>
    </table>

    <div class="chart-block" style="max-width:480px"><h4>Illustrative CAC — B2C vs Enterprise</h4>{CAC_BARS}</div>

    <h3 class="sub">Derived B2C LTV sketch</h3>
    <p class="side-note">From avg MRR ~$50 and LTV:CAC ~30:1 with CAC $20–30. Implied tenure is arithmetic for diligence — B2C tenure is not stated as a separate figure.</p>
    <table>
      <thead><tr><th>Assumption</th><th>Low CAC</th><th>High CAC</th></tr></thead>
      <tbody>
        <tr><td>CAC</td><td>$20</td><td>$30</td></tr>
        <tr class="row-accent"><td>Implied LTV @ 30:1</td><td>$600</td><td>$900</td></tr>
        <tr><td>Months of ~$50 MRR (no discount)</td><td>12 mo</td><td>18 mo</td></tr>
      </tbody>
    </table>

    <h3 class="sub">Derived Enterprise tenure sketch</h3>
    <p class="side-note">LTV ~$144K with planned avg ACV often $12–20K+ → implied tenure ≈ $144K ÷ ACV (LTV as ACV × modeled tenure).</p>
    <table>
      <thead><tr><th>Assumed ACV</th><th>Implied tenure</th></tr></thead>
      <tbody>
        <tr><td>$12K</td><td>~12 years</td></tr>
        <tr class="row-accent"><td>$16K</td><td>~9 years</td></tr>
        <tr><td>$20K</td><td>~7.2 years</td></tr>
      </tbody>
    </table>

    <div class="notify">
      <h5>How we model unit economics</h5>
      <p>B2C assumes ~$50 blended MRR, low digital CAC via freemium, and multi-year retention; Enterprise LTV ~$144K is ACV × modeled tenure. Treat LTV:CAC as directional underwriting inputs — diligence should pressure-test CAC channels and churn.</p>
    </div>
  </section>

  <!-- 09 MARKET -->
  <section class="section flow" id="page-9" data-nav-label="10 · Market &amp; reach">
    <div class="section-head"><span class="section-num">10</span><h2>Market size &amp; reach</h2></div>
    <p class="page-lead">Dollar TAM bands are conservative U.S. addressable ranges grounded in third-party category reports ([9]–[12]). Share → revenue is plan arithmetic. Pocket counts cite [1]–[8].</p>

    <div class="cols-2">
      <div class="panel">
        <span class="stat cyan">$0.5–1.5B</span>
        <span class="stat-label">B2C TAM, U.S.</span>
        <p>Target 1–3% share → ~$5–45M revenue opportunity. Grounded in <a class="ref" href="#ref-11">[11]</a>–<a class="ref" href="#ref-12">[12]</a>.</p>
      </div>
      <div class="panel alt">
        <span class="stat brand">$2–4B</span>
        <span class="stat-label">B2B / Enterprise TAM, U.S.</span>
        <p>Target 1–2% share → ~$20–80M. Inside U.S. video analytics <a class="ref" href="#ref-9">[9]</a>–<a class="ref" href="#ref-10">[10]</a>.</p>
      </div>
    </div>

    <table>
      <thead><tr><th>Segment</th><th>U.S. TAM (plan)</th><th>Target share</th><th>→ Revenue opportunity</th></tr></thead>
      <tbody>
        <tr><td>B2C</td><td>$0.5–1.5B</td><td>1–3%</td><td>~$5–45M</td></tr>
        <tr class="row-accent"><td>B2B / Enterprise</td><td>$2–4B</td><td>1–2%</td><td>~$20–80M</td></tr>
      </tbody>
    </table>
    <div class="chart-block"><h4>Plan revenue opportunity from TAM × share</h4>{TAM_OPP}</div>

    <h3 class="sub">Enterprise segment map (U.S. targets — plan ranges)</h3>
    <div class="panel summary-panel">
      <div class="tags">
        <span class="tag">Large retail $12–24M</span>
        <span class="tag mode">Security agencies $6–12M</span>
        <span class="tag user">Education $6–12M</span>
        <span class="tag ok">CRE $12–24M</span>
        <span class="tag safety">Gov / LE</span>
      </div>
    </div>
    <div class="chart-block"><h4>Segment map — midpoint of plan bands</h4>{SEG_MAP}</div>

    <h3 class="sub">Buyer pockets (demand context)</h3>
    <table class="table-stack">
      <thead><tr><th>Motion</th><th>Price</th><th>Economics</th><th>Buyer / pockets</th></tr></thead>
      <tbody>
        <tr>
          <td><strong>B2C Light</strong></td>
          <td>$20–$300/mo · events $200–$1,200. Shelf: Signage Lite $30–100, Home Security Lite $20–50, Retail Compliance Lite $50–100, Event Security Lite $200–1,200/event. Free funnel 60–90 days.</td>
          <td>Avg MRR ~$50 · CAC $20–30 · LTV:CAC ~30:1 · payback 1–2 mo</td>
          <td>Homeowners, micro-SMEs, consultants, small retail. Pockets: ~52K marketing consulting<a class="ref" href="#ref-1">[1]</a>; ~87M owner-occupied homes<a class="ref" href="#ref-2">[2]</a>; ~0.8M Airbnb hosts<a class="ref" href="#ref-3">[3]</a>; ~8K contract security<a class="ref" href="#ref-4">[4]</a>; ~1.0M+ retail + ~0.6M restaurants<a class="ref" href="#ref-5">[5]</a><a class="ref" href="#ref-6">[6]</a>.</td>
        </tr>
        <tr class="row-accent">
          <td><strong>B2B Starter / Pro</strong></td>
          <td>$500–$3,000/mo · ACV ~$12–36K. Starter $500–1,000 (1–5 sites, 5 cams). Pro $1,500–3,000 (5–20 sites, 25 cams). Mobile/wearable +40–60%.</td>
          <td>Retention 85–90% · CAC payback ~3–4 mo</td>
          <td>Multi-site retail, offices, regional security, campuses, warehouses. Pockets: ~8K contract security<a class="ref" href="#ref-4">[4]</a>; ~99K public K–12<a class="ref" href="#ref-7">[7]</a>; ~38K warehousing<a class="ref" href="#ref-8">[8]</a>.</td>
        </tr>
        <tr>
          <td><strong>Enterprise</strong></td>
          <td>$5,000+/mo · contracts $6K–$150K+/yr. Unlimited sites/cameras, Matrix, VPN fleets, custom ERP/CRM/eHealth/SIEM.</td>
          <td>LTV ~$144K · CAC $3–5K · LTV:CAC ~40:1</td>
          <td>Home care, maritime, industrial, municipal, multi-brand retail. Segment $ targets above; market-size URLs in Sources.</td>
        </tr>
      </tbody>
    </table>
  </section>

  <!-- 10 REVENUE -->
  <section class="section flow" id="page-10" data-nav-label="11 · Revenue path">
    <div class="section-head"><span class="section-num">11</span><h2>Revenue path &amp; derived mix</h2></div>
    <p class="page-lead">Seed milestones and growth years on the plan path. Derived mix peels B2C at ~$50 MRR first; residual → B2B/Enterprise blended ACV.</p>

    <h3>10.1 Seed milestones (before scale years)</h3>
    <table>
      <thead><tr><th>Horizon</th><th>Commercial proof</th></tr></thead>
      <tbody>
        <tr><td>Seed ($2.5M) in-seed</td><td>5–10 pilots · <strong>$50–100K ARR</strong> · 50-lead pipeline · 2–3 partners</td></tr>
        <tr class="row-accent"><td>Series A language</td><td>Path toward ~200 customers (sales + marketing ramp)</td></tr>
      </tbody>
    </table>

    <h3 class="sub">10.2 Growth years</h3>
    <table>
      <thead><tr><th>Year</th><th>Revenue</th><th>B2B customers</th><th>Consumer users</th><th>Note</th></tr></thead>
      <tbody>
        <tr><td><strong>2027</strong></td><td>~$1M</td><td>50</td><td>~600</td><td>First commercial proof after seed launch of five beta-ready products</td></tr>
        <tr class="row-accent"><td><strong>2028</strong></td><td>~$8M</td><td>200</td><td>6,000+</td><td>Breakeven; capital above burn accelerates arrival</td></tr>
        <tr><td><strong>2029</strong></td><td>~$26M</td><td>500</td><td>20,000+</td><td>Solidly profitable on the three motions</td></tr>
        <tr class="row-accent"><td><strong>2030–2031</strong></td><td>—</td><td>—</td><td>—</td><td>Exit $500M–$1B (plan target)</td></tr>
      </tbody>
    </table>

    <div class="ffc-charts">
      <div class="chart-block"><h4>Plan revenue path (USD millions)</h4>{REV_PATH}</div>
      <div class="chart-block"><h4>Plan customer counts (B2B · consumers)</h4>{CUST_PATH}</div>
    </div>

    <h3 class="sub">10.3 Derived mix check</h3>
    <p class="side-note">Using ~$50 blended B2C MRR → $600/yr. Consistency check on the revenue path. Implied B2B ACVs sit inside Starter/Pro ~$12–36K and Enterprise “often $12–20K+,” with 2029 implying a richer mix.</p>
    <table class="table-stack">
      <thead><tr><th>Year</th><th>Plan revenue</th><th>B2C rev (derived)</th><th>Residual → B2B+Ent</th><th>B2B accounts</th><th>Implied blended B2B ACV</th></tr></thead>
      <tbody>
        <tr><td>2027</td><td>$1.0M</td><td>$0.36M (600 × $600/yr)</td><td>$0.64M</td><td>50</td><td><strong>~$12.8K</strong></td></tr>
        <tr class="row-accent"><td>2028</td><td>$8.0M</td><td>$3.6M (6,000 × $600/yr)</td><td>$4.4M</td><td>200</td><td><strong>~$22.0K</strong></td></tr>
        <tr><td>2029</td><td>$26.0M</td><td>$12.0M (20,000 × $600/yr)</td><td>$14.0M</td><td>500</td><td><strong>~$28.0K</strong></td></tr>
      </tbody>
    </table>
    <div class="chart-block"><h4>Derived revenue mix (B2C · B2B+Enterprise)</h4>{MIX_PATH}</div>
  </section>

  <!-- 11 PREREQ -->
  <section class="section flow" id="page-11" data-nav-label="12 · Prerequisites">
    <div class="section-head"><span class="section-num">12</span><h2>Financial prerequisites — contract scoreboard</h2></div>
    <p class="page-lead">Expected contract and logo results from marketing and sales so the plan financials hold. Seed size changes <strong>how fast</strong> GTM stands up — not CAC, LTV, or payback.</p>

    <h3>12.1 What “holding” means</h3>
    <table class="table-stack">
      <thead><tr><th>Horizon</th><th>Contracts / logos required</th><th>ARR / revenue required</th><th>Implied deal shape</th></tr></thead>
      <tbody>
        <tr><td><strong>In-seed ($2.5M)</strong></td><td><strong>5–10 pilots</strong> · <strong>50-lead pipeline</strong> · <strong>2–3 partners</strong></td><td><strong>$50–100K ARR</strong></td><td>Early B2B; mostly Starter-like</td></tr>
        <tr class="row-accent"><td><strong>End 2027</strong></td><td><strong>50 B2B</strong> + <strong>~600 paying consumers</strong></td><td><strong>~$1M</strong></td><td>Blended B2B ACV <strong>~$12.8K</strong> + B2C @ <strong>~$50 MRR</strong></td></tr>
        <tr><td><strong>End 2028</strong></td><td><strong>200 B2B</strong> + <strong>6,000+ consumers</strong></td><td><strong>~$8M</strong> (breakeven)</td><td>Blended B2B ACV <strong>~$22K</strong></td></tr>
        <tr class="row-accent"><td><strong>End 2029</strong></td><td><strong>500 B2B</strong> + <strong>20,000+ consumers</strong></td><td><strong>~$26M</strong></td><td>Blended B2B ACV <strong>~$28K</strong></td></tr>
        <tr><td><strong>Series A narrative</strong></td><td>Path toward <strong>~200 customers</strong></td><td>Sales + marketing ramp</td><td>Same unit economics</td></tr>
      </tbody>
    </table>
    <div class="flow-rail">
      <div class="flow-node"><strong>Seed proof</strong><span>5–10 pilots · $50–100K ARR</span></div>
      <div class="flow-arrow">→</div>
      <div class="flow-node alt"><strong>2027</strong><span>50 B2B · 600 B2C · ~$1M</span></div>
      <div class="flow-arrow">→</div>
      <div class="flow-node"><strong>2028</strong><span>200 B2B · 6K+ B2C · ~$8M</span></div>
      <div class="flow-arrow">→</div>
      <div class="flow-node ok"><strong>2029</strong><span>500 B2B · 20K+ B2C · ~$26M</span></div>
    </div>

    <h3 class="sub">12.2 Seed window — minimum for the plan to be “true”</h3>
    <table>
      <thead><tr><th>Result</th><th>Why it matters</th></tr></thead>
      <tbody>
        <tr><td><strong>5–10 live pilots / early contracts</strong></td><td>Commercial proof, not demo theater</td></tr>
        <tr class="row-accent"><td><strong>$50–100K ARR</strong></td><td>At ~$12–13K ACV ≈ <strong>4–8 paying B2B</strong>; at Starter mid ~$9K ≈ <strong>6–11</strong></td></tr>
        <tr><td><strong>50 qualified leads in pipeline</strong></td><td>Enough to staff Series A story</td></tr>
        <tr class="row-accent"><td><strong>2–3 channel partners live</strong></td><td>De-risks getting to ~50 logos</td></tr>
      </tbody>
    </table>
    <p class="side-note"><strong>Seed ($2.5M)</strong> must hit these proof gates. <strong>Accelerate ($5–7M)</strong> scales the same economics — not a higher ACV model.</p>

    <h3 class="sub">12.3 2027 — first year financials hold</h3>
    <table>
      <thead><tr><th>Book</th><th>Count</th><th>Revenue (derived)</th><th>What “a contract” looks like</th></tr></thead>
      <tbody>
        <tr><td>B2B (Starter/Pro/Ent mix)</td><td><strong>50</strong></td><td><strong>~$640K</strong></td><td>Avg <strong>~$12.8K ACV</strong> ≈ <strong>~$1,070/mo</strong> → mostly Starter, few Pro</td></tr>
        <tr class="row-accent"><td>B2C paid</td><td><strong>~600</strong></td><td><strong>~$360K</strong></td><td><strong>~$50 MRR</strong> after freemium</td></tr>
        <tr><td><strong>Total</strong></td><td></td><td><strong>~$1M</strong></td><td></td></tr>
      </tbody>
    </table>
    <p class="side-note"><strong>Net new after seed:</strong> if seed ends at 5–10 B2B, still need roughly <strong>+40–45 B2B</strong> into 2027, plus <strong>~600 paid B2C</strong>.</p>

    <h3 class="sub">12.4 2028 — breakeven year (hardest step-up)</h3>
    <table>
      <thead><tr><th>Book</th><th>Ending count</th><th>YoY net logos</th><th>Revenue (derived)</th><th>Deal quality bar</th></tr></thead>
      <tbody>
        <tr><td>B2B</td><td><strong>200</strong></td><td><strong>+150</strong> stock</td><td><strong>~$4.4M</strong></td><td>Avg ACV must rise to <strong>~$22K</strong></td></tr>
        <tr class="row-accent"><td>B2C</td><td><strong>6,000+</strong></td><td><strong>~+5,400</strong></td><td><strong>~$3.6M</strong></td><td>Still ~$50 MRR blend</td></tr>
        <tr><td><strong>Total</strong></td><td></td><td></td><td><strong>~$8M</strong></td><td></td></tr>
      </tbody>
    </table>
    <p class="side-note">With <strong>85–90% B2B retention</strong>, also replace churn: rough order <strong>~160–180 new B2B contracts</strong> in the 2027→2028 window to <strong>end at 200</strong> (not just +150 ignoring churn). Series A “path toward ~200” is essentially this 2028 B2B stock.</p>

    <h3 class="sub">12.5 2029 — $26M holds only if mix richens</h3>
    <table>
      <thead><tr><th>Book</th><th>Ending count</th><th>YoY net logos</th><th>Revenue (derived)</th><th>Deal quality bar</th></tr></thead>
      <tbody>
        <tr><td>B2B</td><td><strong>500</strong></td><td><strong>+300</strong> stock</td><td><strong>~$14M</strong></td><td>Avg ACV <strong>~$28K</strong> (Pro-heavy + Enterprise + premiums)</td></tr>
        <tr class="row-accent"><td>B2C</td><td><strong>20,000+</strong></td><td><strong>~+14,000</strong></td><td><strong>~$12M</strong></td><td>Volume motion stays cheap CAC</td></tr>
        <tr><td><strong>Total</strong></td><td></td><td></td><td><strong>~$26M</strong></td><td></td></tr>
      </tbody>
    </table>
    <p class="side-note">With 10–15% annual churn on a growing book, <strong>new B2B logos needed</strong> are closer to <strong>~320–350</strong> in that step, not 300.</p>

    <div class="ffc-charts">
      <div class="chart-block"><h4>B2B contract stock required (ending logos)</h4>{B2B_STOCK}<p class="bar-note">Seed bar ≈ midpoint of 4–11 logos implied by $50–100K ARR at ~$9–13K ACV.</p></div>
      <div class="chart-block"><h4>Required blended B2B ACV (USD thousands)</h4>{ACV_PATH}</div>
    </div>
  </section>

  <!-- 12 CAPACITY -->
  <section class="section flow" id="page-12" data-nav-label="13 · Mkt &amp; sales capacity">
    <div class="section-head"><span class="section-num">13</span><h2>Marketing spend &amp; sales capacity</h2></div>
    <p class="page-lead">Marketing program residuals (planning split) vs pricing CAC, and derived GTM headcount vs required contracts.</p>

    <h3>13.1 What marketing spend must “buy” (CAC capacity)</h3>
    <table class="table-stack">
      <thead><tr><th>Round</th><th>Marketing programs (approx.)</th><th>If spent at B2C CAC $20–30</th><th>If spent at Enterprise CAC $3–5K</th></tr></thead>
      <tbody>
        <tr><td>Seed ($2.5M)</td><td>~$698K</td><td>~23K–35K B2C logos <em>capacity</em></td><td>~140–230 Ent logos <em>capacity</em></td></tr>
        <tr class="row-accent"><td>Accelerate ($6M mid)</td><td>~$1.5M</td><td>~50K–75K B2C</td><td>~300–500 Ent</td></tr>
      </tbody>
    </table>
    <ul>
      <li><strong>2027 consumers (600)</strong> are cheap: at $25 CAC ≈ <strong>$15K</strong> of CAC — a small slice of even burn marketing.</li>
      <li><strong>2027’s 50 B2B</strong> are the scarce object: sales-assisted, 3–4 mo payback, not $25 CAC.</li>
      <li><strong>2028–29</strong> need marketing to feed both high B2C volume and a 50-lead→AE machine that upgrades ACV from ~$13K → ~$22K → ~$28K.</li>
    </ul>
    <div class="notify">
      <h5>Marketing job for financials to hold</h5>
      <p>1) Fill <strong>50 → pipeline → AE</strong> for B2B · 2) Convert freemium → <strong>paid B2C at ~$50 MRR</strong> · 3) Support <strong>land-and-expand</strong> so average B2B contract value rises each year. Not “spend the bucket.”</p>
    </div>

    <h3 class="sub">13.2 Sales capacity vs required contracts</h3>
    <table>
      <thead><tr><th>Round</th><th>Sales capacity</th><th>CS</th><th>Implied job for financials</th></tr></thead>
      <tbody>
        <tr><td>Seed ($2.5M)</td><td><strong>4.5 FTE</strong> sales</td><td><strong>1.0 FTE</strong></td><td>Close <strong>$50–100K ARR</strong> · 50-lead book · path to ~50 B2B</td></tr>
        <tr class="row-accent"><td>Accelerate ($5–7M)</td><td><strong>$2.5M</strong> sales team budget</td><td>CS tools in product line</td><td>Parallel logos toward <strong>~200 B2B / ~$8M</strong></td></tr>
      </tbody>
    </table>
    <p class="side-note">Illustrative productivity: seed <strong>4.5 Sales FTE</strong> toward 50 B2B by 2027 ≈ on the order of <strong>~3–5 new logos/month</strong> once ramped (plus partner-sourced). Accelerate’s <strong>$2.5M sales budget</strong> parallelizes logo math toward ~200. Partners (<strong>2–3</strong> in-seed) are part of the contract machine.</p>
  </section>

  <!-- 13 UNDERWRITE -->
  <section class="section flow" id="page-13" data-nav-label="14 · Underwriting">
    <div class="section-head"><span class="section-num">14</span><h2>Underwriting checklist &amp; failure modes</h2></div>
    <p class="page-lead">Five holds for diligence, the use-of-proceeds playbook, and what breaks the financials even when activity looks busy.</p>

    <div style="display:grid;gap:10px;margin:14px 0">
      <div class="notify"><h5>01 · Price from the shelf</h5><p>B2C Lite SKUs · B2B Starter/Pro bands · Enterprise $5K+/mo floor</p></div>
      <div class="notify alt"><h5>02 · Unit economics hold</h5><p>CAC / LTV / payback unchanged from Seed $2.5M to Accelerate $5–7M</p></div>
      <div class="notify"><h5>03 · Seed proof first</h5><p>$50–100K ARR · 5–10 pilots · 50 leads · 2–3 partners</p></div>
      <div class="notify alt"><h5>04 · Scale years</h5><p>$1M / $8M / $26M with 50→200→500 B2B and 600→6K→20K B2C</p></div>
      <div class="notify"><h5>05 · Contract quality rises</h5><p>Blended B2B ACV ~$13K → $22K → $28K with 85–90% retention · TAM share as ceiling context</p></div>
    </div>

    <h3 class="sub">Use-of-proceeds underwriting playbook</h3>
    <ol>
      <li><strong>Underwrite Seed $2.5M</strong> with the five-bucket split → <strong>~13.7 FTE</strong> + ~$1.23M non-people.</li>
      <li><strong>Then Accelerate $5–7M</strong> (Series A; mid often ~$6M on $20–30M pre) on the same metric frame.</li>
      <li><strong>Hold unit economics constant</strong> across Seed and Accelerate; measure speed KPIs, not a new CAC story.</li>
      <li><strong>Price seed headcount</strong> with §05 rates ($82 / $76 / $109 / $83 / $100K); do not treat Marketing or Tech as 100% people.</li>
      <li><strong>Compare rounds in §03</strong> — marketing, sales/GTM, tech/product, ops/runway, total raise.</li>
    </ol>

    <h3 class="sub">One-page expected-results checklist</h3>
    <table class="table-stack">
      <thead><tr><th>Stage</th><th>Expected contract results</th></tr></thead>
      <tbody>
        <tr><td><strong>Seed ($2.5M)</strong></td><td>5–10 pilots · <strong>$50–100K ARR</strong> · 50 leads · 2–3 partners</td></tr>
        <tr class="row-accent"><td><strong>2027</strong></td><td><strong>50 B2B</strong> @ ~<strong>$13K</strong> blended ACV · <strong>600</strong> paid B2C @ ~<strong>$50 MRR</strong> · <strong>~$1M</strong></td></tr>
        <tr><td><strong>2028</strong></td><td><strong>200 B2B</strong> @ ~<strong>$22K</strong> ACV · <strong>6,000+</strong> B2C · <strong>~$8M</strong> · retention <strong>85–90%</strong></td></tr>
        <tr class="row-accent"><td><strong>2029</strong></td><td><strong>500 B2B</strong> @ ~<strong>$28K</strong> ACV · <strong>20,000+</strong> B2C · <strong>~$26M</strong></td></tr>
        <tr><td><strong>Seed → Accelerate</strong></td><td>Same CAC/LTV/payback; Accelerate <strong>scales</strong> the same contract curve</td></tr>
      </tbody>
    </table>

    <h3 class="sub">Failure modes that break the financials</h3>
    <ul>
      <li>Lots of pilots but <strong>ARR &lt; $50K</strong> in-seed</li>
      <li>50 logos but <strong>ACV stuck ≪ $12K</strong> (cannot make $1M with 600 B2C alone)</li>
      <li>Hit logo counts but <strong>churn &gt; 10–15%</strong> (never reach 200/500 stock)</li>
      <li>B2C CAC blows past <strong>$20–30</strong> or paid conversion fails (2028–29 consumer revenue collapses)</li>
      <li>Mix never richens (ACV stuck at Starter) → <strong>$8M / $26M</strong> miss even at 200/500 logos</li>
    </ul>

    <div class="kicker">Bottom line: rising B2B book 50 → 200 → 500 with rising ACV ~$13K → $22K → $28K, plus B2C 600 → 6K → 20K at ~$50 MRR — gated by 5–10 pilots and $50–100K ARR in the $2.5M seed. Accelerate ($5–7M) buys scale on the same economics story.</div>
  </section>

  <!-- 14 JARGON -->
  <section class="section flow" id="page-14" data-nav-label="15 · Jargon">
    <div class="section-head"><span class="section-num">15</span><h2>Financial jargon in plain English</h2></div>
    <p class="page-lead">For non-financial readers. Skim the cheat sheet; use definitions when a term appears in a table.</p>

    <h3>Cheat sheet</h3>
    <div class="jargon-grid">
      <div class="jargon-item"><strong>Revenue</strong><p>Money customers pay you. Plan ~$1M → $8M → $26M.</p></div>
      <div class="jargon-item"><strong>ARR</strong><p>Yearly software run-rate if today’s subscriptions kept going for a year. Seed proof $50–100K ARR.</p></div>
      <div class="jargon-item"><strong>MRR</strong><p>Same idea per month. ARR ≈ MRR × 12. B2C avg ~$50 MRR.</p></div>
      <div class="jargon-item"><strong>ACV</strong><p>Typical yearly value of one business contract. B2B ~$12–36K; mix rises ~$13K → $22K → $28K.</p></div>
      <div class="jargon-item"><strong>CAC</strong><p>Spend to win one paying customer. B2C $20–30; Enterprise $3–5K.</p></div>
      <div class="jargon-item"><strong>LTV</strong><p>Total money expected from one customer over their life. Enterprise ~$144K.</p></div>
      <div class="jargon-item"><strong>LTV:CAC</strong><p>Dollars back per dollar spent to acquire (e.g. 30:1).</p></div>
      <div class="jargon-item"><strong>Payback</strong><p>Months until payments cover CAC. B2C 1–2 mo; B2B 3–4 mo.</p></div>
      <div class="jargon-item"><strong>Retention / churn</strong><p>Share who stay / leave. B2B plan 85–90% retention.</p></div>
      <div class="jargon-item"><strong>TAM</strong><p>Biggest market you could theoretically sell into. B2C $0.5–1.5B; B2B/Ent $2–4B.</p></div>
      <div class="jargon-item"><strong>Seed</strong><p>This plan’s seed ask is <strong>$2.5M</strong> for launch, pilots, and footprint.</p></div>
      <div class="jargon-item"><strong>Use of proceeds</strong><p>How invested money will be spent.</p></div>
      <div class="jargon-item"><strong>Speed / scale</strong><p>Accelerate scales GTM faster on the same unit economics — not a new model.</p></div>
      <div class="jargon-item"><strong>SAFE / note</strong><p>Cash in now; exact ownership % set later.</p></div>
      <div class="jargon-item"><strong>Pre- / post-money</strong><p>Company value before / after new cash. Accelerate framed at $20–30M pre.</p></div>
      <div class="jargon-item"><strong>Dilution</strong><p>Founders’ % ownership shrinks when new investors buy in.</p></div>
      <div class="jargon-item"><strong>FTE</strong><p>One full-time person’s year of work.</p></div>
      <div class="jargon-item"><strong>Logo</strong><p>One named customer account.</p></div>
      <div class="jargon-item"><strong>Pipeline</strong><p>List of potential deals being worked. Seed asks 50-lead pipeline.</p></div>
      <div class="jargon-item"><strong>Land-and-expand</strong><p>Start small, then sell more later — how ACV rises.</p></div>
      <div class="jargon-item"><strong>Freemium</strong><p>Free 60–90 days, then Lite / Pro.</p></div>
      <div class="jargon-item"><strong>GTM</strong><p>Go-to-market — how you sell and market.</p></div>
      <div class="jargon-item"><strong>Underwrite</strong><p>Investor judgment: “Can I trust these numbers?”</p></div>
      <div class="jargon-item"><strong>Unit economics</strong><p>Whether one customer is profitable on paper (CAC vs LTV).</p></div>
      <div class="jargon-item"><strong>Runway</strong><p>How many months you can keep operating with cash on hand before needing more capital or profits.</p></div>
      <div class="jargon-item"><strong>Breakeven</strong><p>Business stops losing money overall (~2028 on plan).</p></div>
      <div class="jargon-item"><strong>Accelerate</strong><p>Name for Series A in this plan: <strong>$5–7M</strong> on <strong>$20–30M</strong> pre (often ~$6M) after the $2.5M seed.</p></div>
      <div class="jargon-item"><strong>Footprint</strong><p>Where the company is set up (Greece, U.S., London).</p></div>
      <div class="jargon-item"><strong>Pilot</strong><p>First real-world trial — often limited — before a full contract.</p></div>
    </div>

    <h3 class="sub">ARR vs ACV vs MRR</h3>
    <div class="notify">
      <h5>Quick distinction</h5>
      <p><strong>MRR</strong> = monthly for one/many subscriptions. <strong>ACV</strong> = yearly value of one B2B deal. <strong>ARR</strong> = yearly run-rate across the book. If 50 customers average $12.8K ACV → ~$640K of that book’s ARR.</p>
    </div>

    <h3 class="sub">Phrases used in this financials pack</h3>
    <table>
      <thead><tr><th>Phrase</th><th>Plain English</th></tr></thead>
      <tbody>
        <tr><td><strong>Seed then Accelerate</strong></td><td>$2.5M seed first; Accelerate ($5–7M Series A) scales the same motions</td></tr>
        <tr class="row-accent"><td><strong>Unit economics hold</strong></td><td>Seed and Accelerate do not invent different customer math</td></tr>
        <tr><td><strong>Capital buys scale, not a rewrite</strong></td><td>More money → more people/ads/coverage sooner, not a new product thesis</td></tr>
        <tr class="row-accent"><td><strong>Financials hold</strong></td><td>Logo counts, ARR gates, retention, and average deal size stay on the plan path</td></tr>
        <tr><td><strong>Derived</strong></td><td>Calculated from other stated figures in this pack (e.g. mix check)</td></tr>
        <tr class="row-accent"><td><strong>Planning rates</strong></td><td>Modeling assumptions (e.g. $/FTE) used to map dollars to FTEs</td></tr>
        <tr><td><strong>Mix richens</strong></td><td>Average deal gets larger (more Pro/Enterprise), not only more logos</td></tr>
        <tr class="row-accent"><td><strong>Scarce object</strong></td><td>The hard thing to win (paying B2B logos, not cheap B2C clicks)</td></tr>
      </tbody>
    </table>

    <h3 class="sub">Tiny examples with EyeNet numbers</h3>
    <ul>
      <li><strong>ARR vs one contract:</strong> Starter ~$750/mo → ~$9K ACV. Ten such ≈ ~$90K ARR — inside seed $50–100K ARR gate.</li>
      <li><strong>CAC payback:</strong> Spend $25 to win B2C at $50/mo → payback about half a month to one month (plan 1–2 mo with friction).</li>
      <li><strong>LTV:CAC:</strong> Spend $30 CAC, get ~$900 LTV → 30:1.</li>
      <li><strong>Retention math:</strong> Start with 200 B2B at 90% retention → keep 180; must add new logos to end higher.</li>
      <li><strong>Accelerate pre/post:</strong> $20–30M pre + ~$6M mid → roughly 20–25% dilution at that round.</li>
    </ul>
  </section>

  <!-- 15 MASTER -->
  <section class="section flow" id="page-15" data-nav-label="16 · Master tables">
    <div class="section-head"><span class="section-num">16</span><h2>Master tables (appendix)</h2></div>
    <p class="page-lead">Canonical rollups for seed dollars, FTE, packages, unit economics, and revenue path.</p>

    <h3>Master dollar table — Seed vs Accelerate (USD thousands)</h3>
    <table class="table-stack">
      <thead><tr><th>Metric</th><th>Seed $2.5M</th><th>Accelerate $5–7M ($6M mid)</th></tr></thead>
      <tbody>
        <tr><td>Marketing / demand</td><td>850</td><td>1,500</td></tr>
        <tr class="row-accent"><td>Sales / GTM</td><td>1,000 (Pers 550 + Sales/ft 450)</td><td>2,500</td></tr>
        <tr><td>Tech / product</td><td>400</td><td>1,200</td></tr>
        <tr class="row-accent"><td>Ops / runway</td><td>250</td><td>800</td></tr>
        <tr><td><strong>Total</strong></td><td><strong>2,500</strong></td><td><strong>6,000 mid</strong></td></tr>
      </tbody>
    </table>

    <h3 class="sub">Master FTE table — Seed &amp; Accelerate (derived)</h3>
    <table class="table-stack">
      <thead><tr><th>Round</th><th>Eng</th><th>Sales</th><th>Mkt people</th><th>CS</th><th>Ops</th><th>FTE</th><th>People $</th><th>Non-people $</th></tr></thead>
      <tbody>
        <tr><td>Seed $2.5M</td><td>4.5</td><td>4.5</td><td>2.0</td><td>1.0</td><td>1.7</td><td><strong>13.7</strong></td><td>$1,265K</td><td>$1,235K</td></tr>
        <tr class="row-accent"><td>Accelerate $6M mid</td><td>7.0</td><td>21.0</td><td>4.0</td><td>1.0</td><td>—</td><td><strong>33.0</strong></td><td>$2,872K</td><td>$3,128K</td></tr>
      </tbody>
    </table>

    <h3 class="sub">Package price card</h3>
    <table class="table-stack">
      <thead><tr><th>Package</th><th>Recurring</th><th>ACV / other</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td>B2C Light</td><td>$20–$300/mo</td><td>Events $200–$1,200; avg MRR ~$50</td><td>Free 60–90 days</td></tr>
        <tr class="row-accent"><td>B2B Starter</td><td>$500–$1,000/mo</td><td>Part of ~$12–36K ACV path</td><td>1–5 sites, 5 cams</td></tr>
        <tr><td>B2B Professional</td><td>$1,500–$3,000/mo</td><td>Part of ~$12–36K ACV path</td><td>5–20 sites, 25 cams</td></tr>
        <tr class="row-accent"><td>B2B mobile/wearable</td><td>+40–60%</td><td>On applicable variants</td><td></td></tr>
        <tr><td>Enterprise</td><td>$5,000+/mo</td><td>$6K–$150K+/yr; avg often $12–20K+</td><td>Unlimited scale</td></tr>
      </tbody>
    </table>

    <h3 class="sub">Unit economics card</h3>
    <table>
      <thead><tr><th>Motion</th><th>CAC</th><th>LTV / ratio</th><th>Payback / retention</th></tr></thead>
      <tbody>
        <tr><td>B2C</td><td>$20–30</td><td>LTV:CAC ~30:1</td><td>1–2 mo</td></tr>
        <tr class="row-accent"><td>B2B</td><td>—</td><td>—</td><td>Retention 85–90% · payback 3–4 mo</td></tr>
        <tr><td>Enterprise</td><td>$3–5K</td><td>LTV ~$144K · ~40:1</td><td>Strategic tenure model</td></tr>
      </tbody>
    </table>

    <h3 class="sub">Revenue path card</h3>
    <table>
      <thead><tr><th>Year</th><th>Revenue</th><th>B2B</th><th>Consumers</th></tr></thead>
      <tbody>
        <tr><td>2027</td><td>~$1M</td><td>50</td><td>~600</td></tr>
        <tr class="row-accent"><td>2028</td><td>~$8M</td><td>200</td><td>6,000+</td></tr>
        <tr><td>2029</td><td>~$26M</td><td>500</td><td>20,000+</td></tr>
      </tbody>
    </table>

  </section>

  <!-- 16 SOURCES -->
  <section class="section flow" id="page-16" data-nav-label="17 · Sources">
    <div class="section-head"><span class="section-num">17</span><h2>Sources</h2></div>
    <p class="page-lead">Public references for addressable pockets [1]–[8] and dollar TAM category reports [9]–[12]. Enterprise segment-map dollars remain EyeNet plan targets; they are not census counts.</p>

    <h3>Addressable pockets (GTM counts)</h3>
    <ol class="addendum-list">
      <li id="ref-1"><span class="ref-num">[1]</span><div><span class="ref-label">U.S. Census CBP 2023 · NAICS 541613</span><span class="ref-use">B2C · ~52K marketing consulting establishments</span><a href="https://naicscodes.org/industry/54161-management-consulting-services/" target="_blank" rel="noopener noreferrer">https://naicscodes.org/industry/54161-management-consulting-services/</a></div></li>
      <li id="ref-2"><span class="ref-num">[2]</span><div><span class="ref-label">U.S. Census ACS 2024</span><span class="ref-use">B2C · ~87M owner-occupied homes</span><a href="https://data.census.gov/table/ACSDT1Y2024.C25075" target="_blank" rel="noopener noreferrer">https://data.census.gov/table/ACSDT1Y2024.C25075</a></div></li>
      <li id="ref-3"><span class="ref-num">[3]</span><div><span class="ref-label">Industry reports 2024 (CRE Daily)</span><span class="ref-use">B2C · ~0.8M U.S. Airbnb hosts</span><a href="https://www.credaily.com/briefs/the-political-influence-of-short-term-rentals-is-growing/" target="_blank" rel="noopener noreferrer">https://www.credaily.com/briefs/the-political-influence-of-short-term-rentals-is-growing/</a></div></li>
      <li id="ref-4"><span class="ref-num">[4]</span><div><span class="ref-label">NASCO 2024 white paper</span><span class="ref-use">B2C &amp; B2B · ~8K U.S. contract security companies</span><a href="https://www.nasco.org/wp-content/uploads/2024/09/2024_White_Paper.pdf" target="_blank" rel="noopener noreferrer">https://www.nasco.org/wp-content/uploads/2024/09/2024_White_Paper.pdf</a></div></li>
      <li id="ref-5"><span class="ref-num">[5]</span><div><span class="ref-label">U.S. Census Economic Census</span><span class="ref-use">B2C · ~1.0M+ retail establishments</span><a href="https://data.census.gov/table/ECNBASIC2022.EC2244BASIC" target="_blank" rel="noopener noreferrer">https://data.census.gov/table/ECNBASIC2022.EC2244BASIC</a></div></li>
      <li id="ref-6"><span class="ref-num">[6]</span><div><span class="ref-label">CBP / NAICS 7225</span><span class="ref-use">B2C · ~0.6M restaurant / eating-place establishments</span><a href="https://naicscodes.org/industry-group/7225-restaurants-and-other-eating-places/" target="_blank" rel="noopener noreferrer">https://naicscodes.org/industry-group/7225-restaurants-and-other-eating-places/</a></div></li>
      <li id="ref-7"><span class="ref-num">[7]</span><div><span class="ref-label">NCES SY 2024–25</span><span class="ref-use">B2B · ~99K public K–12 schools</span><a href="https://nces.ed.gov/ccd/tables/202425_summary_3.asp" target="_blank" rel="noopener noreferrer">https://nces.ed.gov/ccd/tables/202425_summary_3.asp</a></div></li>
      <li id="ref-8"><span class="ref-num">[8]</span><div><span class="ref-label">IBISWorld 2024</span><span class="ref-use">B2B · ~38K general warehousing &amp; storage businesses</span><a href="https://www.ibisworld.com/united-states/number-of-businesses/general-warehousing-storage/1224/" target="_blank" rel="noopener noreferrer">https://www.ibisworld.com/united-states/number-of-businesses/general-warehousing-storage/1224/</a></div></li>
    </ol>

    <h3>Dollar TAM — category reports</h3>
    <p class="side-note" style="margin-top:0">EyeNet’s $2–4B (B2B / Enterprise) and $0.5–1.5B (B2C) are conservative addressable slices of these larger markets — not the full global categories.</p>
    <ol class="addendum-list" start="9">
      <li id="ref-9"><span class="ref-num">[9]</span><div><span class="ref-label">Grand View Research — Video Analytics Market (2025–2030)</span><span class="ref-use">Global ~$12.7B (2024); North America ~33.2% share (~$4.2B) · B2B / Enterprise TAM context</span><a href="https://www.grandviewresearch.com/industry-analysis/video-analytics-market" target="_blank" rel="noopener noreferrer">https://www.grandviewresearch.com/industry-analysis/video-analytics-market</a></div></li>
      <li id="ref-10"><span class="ref-num">[10]</span><div><span class="ref-label">MarketsandMarkets — U.S. Video Analytics Market</span><span class="ref-use">U.S. ~$2.28B (2023) → ~$5.65B (2028) · brackets EyeNet B2B / Enterprise $2–4B band</span><a href="https://www.marketsandmarkets.com/Market-Reports/geography/intelligent-video-analytics-market/US" target="_blank" rel="noopener noreferrer">https://www.marketsandmarkets.com/Market-Reports/geography/intelligent-video-analytics-market/US</a></div></li>
      <li id="ref-11"><span class="ref-num">[11]</span><div><span class="ref-label">Grand View Research Horizon — U.S. Smart Home Security Camera</span><span class="ref-use">U.S. ~$3.68B (2024) · B2C ceiling; EyeNet $0.5–1.5B is a software / action slice</span><a href="https://www.grandviewresearch.com/horizon/outlook/smart-home-security-camera-market/united-states" target="_blank" rel="noopener noreferrer">https://www.grandviewresearch.com/horizon/outlook/smart-home-security-camera-market/united-states</a></div></li>
      <li id="ref-12"><span class="ref-num">[12]</span><div><span class="ref-label">MarketsandMarkets — U.S. VSaaS Market</span><span class="ref-use">U.S. ~$1.30B (2026) → ~$2.52B (2031) · cloud-incumbent adjacent (storage / bandwidth)</span><a href="https://www.marketsandmarkets.com/Market-Reports/geography/video-surveillance-as-a-service-market/US" target="_blank" rel="noopener noreferrer">https://www.marketsandmarkets.com/Market-Reports/geography/video-surveillance-as-a-service-market/US</a></div></li>
    </ol>

    <p class="footer-note">EyeNet Vision · Financials · Confidential. Share % and segment-map dollars are plan targets, not reported revenue. Specs subject to change.</p>
  </section>

</div>

  <nav class="doc-nav no-print" aria-label="Page navigation">
    <button type="button" class="doc-nav-prev">← Previous</button>
    <div class="doc-nav-mid">
      <span class="doc-nav-label"></span>
    </div>
    <button type="button" class="doc-nav-next">Next →</button>
  </nav>
{NAV_JS}
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>EyeNet Financials</title>
  {CSS}
  <style>{EXTRA_CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
