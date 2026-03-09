#!/usr/bin/env python3
"""
Professional Infographic Generator
Supports 20 layouts and multiple visual styles
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_image import generate_image

# Layout definitions
LAYOUTS = {
    "bridge": {
        "name": "Bridge",
        "description": "Problem → Solution, bridging the gap",
        "visual": "arch or bridge shape connecting two sides"
    },
    "circular-flow": {
        "name": "Circular Flow", 
        "description": "Cycles, recurring processes",
        "visual": "circular or cyclical flow diagram"
    },
    "comparison-table": {
        "name": "Comparison Table",
        "description": "Multi-factor comparison",
        "visual": "side-by-side comparison columns"
    },
    "do-dont": {
        "name": "Do vs Don't",
        "description": "Correct vs incorrect practices",
        "visual": "split screen with checkmarks and X marks"
    },
    "equation": {
        "name": "Equation",
        "description": "Formula breakdown, input → output",
        "visual": "mathematical or logical equation layout"
    },
    "feature-list": {
        "name": "Feature List",
        "description": "Product features, key points",
        "visual": "bullet points with icons"
    },
    "fishbone": {
        "name": "Fishbone",
        "description": "Root cause analysis",
        "visual": "fishbone or Ishikawa diagram"
    },
    "funnel": {
        "name": "Funnel",
        "description": "Conversion funnel, filtering process",
        "visual": "inverted pyramid or funnel shape"
    },
    "grid-cards": {
        "name": "Grid Cards",
        "description": "Multi-topic overview",
        "visual": "card grid layout"
    },
    "iceberg": {
        "name": "Iceberg",
        "description": "Surface vs hidden layers",
        "visual": "iceberg with visible and submerged parts"
    },
    "journey-path": {
        "name": "Journey Path",
        "description": "User journey, milestones",
        "visual": "winding path with milestones"
    },
    "layers-stack": {
        "name": "Layers Stack",
        "description": "Tech stack, layered structure",
        "visual": "stacked layers or cake layers"
    },
    "mind-map": {
        "name": "Mind Map",
        "description": "Brainstorming, idea expansion",
        "visual": "radial mind map with central concept"
    },
    "nested-circles": {
        "name": "Nested Circles",
        "description": "Influence levels, scope circles",
        "visual": "concentric circles"
    },
    "priority-quadrants": {
        "name": "Priority Quadrants",
        "description": "Four-quadrant matrix, prioritization",
        "visual": "2x2 matrix grid"
    },
    "pyramid": {
        "name": "Pyramid",
        "description": "Hierarchy, Maslow's needs",
        "visual": "pyramid with stacked levels"
    },
    "scale-balance": {
        "name": "Scale Balance",
        "description": "Pros vs cons, weighing options",
        "visual": "balance scale with two sides"
    },
    "timeline-horizontal": {
        "name": "Timeline",
        "description": "History, chronological events",
        "visual": "horizontal timeline"
    },
    "tree-hierarchy": {
        "name": "Tree Hierarchy",
        "description": "Org chart, taxonomy",
        "visual": "tree structure or org chart"
    },
    "venn": {
        "name": "Venn",
        "description": "Overlapping concepts",
        "visual": "Venn diagram with overlapping circles"
    }
}

# Visual styles
STYLES = {
    "craft-handmade": {
        "name": "Craft Handmade",
        "prompt": "handcrafted paper cutout style, artisanal textures, warm handmade aesthetic"
    },
    "technical-schematic": {
        "name": "Technical Schematic",
        "prompt": "technical blueprint style, precise lines, engineering schematic aesthetic"
    },
    "corporate-memphis": {
        "name": "Corporate Memphis",
        "prompt": "corporate memphis style, bold geometric shapes, vibrant business colors"
    },
    "minimal-clean": {
        "name": "Minimal Clean",
        "prompt": "minimalist clean design, generous whitespace, subtle colors, modern simplicity"
    },
    "vintage-retro": {
        "name": "Vintage Retro",
        "prompt": "vintage retro aesthetic, muted nostalgic colors, classic print style"
    },
    "futuristic-tech": {
        "name": "Futuristic Tech",
        "prompt": "futuristic tech style, neon accents, sleek digital aesthetic"
    },
    "organic-nature": {
        "name": "Organic Nature",
        "prompt": "organic nature-inspired, flowing natural forms, earthy color palette"
    },
    "playful-illustration": {
        "name": "Playful Illustration",
        "prompt": "playful illustration style, friendly characters, cheerful colors"
    }
}

def generate_infographic(
    content: str,
    output_path: str = "./infographic.png",
    layout: str = None,
    style: str = "craft-handmade",
    aspect: str = "landscape"
):
    """
    Generate professional infographic
    
    Args:
        content: Content to visualize
        output_path: Output file path
        layout: Layout type (auto-detected if None)
        style: Visual style
        aspect: Aspect ratio (landscape, portrait, square)
    """
    # Auto-detect layout if not specified
    if layout is None:
        layout = auto_detect_layout(content)
        print(f"🔍 Auto-detected layout: {layout}")
    
    if layout not in LAYOUTS:
        print(f"❌ Unknown layout: {layout}", file=sys.stderr)
        return False
    
    if style not in STYLES:
        print(f"❌ Unknown style: {style}", file=sys.stderr)
        return False
    
    layout_info = LAYOUTS[layout]
    style_info = STYLES[style]
    
    # Determine dimensions
    if aspect == "landscape":
        width, height = 1920, 1080
    elif aspect == "portrait":
        width, height = 1080, 1920
    else:  # square
        width, height = 1080, 1080
    
    # Build prompt
    prompt = f"""Professional infographic, {layout_info['name']} layout,
{layout_info['visual']}, {style_info['prompt']},
topic: "{content[:50]}",
clear information visualization, data presentation,
no text labels, pure visual diagram,
high quality, detailed"""
    
    prompt = " ".join(prompt.split())
    
    print(f"🎨 Generating infographic")
    print(f"   Layout: {layout_info['name']}")
    print(f"   Style: {style_info['name']}")
    print(f"   Aspect: {aspect}")
    print()
    
    return generate_image(prompt, output_path, width, height)

def auto_detect_layout(content: str) -> str:
    """Auto-detect best layout based on content analysis"""
    content_lower = content.lower()
    
    # Check for keywords
    if any(word in content_lower for word in ["problem", "solution", "挑战", "解决方案"]):
        return "bridge"
    elif any(word in content_lower for word in ["cycle", "loop", "循环", "周期"]):
        return "circular-flow"
    elif any(word in content_lower for word in ["compare", "vs", "对比", "比较"]):
        return "comparison-table"
    elif any(word in content_lower for word in ["do", "don't", "正确", "错误"]):
        return "do-dont"
    elif any(word in content_lower for word in ["formula", "equation", "公式", "方程"]):
        return "equation"
    elif any(word in content_lower for word in ["feature", "功能", "特点"]):
        return "feature-list"
    elif any(word in content_lower for word in ["cause", "reason", "原因", "根源"]):
        return "fishbone"
    elif any(word in content_lower for word in ["funnel", "convert", "漏斗", "转化"]):
        return "funnel"
    elif any(word in content_lower for word in ["surface", "hidden", "表面", "隐藏"]):
        return "iceberg"
    elif any(word in content_lower for word in ["journey", "path", "旅程", "路径"]):
        return "journey-path"
    elif any(word in content_lower for word in ["stack", "layer", "栈", "层"]):
        return "layers-stack"
    elif any(word in content_lower for word in ["mind map", "brainstorm", "思维导图", "头脑风暴"]):
        return "mind-map"
    elif any(word in content_lower for word in ["priority", "quadrant", "优先级", "象限"]):
        return "priority-quadrants"
    elif any(word in content_lower for word in ["hierarchy", "level", "层级", "金字塔"]):
        return "pyramid"
    elif any(word in content_lower for word in ["pros", "cons", "trade", "权衡", "利弊"]):
        return "scale-balance"
    elif any(word in content_lower for word in ["timeline", "history", "时间线", "历史"]):
        return "timeline-horizontal"
    elif any(word in content_lower for word in ["organization", "tree", "组织", "树形"]):
        return "tree-hierarchy"
    elif any(word in content_lower for word in ["overlap", "intersect", "交集", "重叠"]):
        return "venn"
    else:
        return "feature-list"  # Default

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate professional infographics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Layouts:
  {', '.join(LAYOUTS.keys())}

Styles:
  {', '.join(STYLES.keys())}

Examples:
  # Auto layout detection
  %(prog)s "AI发展史"
  
  # Specify layout and style
  %(prog)s "产品功能对比" --layout comparison-table --style corporate-memphis
  
  # Portrait aspect ratio
  %(prog)s "用户增长漏斗" --layout funnel --aspect portrait
"""
    )
    
    parser.add_argument("content", help="Content to visualize")
    parser.add_argument("-l", "--layout", 
                       choices=list(LAYOUTS.keys()),
                       help="Layout type (auto-detected if not specified)")
    parser.add_argument("-s", "--style", default="craft-handmade",
                       choices=list(STYLES.keys()),
                       help="Visual style (default: craft-handmade)")
    parser.add_argument("-a", "--aspect", default="landscape",
                       choices=["landscape", "portrait", "square"],
                       help="Aspect ratio (default: landscape)")
    parser.add_argument("-o", "--output", default="./infographic.png",
                       help="Output file path (default: ./infographic.png)")
    
    args = parser.parse_args()
    
    success = generate_infographic(
        content=args.content,
        output_path=args.output,
        layout=args.layout,
        style=args.style,
        aspect=args.aspect
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
