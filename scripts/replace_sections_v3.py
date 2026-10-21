#!/usr/bin/env python3
"""Replace sections in bp/index.html using line ranges from copy file."""
import sys

# Read both files
with open('bp/index.html', 'r') as f:
    current_lines = f.readlines()

with open('bp/index copy.html', 'r') as f:
    copy_lines = f.readlines()

# Verify line counts are close
if abs(len(current_lines) - len(copy_lines)) > 2000:
    print(f"WARNING: File sizes differ significantly: current={len(current_lines)}, copy={len(copy_lines)}")

# Section line ranges (1-based, inclusive)
# These are the 4 sections to copy from the copy file
sections = [
    ('home', 1041, 1111),
    ('executive', 1112, 1603),
    ('key-milestones', 1604, 1898),
    ('services', 1899, 2273),
]

# Verify section IDs at start line
for name, start, end in sections:
    copy_line = copy_lines[start-1]
    curr_line = current_lines[start-1]
    if f'id="{name}"' not in copy_line:
        print(f"ERROR: Copy file doesn't have id=\"{name}\" at line {start}")
        print(f"  Found: {copy_line.rstrip()}")
        sys.exit(1)
    if f'id="{name}"' not in curr_line:
        print(f"ERROR: Current file doesn't have id=\"{name}\" at line {start}")
        print(f"  Found: {curr_line.rstrip()}")
        sys.exit(1)
    print(f"Verified '{name}' at line {start}")

# Replace each section
for name, start, end in sections:
    s = start - 1  # 0-indexed
    e = end - 1
    old_len = e - s + 1
    new_len = old_len  # same range
    current_lines[s:e+1] = copy_lines[s:e+1]
    print(f"Replaced '{name}' (lines {start}-{end}, {old_len} lines)")

# Write result
with open('bp/index.html', 'w') as f:
    f.writelines(current_lines)

print(f"\nDONE: Replaced all 4 sections. Total lines: {len(current_lines)}")