"""
Generate Universal Knowledge Assistant Logo
Creates a professional logo for the application.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def create_logo():
    """Create a professional logo for Universal Knowledge Assistant."""
    # Create a 512x512 image with transparent background
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors - Professional palette
    bg_color = (15, 15, 15, 255)  # Dark background
    accent_color = (100, 149, 237, 255)  # Cornflower blue
    text_color = (245, 245, 245, 255)  # Light text
    
    # Draw circular background
    margin = 40
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=bg_color,
        outline=accent_color,
        width=8
    )
    
    # Draw book/knowledge icon
    # Left page
    book_left = [
        (size // 2 - 120, size // 2 - 60),
        (size // 2 - 10, size // 2 - 80),
        (size // 2 - 10, size // 2 + 80),
        (size // 2 - 120, size // 2 + 60)
    ]
    draw.polygon(book_left, fill=accent_color)
    
    # Right page
    book_right = [
        (size // 2 + 10, size // 2 - 80),
        (size // 2 + 120, size // 2 - 60),
        (size // 2 + 120, size // 2 + 60),
        (size // 2 + 10, size // 2 + 80)
    ]
    draw.polygon(book_right, fill=accent_color)
    
    # Draw AI circuit lines overlay
    circuit_color = (150, 200, 255, 180)
    
    # Horizontal lines
    for i in range(3):
        y = size // 2 - 40 + i * 40
        draw.line([(size // 2 - 80, y), (size // 2 - 30, y)], fill=circuit_color, width=3)
        draw.line([(size // 2 + 30, y), (size // 2 + 80, y)], fill=circuit_color, width=3)
    
    # Draw connection nodes
    for i in range(3):
        y = size // 2 - 40 + i * 40
        draw.ellipse(
            [size // 2 - 85, y - 5, size // 2 - 75, y + 5],
            fill=circuit_color
        )
        draw.ellipse(
            [size // 2 + 75, y - 5, size // 2 + 85, y + 5],
            fill=circuit_color
        )
    
    # Save at different resolutions
    output_dir = Path(__file__).parent / "assets" / "universal-knowledge"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Main logo
    logo_path = output_dir / "LLM-Assistant-Logo.png"
    img.save(logo_path, "PNG")
    print(f"✅ Created logo: {logo_path}")
    
    # Android Chrome (192x192)
    android_chrome_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
    android_chrome_192.save(output_dir / "android-chrome-192x192.png", "PNG")
    print(f"✅ Created android-chrome-192x192.png")
    
    # Android Chrome (512x512)
    img.save(output_dir / "android-chrome-512x512.png", "PNG")
    print(f"✅ Created android-chrome-512x512.png")
    
    # Favicon sizes
    for size_val in [16, 32, 48]:
        favicon = img.resize((size_val, size_val), Image.Resampling.LANCZOS)
        favicon.save(output_dir / f"favicon-{size_val}x{size_val}.png", "PNG")
        print(f"✅ Created favicon-{size_val}x{size_val}.png")
    
    # Apple touch icon
    apple_touch = img.resize((180, 180), Image.Resampling.LANCZOS)
    apple_touch.save(output_dir / "apple-touch-icon.png", "PNG")
    print(f"✅ Created apple-touch-icon.png")
    
    # Generate ICO file (multi-resolution)
    img_256 = img.resize((256, 256), Image.Resampling.LANCZOS)
    img_256.save(
        output_dir / "app.ico",
        format='ICO',
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    )
    print(f"✅ Created app.ico")
    
    print("\n✅ All logo assets created successfully!")
    return logo_path


if __name__ == "__main__":
    create_logo()
