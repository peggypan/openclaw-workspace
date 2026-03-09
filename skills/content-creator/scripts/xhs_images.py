#!/usr/bin/env python3
"""
Xiaohongshu (小红书) Infographic Generator
Generates 3:4 aspect ratio images optimized for XHS/RedNote
"""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_image import generate_image

# Style definitions with enhanced visual characteristics
STYLES = {
    "cute": {
        "name": "可爱风",
        "description": "Soft pastels, rounded shapes, kawaii illustrations",
        "prompt_addition": "cute kawaii style, soft pastel colors, rounded friendly shapes, adorable illustrations, cheerful atmosphere"
    },
    "fresh": {
        "name": "清新风", 
        "description": "Light airy feel, nature elements, soft greens and blues",
        "prompt_addition": "fresh and clean aesthetic, natural light, soft green and blue tones, botanical elements, airy composition"
    },
    "warm": {
        "name": "温暖风",
        "description": "Cozy earth tones, warm lighting, inviting feel",
        "prompt_addition": "warm cozy atmosphere, earthy tones, golden hour lighting, inviting and comfortable, soft shadows"
    },
    "bold": {
        "name": "大胆风",
        "description": "High contrast, vibrant colors, strong typography",
        "prompt_addition": "bold and vibrant, high contrast, striking colors, strong visual impact, dynamic composition"
    },
    "minimal": {
        "name": "极简风",
        "description": "Clean lines, lots of whitespace, monochrome or duo-tone",
        "prompt_addition": "minimalist design, clean lines, generous whitespace, simple elegance, monochrome or duo-tone palette"
    },
    "retro": {
        "name": "复古风",
        "description": "Vintage aesthetics, muted colors, classic typography",
        "prompt_addition": "retro vintage style, muted nostalgic colors, classic typography, grain texture, timeless aesthetic"
    },
    "pop": {
        "name": "波普风",
        "description": "Bright colors, bold patterns, energetic and playful",
        "prompt_addition": "pop art style, bright bold colors, playful patterns, energetic and fun, comic-inspired elements"
    },
    "notion": {
        "name": "Notion风",
        "description": "Clean documentation style, subtle colors, organized layout",
        "prompt_addition": "clean documentation style, subtle neutral colors, organized grid layout, Notion-like aesthetic, professional and tidy"
    },
    "chalkboard": {
        "name": "黑板风",
        "description": "Dark background, white/chalk text, hand-drawn feel",
        "prompt_addition": "chalkboard style, dark background, white chalk-like text, hand-drawn illustrations, educational and artistic"
    }
}

# Layout definitions
LAYOUTS = {
    "sparse": {
        "name": "稀疏",
        "description": "1-2 key points, lots of breathing room",
        "density": "low",
        "points_range": (1, 2)
    },
    "balanced": {
        "name": "平衡",
        "description": "3-4 points, comfortable spacing", 
        "density": "medium",
        "points_range": (3, 4)
    },
    "dense": {
        "name": "密集",
        "description": "5-8 points, information-rich",
        "density": "high",
        "points_range": (5, 8)
    },
    "list": {
        "name": "列表",
        "description": "4-7 items in list format",
        "density": "medium",
        "points_range": (4, 7)
    },
    "comparison": {
        "name": "对比",
        "description": "Two-column comparison layout",
        "density": "medium",
        "points_range": (2, 4)
    },
    "flow": {
        "name": "流程",
        "description": "3-6 step process flow",
        "density": "medium",
        "points_range": (3, 6)
    }
}

def create_slug(text: str) -> str:
    """Create URL-friendly slug from text"""
    # Extract first 2-4 words
    words = text.split()[:4]
    slug = "-".join(words)
    # Remove non-alphanumeric except hyphens
    slug = re.sub(r'[^\w\-]', '', slug)
    return slug.lower()[:50]

def generate_xhs_images(
    content: str,
    output_dir: str = "./xhs-output",
    style: str = "cute",
    layout: str = "balanced",
    num_images: int = 3,
    topic: str = None
):
    """
    Generate XHS infographic series
    
    Args:
        content: Source content (text or file path)
        output_dir: Output directory
        style: Visual style (cute, fresh, warm, bold, minimal, retro, pop, notion, chalkboard)
        layout: Layout type (sparse, balanced, dense, list, comparison, flow)
        num_images: Number of images to generate (1-10)
        topic: Optional topic override
    """
    # Validate inputs
    if style not in STYLES:
        print(f"❌ Unknown style: {style}. Available: {', '.join(STYLES.keys())}", file=sys.stderr)
        return False
    
    if layout not in LAYOUTS:
        print(f"❌ Unknown layout: {layout}. Available: {', '.join(LAYOUTS.keys())}", file=sys.stderr)
        return False
    
    # Create output directory
    topic_slug = create_slug(topic or content[:50])
    session_dir = os.path.join(output_dir, topic_slug)
    os.makedirs(session_dir, exist_ok=True)
    
    style_info = STYLES[style]
    layout_info = LAYOUTS[layout]
    
    print(f"🎨 Generating {num_images} XHS images")
    print(f"   Style: {style_info['name']} ({style})")
    print(f"   Layout: {layout_info['name']} ({layout})")
    print(f"   Output: {session_dir}")
    print()
    
    # Generate images
    generated = []
    for i in range(1, num_images + 1):
        # Build prompt
        is_cover = (i == 1)
        
        if is_cover:
            prompt = f"""Xiaohongshu cover image, {style_info['prompt_addition']},
title: "{content[:30]}", eye-catching headline, attractive cover design,
3:4 vertical aspect ratio, optimized for mobile viewing,
no text, pure visual design"""
        else:
            prompt = f"""Xiaohongshu infographic, {style_info['prompt_addition']},
{layout_info['description']}, content card {i} of {num_images},
information visualization, clean and readable,
3:4 vertical aspect ratio, optimized for mobile viewing,
no text, pure visual design"""
        
        # Clean up prompt
        prompt = " ".join(prompt.split())
        
        # Generate
        output_file = os.path.join(session_dir, f"{i:02d}-{'cover' if is_cover else f'content-{i}'}-{topic_slug[:20]}.png")
        
        print(f"  Generating image {i}/{num_images}...")
        success = generate_image(
            prompt=prompt,
            output_path=output_file,
            width=1080,
            height=1440
        )
        
        if success:
            generated.append(output_file)
        
        print()
    
    print(f"✅ Generated {len(generated)}/{num_images} images in: {session_dir}")
    return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate Xiaohongshu (小红书) infographic series",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Styles:
  {', '.join(STYLES.keys())}

Layouts:
  {', '.join(LAYOUTS.keys())}

Examples:
  # Auto style/layout
  %(prog)s "AI未来的10个趋势"
  
  # Specify style and layout  
  %(prog)s "今日星座运势" --style notion --layout list
  
  # Generate 5 images
  %(prog)s "健身指南" --style bold --num 5
"""
    )
    
    parser.add_argument("content", help="Content text or file path")
    parser.add_argument("-s", "--style", default="cute", 
                       choices=list(STYLES.keys()),
                       help="Visual style (default: cute)")
    parser.add_argument("-l", "--layout", default="balanced",
                       choices=list(LAYOUTS.keys()),
                       help="Layout type (default: balanced)")
    parser.add_argument("-n", "--num", type=int, default=3,
                       help="Number of images (1-10, default: 3)")
    parser.add_argument("-o", "--output", default="./xhs-output",
                       help="Output directory (default: ./xhs-output)")
    parser.add_argument("-t", "--topic",
                       help="Topic slug (auto-generated from content if not specified)")
    
    args = parser.parse_args()
    
    # Validate num_images
    if args.num < 1 or args.num > 10:
        print("❌ num must be between 1 and 10", file=sys.stderr)
        sys.exit(1)
    
    success = generate_xhs_images(
        content=args.content,
        output_dir=args.output,
        style=args.style,
        layout=args.layout,
        num_images=args.num,
        topic=args.topic
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
