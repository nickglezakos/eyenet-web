#!/usr/bin/env python3
"""Replace sections in bp/index.html with content from bp/index copy.html
Uses HTML comment markers to identify sections, not line numbers."""

import re

def extract_section(content, start_id):
    """Extract a page section from start comment/id to the closing </div></div></div>"""
    # Pattern: <!-- Name Page --><div id="xxx" class="page">...content...</div></div></div>
    # We match from the comment line through to the triple closing div that ends the page section
    pattern = rf'(<!-- .*? -->\s*<div id="{start_id}" class="page".*?</div>\s*</div>\s*</div>)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1)
    return None

def replace_section(content, section_html, section_id):
    """Replace a section in content identified by its div id"""
    pattern = rf'(<!-- .*? -->\s*<div id="{section_id}" class="page".*?</div>\s*</div>\s*</div>)'
    return re.sub(pattern, lambda m: section_html, content, count=1, flags=re.DOTALL)

# Read both files
with open('bp/index.html', 'r') as f:
    current = f.read()

with open('bp/index copy.html', 'r') as f:
    copy = f.read()

# Sections to replace: home, executive, key-milestones, services
sections = ['home', 'executive', 'key-milestones', 'services']

for section_id in sections:
    # Extract from copy
    section_html = extract_section(copy, section_id)
    if section_html is None:
        print(f"ERROR: Could not extract '{section_id}' from copy file")
        exit(1)
    print(f"Extracted '{section_id}' ({len(section_html)} chars)")

    # Replace in current
    new_current = replace_section(current, section_html, section_id)
    if new_current == current:
        print(f"ERROR: Could not find '{section_id}' in target file")
        exit(1)
    current = new_current
    print(f"Replaced '{section_id}'")

# Write result
with open('bp/index.html', 'w') as f:
    f.write(current)

print("\nDONE: Replaced all 4 sections successfully")