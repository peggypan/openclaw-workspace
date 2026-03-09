#!/usr/bin/env python3
"""
Article Cover Image Generator
Generates 2.35:1 aspect ratio cover images for articles/blogs
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_image import generate_image

# Cover styles
STYLES = {
    "bold-typography": {
        "name": "Bold Typography",
        "prompt": "bold typography focus, large impactful text treatment, strong visual hierarchy"
    },
    "abstract-geometric": {
        "name": "Abstract Geometric",
        "prompt": "abstract geometric shapes, modern art composition, bold color blocks"
    },
    "photographic": {
        "name": "Photographic",
        "prompt": "professional photography style, cinematic composition, depth of field"
    },
    "illustrated": {
        "name": "Illustrated",
        "prompt": "custom illustration style, artistic interpretation, unique visual metaphor"
    },
    "minimalist": {
        "name": "Minimalist",
        "prompt": "minimalist design, generous negative space, single focal point, elegant simplicity"
    },
    "gradient-mesh": {
        "name": "Gradient Mesh",
        "prompt": "gradient mesh background, soft color transitions, modern digital aesthetic"
    },
    "duotone": {
        "name": "Duotone",
        "prompt": "duotone color scheme, two-color palette, high contrast artistic treatment"
    },
    "dark-moody": {
        "name": "Dark Moody",
        "prompt": "dark moody atmosphere, dramatic lighting, mysterious and sophisticated"
    }
}

def generate_cover(
    title: str,
    output_path: str = "./cover.png",
    style: str = "bold-typography",
    subtitle: str = None
):
    """
    Generate article cover image
    
    Args:
        title: Article title
        output_path: Output file path
        style: Visual style
        subtitle: Optional subtitle/description
    """
    if style not in STYLES:
        print(f"❌ Unknown style: {style}. Available: {', '.join(STYLES.keys())}", file=sys.stderr)
        return False
    
    style_info = STYLES[style]
    
    # Build prompt
    prompt = f"""Article cover image, 2.35:1 wide cinematic aspect ratio,
{style_info['prompt']},
topic: "{title}",
professional blog header image, eye-catching hero image,
no text, pure visual design,
suitable for article header, high quality"""
    
    if subtitle:
        prompt += f", context: {subtitle[:100]}"
    
    prompt = " ".join(prompt.split())
    
    print(f"🎨 Generating cover image")
    print(f"   Title: {title}")
    print(f"   Style: {style_info['name']}")
    print()
    
    # 2.35:1 aspect ratio - common cinematic/blog header size
    width, height = 2350, 1000
    
    return generate_image(prompt, output_path, width, height)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate article cover images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Styles:
  {', '.join(STYLES.keys())}

Examples:
  # Default bold typography
  %(prog)s "AI时代的内容创作"
  
  # Specific style
  %(prog)s "未来已来" --style gradient-mesh
  
  # With subtitle
  %(prog)s "深度学习入门" --style illustrated --subtitle "从零开始掌握神经网络"
"""
    )
    
    parser.add_argument("title", help="Article title")
    parser.add_argument("-s", "--style", default="bold-typography",
                       choices=list(STYLES.keys()),
                       help="Visual style (default: bold-typography)")
    parser.add_argument("--subtitle", help="Optional subtitle/description")
    parser.add_argument("-o", "--output", default="./cover.png",
                       help="Output file path (default: ./cover.png)")
    
    args = parser.parse_args()
    
    success = generate_cover(
        title=args.title,
        output_path=args.output,
        style=args.style,
        subtitle=args.subtitle
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
