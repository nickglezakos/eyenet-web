import os
import cairosvg
from PIL import Image
from io import BytesIO

# Create directory structure
base_dir = "assets/logos"
subdirs = ["svg", "png/full/light", "png/full/dark", "png/eye/light", "png/eye/dark", "favicon"]
for subdir in subdirs:
    os.makedirs(os.path.join(base_dir, subdir), exist_ok=True)

# Full EYENET logo SVG (light mode - original colors)
eyenet_light_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="5 5 285 70" xmlns="http://www.w3.org/2000/svg">
  <!-- E -->
  <rect x="10" y="10" width="8" height="60" fill="#0891b2" opacity="1"/>
  <rect x="18" y="10" width="25" height="8" fill="#0891b2" opacity="0.9"/>
  <rect x="18" y="36" width="20" height="8" fill="#0891b2" opacity="0.8"/>
  <rect x="18" y="62" width="25" height="8" fill="#0891b2" opacity="1"/>
  
  <!-- Y -->
  <rect x="55" y="10" width="8" height="25" fill="#22d3ee" opacity="1"/>
  <rect x="63" y="35" width="8" height="35" fill="#22d3ee" opacity="0.9"/>
  <rect x="71" y="10" width="8" height="25" fill="#22d3ee" opacity="0.8"/>
  
  <!-- E -->
  <rect x="95" y="10" width="8" height="60" fill="#06b6d4" opacity="1"/>
  <rect x="103" y="10" width="25" height="8" fill="#06b6d4" opacity="0.9"/>
  <rect x="103" y="36" width="20" height="8" fill="#06b6d4" opacity="0.8"/>
  <rect x="103" y="62" width="25" height="8" fill="#06b6d4" opacity="1"/>
  
  <!-- N -->
  <rect x="145" y="10" width="8" height="60" fill="#0891b2" opacity="1"/>
  <rect x="153" y="20" width="8" height="13" fill="#0891b2" opacity="0.9"/>
  <rect x="161" y="33" width="8" height="14" fill="#0891b2" opacity="0.8"/>
  <rect x="169" y="47" width="8" height="13" fill="#0891b2" opacity="0.9"/>
  <rect x="177" y="10" width="8" height="60" fill="#0891b2" opacity="1"/>
  
  <!-- E -->
  <rect x="200" y="10" width="8" height="60" fill="#22d3ee" opacity="1"/>
  <rect x="208" y="10" width="25" height="8" fill="#22d3ee" opacity="0.9"/>
  <rect x="208" y="36" width="20" height="8" fill="#22d3ee" opacity="0.8"/>
  <rect x="208" y="62" width="25" height="8" fill="#22d3ee" opacity="1"/>
  
  <!-- T -->
  <rect x="250" y="10" width="30" height="8" fill="#06b6d4" opacity="1"/>
  <rect x="261" y="18" width="8" height="52" fill="#06b6d4" opacity="0.9"/>
</svg>'''

# Full EYENET logo SVG (dark mode - lighter colors)
eyenet_dark_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="5 5 285 70" xmlns="http://www.w3.org/2000/svg">
  <!-- E -->
  <rect x="10" y="10" width="8" height="60" fill="#22d3ee" opacity="1"/>
  <rect x="18" y="10" width="25" height="8" fill="#22d3ee" opacity="0.9"/>
  <rect x="18" y="36" width="20" height="8" fill="#22d3ee" opacity="0.8"/>
  <rect x="18" y="62" width="25" height="8" fill="#22d3ee" opacity="1"/>
  
  <!-- Y -->
  <rect x="55" y="10" width="8" height="25" fill="#67e8f9" opacity="1"/>
  <rect x="63" y="35" width="8" height="35" fill="#67e8f9" opacity="0.9"/>
  <rect x="71" y="10" width="8" height="25" fill="#67e8f9" opacity="0.8"/>
  
  <!-- E -->
  <rect x="95" y="10" width="8" height="60" fill="#22d3ee" opacity="1"/>
  <rect x="103" y="10" width="25" height="8" fill="#22d3ee" opacity="0.9"/>
  <rect x="103" y="36" width="20" height="8" fill="#22d3ee" opacity="0.8"/>
  <rect x="103" y="62" width="25" height="8" fill="#22d3ee" opacity="1"/>
  
  <!-- N -->
  <rect x="145" y="10" width="8" height="60" fill="#22d3ee" opacity="1"/>
  <rect x="153" y="20" width="8" height="13" fill="#22d3ee" opacity="0.9"/>
  <rect x="161" y="33" width="8" height="14" fill="#22d3ee" opacity="0.8"/>
  <rect x="169" y="47" width="8" height="13" fill="#22d3ee" opacity="0.9"/>
  <rect x="177" y="10" width="8" height="60" fill="#22d3ee" opacity="1"/>
  
  <!-- E -->
  <rect x="200" y="10" width="8" height="60" fill="#67e8f9" opacity="1"/>
  <rect x="208" y="10" width="25" height="8" fill="#67e8f9" opacity="0.9"/>
  <rect x="208" y="36" width="20" height="8" fill="#67e8f9" opacity="0.8"/>
  <rect x="208" y="62" width="25" height="8" fill="#67e8f9" opacity="1"/>
  
  <!-- T -->
  <rect x="250" y="10" width="30" height="8" fill="#22d3ee" opacity="1"/>
  <rect x="261" y="18" width="8" height="52" fill="#22d3ee" opacity="0.9"/>
</svg>'''

# EYE only logo SVG (light mode)
eye_light_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="5 5 133 70" xmlns="http://www.w3.org/2000/svg">
  <!-- E -->
  <rect x="10" y="10" width="8" height="60" fill="#0891b2" opacity="1"/>
  <rect x="18" y="10" width="25" height="8" fill="#0891b2" opacity="0.9"/>
  <rect x="18" y="36" width="20" height="8" fill="#0891b2" opacity="0.8"/>
  <rect x="18" y="62" width="25" height="8" fill="#0891b2" opacity="1"/>
  
  <!-- Y -->
  <rect x="55" y="10" width="8" height="25" fill="#22d3ee" opacity="1"/>
  <rect x="63" y="35" width="8" height="35" fill="#22d3ee" opacity="0.9"/>
  <rect x="71" y="10" width="8" height="25" fill="#22d3ee" opacity="0.8"/>
  
  <!-- E -->
  <rect x="95" y="10" width="8" height="60" fill="#06b6d4" opacity="1"/>
  <rect x="103" y="10" width="25" height="8" fill="#06b6d4" opacity="0.9"/>
  <rect x="103" y="36" width="20" height="8" fill="#06b6d4" opacity="0.8"/>
  <rect x="103" y="62" width="25" height="8" fill="#06b6d4" opacity="1"/>
</svg>'''

# EYE only logo SVG (dark mode)
eye_dark_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="5 5 133 70" xmlns="http://www.w3.org/2000/svg">
  <!-- E -->
  <rect x="10" y="10" width="8" height="60" fill="#22d3ee" opacity="1"/>
  <rect x="18" y="10" width="25" height="8" fill="#22d3ee" opacity="0.9"/>
  <rect x="18" y="36" width="20" height="8" fill="#22d3ee" opacity="0.8"/>
  <rect x="18" y="62" width="25" height="8" fill="#22d3ee" opacity="1"/>
  
  <!-- Y -->
  <rect x="55" y="10" width="8" height="25" fill="#67e8f9" opacity="1"/>
  <rect x="63" y="35" width="8" height="35" fill="#67e8f9" opacity="0.9"/>
  <rect x="71" y="10" width="8" height="25" fill="#67e8f9" opacity="0.8"/>
  
  <!-- E -->
  <rect x="95" y="10" width="8" height="60" fill="#22d3ee" opacity="1"/>
  <rect x="103" y="10" width="25" height="8" fill="#22d3ee" opacity="0.9"/>
  <rect x="103" y="36" width="20" height="8" fill="#22d3ee" opacity="0.8"/>
  <rect x="103" y="62" width="25" height="8" fill="#22d3ee" opacity="1"/>
</svg>'''

# Save SVG files
with open(os.path.join(base_dir, "svg/eyenet-light.svg"), "w") as f:
    f.write(eyenet_light_svg)

with open(os.path.join(base_dir, "svg/eyenet-dark.svg"), "w") as f:
    f.write(eyenet_dark_svg)

with open(os.path.join(base_dir, "svg/eye-light.svg"), "w") as f:
    f.write(eye_light_svg)

with open(os.path.join(base_dir, "svg/eye-dark.svg"), "w") as f:
    f.write(eye_dark_svg)

print("✓ SVG files created")

# Define sizes for different screens
sizes = {
    "mobile": 192,      # 192px for mobile
    "tablet": 512,      # 512px for tablet
    "desktop": 1024     # 1024px for large screens
}

favicon_sizes = [16, 32, 48, 64, 128, 256]

def svg_to_png(svg_content, output_path, width):
    """Convert SVG to PNG with specified width"""
    png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), output_width=width)
    with open(output_path, 'wb') as f:
        f.write(png_data)

# Generate full EYENET logos
print("\nGenerating full EYENET logos...")
for size_name, width in sizes.items():
    # Light mode
    output_path = os.path.join(base_dir, f"png/full/light/eyenet-{size_name}-{width}px.png")
    svg_to_png(eyenet_light_svg, output_path, width)
    print(f"  ✓ Light mode {size_name}: {width}px")
    
    # Dark mode
    output_path = os.path.join(base_dir, f"png/full/dark/eyenet-{size_name}-{width}px.png")
    svg_to_png(eyenet_dark_svg, output_path, width)
    print(f"  ✓ Dark mode {size_name}: {width}px")

# Generate EYE only logos
print("\nGenerating EYE logos...")
for size_name, width in sizes.items():
    # Light mode
    output_path = os.path.join(base_dir, f"png/eye/light/eye-{size_name}-{width}px.png")
    svg_to_png(eye_light_svg, output_path, width)
    print(f"  ✓ Light mode {size_name}: {width}px")
    
    # Dark mode
    output_path = os.path.join(base_dir, f"png/eye/dark/eye-{size_name}-{width}px.png")
    svg_to_png(eye_dark_svg, output_path, width)
    print(f"  ✓ Dark mode {size_name}: {width}px")

# Generate favicons from EYE logo
print("\nGenerating favicons...")
for size in favicon_sizes:
    # Light mode favicon
    output_path = os.path.join(base_dir, f"favicon/favicon-light-{size}x{size}.png")
    svg_to_png(eye_light_svg, output_path, size)
    print(f"  ✓ Light mode favicon: {size}x{size}px")
    
    # Dark mode favicon
    output_path = os.path.join(base_dir, f"favicon/favicon-dark-{size}x{size}.png")
    svg_to_png(eye_dark_svg, output_path, size)
    print(f"  ✓ Dark mode favicon: {size}x{size}px")

# Create a standard favicon.ico from the 32px version
print("\nCreating favicon.ico files...")
for mode in ["light", "dark"]:
    images = []
    for size in [16, 32, 48]:
        png_path = os.path.join(base_dir, f"favicon/favicon-{mode}-{size}x{size}.png")
        img = Image.open(png_path)
        images.append(img)
    
    ico_path = os.path.join(base_dir, f"favicon/favicon-{mode}.ico")
    images[0].save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"  ✓ {mode.capitalize()} mode favicon.ico created")

print("\n" + "="*50)
print("✓ All logos generated successfully!")
print("="*50)
print("\nDirectory structure:")
print(f"  {base_dir}/")
print("    ├── svg/")
print("    │   ├── eyenet-light.svg")
print("    │   ├── eyenet-dark.svg")
print("    │   ├── eye-light.svg")
print("    │   └── eye-dark.svg")
print("    ├── png/")
print("    │   ├── full/")
print("    │   │   ├── light/ (3 sizes: mobile, tablet, desktop)")
print("    │   │   └── dark/ (3 sizes: mobile, tablet, desktop)")
print("    │   └── eye/")
print("    │       ├── light/ (3 sizes: mobile, tablet, desktop)")
print("    │       └── dark/ (3 sizes: mobile, tablet, desktop)")
print("    └── favicon/")
print("        ├── Multiple sizes (16, 32, 48, 64, 128, 256)")
print("        └── favicon-light.ico & favicon-dark.ico")
