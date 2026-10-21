import re

with open('bp/index.html', 'r') as f:
    content = f.read()

# 1. Extract the temp-business-better section content
bb_pattern = r'<!-- Make Business Better Page -->\s*<div id="temp-business-better" class="page">\s*<div class="content-wrapper">\s*(.*?)\s*</div>\s*</div>\s*</div>'
match = re.search(bb_pattern, content, re.DOTALL)
if not match:
    print("ERROR: Could not find temp-business-better section")
    exit(1)

bb_inner = match.group(1)
bb_full = match.group(0)

# 2. Remove the temp-business-better section entirely
content = content.replace(bb_full, '')

# 3. Insert the business-better content into market-fundamentals before its closing tags
# Find: </div>\n        </div>\n\n        <!-- Competitive Analysis Page -->
old = '\n            </div>\n        </div>\n\n        <!-- Competitive Analysis Page -->'
new = '\n\n                <hr>\n\n                <h2>Real-World Impact</h2>\n' + bb_inner + '\n            </div>\n        </div>\n\n        <!-- Competitive Analysis Page -->'
content = content.replace(old, new)

# 4. Update the h1 title in market-fundamentals
content = content.replace('<h1>Customer Personas & Use Cases</h1>', '<h1>Market Fundamentals</h1>')

# 5. Update load handler: change personas → market-fundamentals
content = content.replace("currentPage && currentPage.id === 'personas'", "currentPage && currentPage.id === 'market-fundamentals'")

# 6. Update print-toc: merge personas and business-better
content = content.replace('<li>Personas</li>\n                <li>Competitive Analysis</li>\n                <li>Services & Platform Functionalities</li>\n                <li>Make Business Better</li>', 
                          '<li>Market Fundamentals</li>\n                <li>Competitive Analysis</li>\n                <li>Services & Platform Functionalities</li>')

# 7. Update Document Structure cards: merge Personas and Business Better into Market Fundamentals
content = content.replace(
    '<div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">\n                        <h3>Customer Personas</h3>\n                        <p>Detailed profiles of target customers including warehouse managers, educational institutes, industrial facilities, retail owners, and security services.</p>\n                    </div>',
    '<div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">\n                        <h3>Market Fundamentals</h3>\n                        <p>Six detailed customer personas with real-world use cases, ROI analysis, and proven business impact stories showing how EyeNet improves operations across industries.</p>\n                    </div>'
)

# Remove the old Make Business Better card
content = content.replace(
    '<div style="background: rgba(34, 211, 238, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(34, 211, 238, 0.2); backdrop-filter: blur(10px);">\n                        <h3>Make Business Better</h3>\n                        <p>Real stories from real businesses showing how EyeNet Vision improves operations across different industries.</p>\n                    </div>',
    ''
)

with open('bp/index.html', 'w') as f:
    f.write(content)

print("DONE: Merged sections successfully")