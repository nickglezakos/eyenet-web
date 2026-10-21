#!/usr/bin/env python3
"""Extract sections from copy file and replace them in current file using content-aware matching."""
import re, sys

def extract_section(html, section_id):
    """Extract a complete page section by its div id."""
    # Match from the opening div (with optional comment preceding it) through to the triple closing
    pattern = rf'<!-- [^>]*?Page[^>]*?-->\s*<div id="{section_id}" class="page[^>]*?">.*?</div>\s*</div>\s*</div>'
    m = re.search(pattern, html, re.DOTALL)
    if m:
        return m.group(0)
    # Try without comment
    pattern2 = rf'<div id="{section_id}" class="page[^>]*?">.*?</div>\s*</div>\s*</div>'
    m = re.search(pattern2, html, re.DOTALL)
    if m:
        return m.group(0)
    return None

def replace_section(html, section_id, new_html):
    """Replace a section by its id."""
    pattern = rf'<!-- [^>]*?Page[^>]*?-->\s*<div id="{section_id}" class="page[^>]*?">.*?</div>\s*</div>\s*</div>'
    result = re.sub(pattern, lambda _: new_html, html, count=1, flags=re.DOTALL)
    if result != html:
        return result
    pattern2 = rf'<div id="{section_id}" class="page[^>]*?">.*?</div>\s*</div>\s*</div>'
    result = re.sub(pattern2, lambda _: new_html, html, count=1, flags=re.DOTALL)
    return result

# Read files
with open('bp/index.html', 'r') as f:
    current = f.read()
with open('bp/index copy.html', 'r') as f:
    copy = f.read()

sections = ['home', 'executive', 'key-milestones', 'services']
for sid in sections:
    new_sec = extract_section(copy, sid)
    if not new_sec:
        print(f"ERROR: Could not extract '{sid}' from copy file")
        sys.exit(1)
    print(f"Extracted '{sid}' ({len(new_sec)} chars)")
    
    updated = replace_section(current, sid, new_sec)
    if updated == current:
        print(f"ERROR: Could not find '{sid}' in current file")
        sys.exit(1)
    current = updated
    print(f"Replaced '{sid}'")

with open('bp/index.html', 'w') as f:
    f.write(current)
print(f"\nDONE: Replaced all 4 sections ({len(current)} bytes total)")