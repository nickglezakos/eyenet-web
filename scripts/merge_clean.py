#!/usr/bin/env python3
"""Clean merge of #personas and #business-better into #market-fundamentals."""
import re, subprocess

with open('bp/index.html', 'r') as f:
    content = f.read()

# ============================================================
# STEP 1: Extract #business-better inner content (just what's inside content-wrapper)
# ============================================================
bb_pattern = r'<div id="business-better" class="page">\s*<div class="content-wrapper">\s*(.*?)\s*</div>\s*</div>\s*</div>'
bb_match = re.search(bb_pattern, content, re.DOTALL)
if not bb_match:
    print("ERROR: Could not find business-better section")
    exit(1)
bb_inner = bb_match.group(1)
bb_full = bb_match.group(0)

# ============================================================
# STEP 2: Remove the #business-better page completely
# ============================================================
content = content.replace(bb_full + '\n', '')

# ============================================================
# STEP 3: Insert bb_inner into #personas before its closing tags
#         Find the closing of personas: </div>\n            </div>\n        </div>
#         Replace with: extra content + the closing tags
# ============================================================
old_close = '            </div>\n        </div>\n\n        <!-- Competitive Analysis Page -->'
new_content = '                <hr>\n\n                <h2>Real-World Impact</h2>\n<h3>Make Business Better</h3>\n' + bb_inner + '\n\n            </div>\n        </div>\n\n        <!-- Competitive Analysis Page -->'
content = content.replace(old_close, new_content)

# ============================================================
# STEP 4: Rename #personas -> #market-fundamentals
# ============================================================
content = content.replace('id="personas"', 'id="market-fundamentals"')
content = content.replace('href="#personas"', 'href="#market-fundamentals"')

# ============================================================
# STEP 5: Update badge-nav
# ============================================================
content = content.replace(
    '<span class="badge-nav" data-page="personas" onclick="showPage(\'personas\')">Personas</span>',
    '<span class="badge-nav" data-page="market-fundamentals" onclick="showPage(\'market-fundamentals\')">Market Fundamentals</span>'
)
content = content.replace(
    '<span class="badge-nav" data-page="business-better" onclick="showPage(\'business-better\')">Make Business Better</span>\n',
    ''
)

# ============================================================
# STEP 6: Update sidebar nav links
# ============================================================
content = content.replace(
    '<li><a href="#personas" class="nav-link" onclick="showPage(\'personas\')">\n                <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">\n                    <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>\n                </svg>\n                Customer Personas\n            </a></li>',
    '<li><a href="#market-fundamentals" class="nav-link" onclick="showPage(\'market-fundamentals\')">\n                <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">\n                    <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>\n                </svg>\n                Market Fundamentals\n            </a></li>'
)

content = content.replace(
    '<li><a href="#business-better" class="nav-link" onclick="showPage(\'business-better\')">\n                <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">\n                    <path d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>\n                </svg>\n                Make Business Better\n            </a></li>\n',
    ''
)

# ============================================================
# STEP 7: Update pages array
# ============================================================
content = content.replace(
    "{ id: 'personas', title: 'Customer Personas' },\n            { id: 'competitive', title: 'Competitive Analysis' },\n            { id: 'business-better', title: 'Make Business Better' },",
    "{ id: 'market-fundamentals', title: 'Market Fundamentals' },\n            { id: 'competitive', title: 'Competitive Analysis' },"
)

# ============================================================
# STEP 8: Update showPage chart init block
# ============================================================
content = content.replace(
    "if (pageId === 'personas')",
    "if (pageId === 'market-fundamentals')"
)
content = content.replace(
    "// Initialize persona charts when personas page is shown",
    "// Initialize market fundamentals charts when market-fundamentals page is shown"
)

# ============================================================
# STEP 9: Update load handler
# ============================================================
content = content.replace(
    "currentPage && currentPage.id === 'personas'",
    "currentPage && currentPage.id === 'market-fundamentals'"
)

# ============================================================
# STEP 10: Update print-toc
# ============================================================
content = content.replace(
    '<li>Personas</li>\n                <li>Competitive Analysis</li>\n                <li>Services & Platform Functionalities</li>\n                <li>Make Business Better</li>',
    '<li>Market Fundamentals</li>\n                <li>Competitive Analysis</li>\n                <li>Services & Platform Functionalities</li>'
)

# ============================================================
# STEP 11: Update Document Structure cards
# ============================================================
content = content.replace(
    '<h3>Customer Personas</h3>\n                        <p>Detailed profiles of target customers including warehouse managers, educational institutes, industrial facilities, retail owners, and security services.</p>',
    '<h3>Market Fundamentals</h3>\n                        <p>Six detailed customer personas with real-world use cases, ROI analysis, and proven business impact stories showing how EyeNet improves operations across industries.</p>'
)

content = content.replace(
    '<div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">\n                        <h3>Make Business Better</h3>\n                        <p>Real stories from real businesses showing how EyeNet Vision improves operations across different industries.</p>\n                    </div>',
    ''
)

# ============================================================
# STEP 12: Update h1 title in market-fundamentals
# ============================================================
content = content.replace(
    '<h1>Customer Personas & Use Cases</h1>',
    '<h1>Market Fundamentals</h1>'
)

# ============================================================
# STEP 13: Re-order Document Structure cards to match badge-nav sequence
# ============================================================
# Find the grid and replace it all with proper ordering
old_grid = '''                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Services & Platform Functionalities</h3>
                        <p>Five specialised applications from Presence to Matrix plus core platform capabilities — computer vision, intelligent triggers, event-driven automation, and more.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Market Fundamentals</h3>
                        <p>Six detailed customer personas with real-world use cases, ROI analysis, and proven business impact stories showing how EyeNet improves operations across industries.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Competitive Analysis</h3>
                        <p>Comprehensive analysis of EyeNet Vision\'s commercial product offerings, competitive positioning, and market opportunities.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Financial Model</h3>
                        <p>Dual-model revenue strategy with 3-year projections showing growth from $1M to $26M ARR.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Investor Strategy</h3>
                        <p>Investment rounds overview, valuation timeline, and clear exit paths (IPO or strategic acquisition).</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Product Roadmap</h3>
                        <p>Development status and launch timeline for all six product applications across deployment modes.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Key Milestones</h3>
                        <p>Five-phase journey from concept to scale — EyeNet operates at the intersection of Phases 3 and 4, validating product-market fit while building the go-to-market engine for Q2 2026 launch.</p>
                    </div>'''

new_grid = '''                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Executive Summary</h3>
                        <p>Investment opportunity overview, financial projections, product portfolio, competitive advantages, and risk mitigation — the complete at-a-glance summary.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Key Milestones</h3>
                        <p>Five-phase journey from concept to scale — EyeNet operates at the intersection of Phases 3 and 4, validating product-market fit while building the go-to-market engine for Q2 2026 launch.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Services & Platform Functionalities</h3>
                        <p>Five specialised applications from Presence to Matrix plus core platform capabilities — computer vision, intelligent triggers, event-driven automation, and more.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Market Fundamentals</h3>
                        <p>Six detailed customer personas with real-world use cases, ROI analysis, and proven business impact stories showing how EyeNet improves operations across industries.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Competitive Analysis</h3>
                        <p>Comprehensive analysis of EyeNet Vision\'s commercial product offerings, competitive positioning, and market opportunities.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Financial Model</h3>
                        <p>Dual-model revenue strategy with 3-year projections showing growth from $1M to $26M ARR.</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Investor Strategy</h3>
                        <p>Investment rounds overview, valuation timeline, and clear exit paths (IPO or strategic acquisition).</p>
                    </div>
                    <div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">
                        <h3>Product Roadmap</h3>
                        <p>Development status and launch timeline for all six product applications across deployment modes.</p>
                    </div>'''

content = content.replace(old_grid, new_grid)

# ============================================================
# STEP 14: Insert Key Milestones box at Key Highlights (from previous work)
# ============================================================
old_highlights = '''                <div class="info-box">
                    <h3>Strategic Advantages</h3>'''
new_highlights = '''                <div class="info-box">
                    <h3>Key Milestones</h3>
                    <ul>
                        <li><strong>Conceived July 2024</strong>: Working prototype delivered within two months</li>
                        <li><strong>5 of 6 Apps Beta-Ready</strong>: Launching Q2 2026 across five deployment modes</li>
                        <li><strong>Navigating Phases 3 & 4</strong>: Validating product-market fit while building the go-to-market engine</li>
                        <li><strong>Two Distribution Partners</strong>: TMA (EyeNet-branded) and NewGen Group (white-label) actively building pipeline</li>
                        <li><strong>Deloitte EMEA Pitch</strong>: NewGen presenting to Deloitte EMEA Cyber Security Committee September 2026</li>
                        <li><strong>Funding Path</strong>: Seed $2.5M → Series A $5-7M → Target $26M ARR by 2028</li>
                    </ul>
                </div>

                <div class="info-box">
                    <h3>Strategic Advantages</h3>'''
content = content.replace(old_highlights, new_highlights)

# ============================================================
# WRITE OUTPUT
# ============================================================
with open('bp/index.html', 'w') as f:
    f.write(content)

print("DONE: Clean merge complete")