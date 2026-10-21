#!/usr/bin/env python3
"""Swap EYENET SENTINEL (5) and EYENET VRADAR (6) sections in roadmap."""
import sys

with open('bp/index.html', 'r') as f:
    content = f.read()

# Find the section boundaries
sentinel_start = content.index('<h3>5. EYENET SENTINEL</h3>')
vradar_start = content.index('<h3>6. EYENET VRADAR</h3>')
launch_strategy = content.index('<h2>Cross-Product Launch Strategy</h2>', vradar_start)

# Extract both sections
sentinel_section = content[sentinel_start:vradar_start]
vradar_section = content[vradar_start:launch_strategy]

print(f"Sentinel section: {len(sentinel_section)} chars (lines {sentinel_start}-{vradar_start-1})")
print(f"Vradar section: {len(vradar_section)} chars (lines {vradar_start}-{launch_strategy-1})")

# Build new content: swap the sections in place
new_content = (
    content[:sentinel_start] +
    vradar_section +   # Vradar goes first (becomes section 5)
    sentinel_section +  # Sentinel goes second (becomes section 6)
    content[launch_strategy:]
)

with open('bp/index.html', 'w') as f:
    f.write(new_content)

print("DONE: Swapped Sentinel and Vradar sections in roadmap")