import re, subprocess

with open('bp/index.html', 'r') as f:
    content = f.read()

original = subprocess.check_output(
    ['git', 'show', 'd89bb65:bp/index.html'],
    cwd='/Users/nickgklezakos/Documents/eyenet-web'
).decode('utf-8')

# Find competitive section in original
comp_match = re.search(r'(<div id="competitive".*?</div>\s*</div>\s*</div>)', original, re.DOTALL)
# Find competitive section in current
current_comp_match = re.search(r'(<div id="competitive".*?</div>\s*</div>\s*</div>)', content, re.DOTALL)

if comp_match and current_comp_match:
    old_section = current_comp_match.group(1)
    new_section = comp_match.group(1)
    content = content.replace(old_section, new_section)
    with open('bp/index.html', 'w') as f:
        f.write(content)
    print('Success: replaced', len(old_section), 'chars with', len(new_section), 'chars')
else:
    print('FAIL: orig match =', comp_match is not None, 'current match =', current_comp_match is not None)