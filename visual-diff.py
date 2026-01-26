import google.generativeai as genai
import os
from pathlib import Path
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def load_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def compare_screenshots(original_path, clone_path, page_name):
    """Compare two screenshots using Gemini Flash"""

    model = genai.GenerativeModel("gemini-2.0-flash")

    original_data = load_image(original_path)
    clone_data = load_image(clone_path)

    prompt = """You are a professional web designer doing a pixel-perfect comparison of two website screenshots.

IMAGE 1 is the ORIGINAL website (the target design).
IMAGE 2 is the CLONE website (attempting to replicate the original).

Analyze these two screenshots and provide a DETAILED list of ALL visual differences. Be extremely thorough and specific. For each difference, describe:

1. EXACT location on the page
2. What the original looks like
3. What the clone looks like
4. How to fix it (CSS properties, spacing values, colors, fonts, etc.)

Focus on:
- Typography (font family, size, weight, line-height, letter-spacing, case)
- Colors (exact hex values if possible)
- Spacing (margins, padding - estimate in pixels)
- Alignment (left/center/right, vertical positioning)
- Layout structure (flexbox/grid differences)
- Element sizing (width, height)
- Borders, shadows, border-radius
- Image positioning and sizing
- Any missing or extra elements

Be brutally honest and extremely detailed. List EVERY difference, no matter how small."""

    response = model.generate_content([
        prompt,
        {"mime_type": "image/png", "data": original_data},
        {"mime_type": "image/png", "data": clone_data}
    ])

    return response.text

def main():
    screenshots_dir = Path("screenshots")

    comparisons = [
        ("home-original-desktop.png", "home-clone-desktop.png", "Homepage Desktop"),
        ("home-original-mobile.png", "home-clone-mobile.png", "Homepage Mobile"),
        ("about-original-desktop.png", "about-clone-desktop.png", "About Desktop"),
        ("contact-original-desktop.png", "contact-clone-desktop.png", "Contact Desktop"),
    ]

    print("=" * 80)
    print("VISUAL DIFF REPORT - Gemini Flash Analysis")
    print("=" * 80)

    for original, clone, name in comparisons:
        original_path = screenshots_dir / original
        clone_path = screenshots_dir / clone

        if not original_path.exists() or not clone_path.exists():
            print(f"\n[SKIP] {name} - screenshots not found")
            continue

        print(f"\n{'=' * 80}")
        print(f"COMPARING: {name}")
        print("=" * 80)

        try:
            result = compare_screenshots(original_path, clone_path, name)
            print(result)
        except Exception as e:
            print(f"Error: {e}")

        print("\n")

if __name__ == "__main__":
    main()
