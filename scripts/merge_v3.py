#!/usr/bin/env python3
"""Line-based clean merge: personas + business-better → market-fundamentals."""
import sys

with open('bp/index.html', 'r') as f:
    lines = f.readlines()

# -- Find line numbers --
personas_start = None
personas_end = None  # line with the second </div> closing (closing content-wrapper)
personas_page_end = None  # line with the third </div> closing (closing the page div)

bb_start = None
bb_content_start = None
bb_content_end = None
bb_page_end = None

for i, line in enumerate(lines):
    if 'id="personas"' in line and personas_start is None:
        personas_start = i
    if 'id="business-better"' in line and bb_start is None:
        bb_start = i
    
# Find personas closing: we need the three consecutive </div> lines
# Pattern: </div>\n            </div>\n        </div>
# After personas content-wrapper closes, then page div closes
# Let's find the sequence near where competitive starts
for i in range(personas_start + 1, len(lines)):
    if '<!-- Competitive Analysis Page -->' in lines[i]:
        # The 3 lines before this comment should be the closing tags of personas
        # Actually personas ends before competitive starts
        # Look backwards for the pattern
        break

# Better approach: find the end of personas by looking for the sequence
# "            </div>\n        </div>\n\n        <!-- Competitive Analysis Page -->"
for i in range(personas_start + 1, len(lines) - 3):
    if (lines[i].strip() == '</div>' and lines[i+1].strip() == '</div>' and 
        ('<!-- Competitive Analysis Page -->' in lines[i+2] or 
         '<!-- Competitive Analysis Page -->' in lines[i+3])):
        personas_end = i
        personas_page_end = i + 1
        break

if personas_page_end is None:
    print("ERROR: Could not find personas closing")
    for i in range(max(0, len(lines)-20), len(lines)):
        if 'Competitive' in lines[i] or 'personas' in lines[i]:
            print(f"  Line {i+1}: {lines[i].rstrip()}")
    sys.exit(1)

# Find business-better structure
for i in range(bb_start + 1, len(lines)):
    if '<div class="content-wrapper">' in lines[i]:
        bb_content_start = i + 1  # first line of content after content-wrapper open
        break

# Find bb_content_end and bb_page_end
for i in range(bb_content_start, len(lines) - 4):
    if (lines[i].strip() == '</div>' and lines[i+1].strip() == '</div>' and 
        ('<!-- Financial' in lines[i+2] or '<!-- Financial' in lines[i+3])):
        bb_content_end = i - 1
        bb_page_end = i + 1
        break

if bb_content_end is None:
    print("ERROR: Could not find business-better closing")
    for i in range(bb_start, min(bb_start + 30, len(lines))):
        print(f"  Line {i+1}: {lines[i].rstrip()}")
    sys.exit(1)

print(f"Personas: start={personas_start+1}, content_end={personas_end+1}, page_end={personas_page_end+1}")
print(f"Business-better: start={bb_start+1}, content={bb_content_start+1}-{bb_content_end+1}, page_end={bb_page_end+1}")

# -- Extract business-better inner content (between content-wrapper open and close)
bb_inner_lines = lines[bb_content_start:bb_content_end+1]

# -- Remove business-better section entirely (from bb_start to bb_page_end inclusive)
del lines[bb_start:bb_page_end+1]

# Recalculate personas_end and personas_page_end since lines shifted
new_personas_end = None
new_personas_page_end = None
for i in range(personas_start + 1, len(lines) - 3):
    if (lines[i].strip() == '</div>' and lines[i+1].strip() == '</div>' and
        ('<!-- Competitive Analysis Page -->' in lines[i+2] or 
         '<!-- Competitive Analysis Page -->' in lines[i+3])):
        new_personas_end = i
        new_personas_page_end = i + 1
        break

if new_personas_page_end is None:
    print("ERROR: Lost personas closing after deletion")
    sys.exit(1)

# -- Insert bb_inner before personas closing --
# Add a hr + heading, then the bb content, then blank line
insertion = ['                <hr>\n',
             '\n',
             '                <h2>Real-World Impact</h2>\n',
             '<h3>Make Business Better</h3>\n']
lines[new_personas_end:new_personas_end] = insertion + bb_inner_lines + ['\n']

# -- Rename id="personas" → id="market-fundamentals" --
for i in range(len(lines)):
    lines[i] = lines[i].replace('id="personas"', 'id="market-fundamentals"')
    lines[i] = lines[i].replace('href="#personas"', 'href="#market-fundamentals"')

# -- Update badge-nav --
for i in range(len(lines)):
    lines[i] = lines[i].replace(
        'data-page="personas" onclick="showPage(\'personas\')">Personas</span>',
        'data-page="market-fundamentals" onclick="showPage(\'market-fundamentals\')">Market Fundamentals</span>')
    lines[i] = lines[i].replace(
        'data-page="business-better" onclick="showPage(\'business-better\')">Make Business Better</span>',
        '')
    # Remove leftover badge-nav line if empty
    if lines[i].strip() == '':
        lines[i] = ''

# -- Update sidebar nav link for personas --
for i in range(len(lines)):
    if 'Customer Personas' in lines[i] and 'href="#personas"' in lines[i-5]:
        # Find the block: <li><a href="#personas"...> ... Customer Personas </a></li>
        # It spans ~5 lines. We'll replace the href and label.
        for j in range(max(0,i-5), min(len(lines), i+2)):
            lines[j] = lines[j].replace('href="#personas"', 'href="#market-fundamentals"')
            lines[j] = lines[j].replace("showPage('personas')", "showPage('market-fundamentals')")
            lines[j] = lines[j].replace('Customer Personas', 'Market Fundamentals')
        break

# -- Remove sidebar nav link for business-better --
for i in range(len(lines)):
    if 'Make Business Better' in lines[i] and 'href="#business-better"' in lines[i-5]:
        # Remove the whole li block (~5 lines)
        for j in range(i-5, i+2):
            lines[j] = ''
        break

# -- Update pages array --
for i in range(len(lines)):
    if "id: 'personas'" in lines[i]:
        lines[i] = lines[i].replace("id: 'personas'", "id: 'market-fundamentals'")
        lines[i] = lines[i].replace("title: 'Customer Personas'", "title: 'Market Fundamentals'")
    if "id: 'business-better'" in lines[i]:
        lines[i] = ''
        # Also remove the trailing comma from the previous line if present
        if i > 0 and lines[i-1].rstrip().endswith(','):
            lines[i-1] = lines[i-1].rstrip()[:-1] + '\n'

# -- Update showPage chart init --
for i in range(len(lines)):
    lines[i] = lines[i].replace("if (pageId === 'personas')", "if (pageId === 'market-fundamentals')")
    lines[i] = lines[i].replace("// Initialize persona charts when personas page is shown", 
                                 "// Initialize market fundamentals charts when market-fundamentals page is shown")

# -- Update load handler --
for i in range(len(lines)):
    lines[i] = lines[i].replace("currentPage && currentPage.id === 'personas'", 
                                 "currentPage && currentPage.id === 'market-fundamentals'")

# -- Update print-toc --
for i in range(len(lines)):
    if '<li>Personas</li>' in lines[i]:
        lines[i] = lines[i].replace('<li>Personas</li>', '<li>Market Fundamentals</li>')
    if '<li>Make Business Better</li>' in lines[i]:
        lines[i] = ''

# -- Update h1 title --
for i in range(len(lines)):
    lines[i] = lines[i].replace('<h1>Customer Personas & Use Cases</h1>', '<h1>Market Fundamentals</h1>')

# -- Update Document Structure cards --
for i in range(len(lines)):
    if '<h3>Customer Personas</h3>' in lines[i]:
        lines[i] = lines[i].replace('<h3>Customer Personas</h3>', '<h3>Market Fundamentals</h3>')
        # Also update the description on the next line
        if i+1 < len(lines) and 'Detailed profiles' in lines[i+1]:
            lines[i+1] = lines[i+1].replace(
                'Detailed profiles of target customers including warehouse managers, educational institutes, industrial facilities, retail owners, and security services.',
                'Six detailed customer personas with real-world use cases, ROI analysis, and proven business impact stories showing how EyeNet improves operations across industries.')
    if '<h3>Make Business Better</h3>' in lines[i]:
        # Remove the entire card block (~4 lines)
        for j in range(i-1, i+3):
            if j < len(lines):
                lines[j] = ''

# Write output
with open('bp/index.html', 'w') as f:
    f.writelines(lines)

print("DONE: Clean merge complete")