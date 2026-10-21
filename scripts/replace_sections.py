#!/usr/bin/env python3
"""Replace sections in bp/index.html with content from bp/index copy.html"""

# Read both files
with open('bp/index.html', 'r') as f:
    current = f.readlines()

with open('bp/index copy.html', 'r') as f:
    copy = f.readlines()

# Sections to replace: (start_line_1based, end_line_1based)
# These are the div blocks for #home, #executive, #key-milestones, #services
sections = [
    (1041, 1111),   # #home
    (1112, 1603),   # #executive
    (1604, 1898),   # #key-milestones
    (1899, 2273),   # #services
]

# Replace each section in current with content from copy (0-indexed)
for start, end in sections:
    s = start - 1  # convert to 0-indexed
    e = end - 1
    current[s:e+1] = copy[s:e+1]

# Write result
with open('bp/index.html', 'w') as f:
    f.writelines(current)

print("DONE: Replaced sections home, executive, key-milestones, services from copy file")