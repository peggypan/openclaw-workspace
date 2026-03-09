#!/usr/bin/env python3
"""
Pollinations AI Image Generator
Free, no-login image generation API wrapper
"""

import urllib.request
import urllib.parse
import sys
import os

def generate_image(prompt: str, output_path: str, width: int = 1024, height: int = 1024, seed: int = None):
    """
    Generate image using Pollinations.ai API
    
    Args:
        prompt: Image description/prompt
        output_path: Where to save the generated image
        width: Image width (default 1024)
        height: Image height (default 1024)
        seed: Random seed for reproducibility (optional)
    """
    # URL encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Build URL
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
    if seed:
        url += f"&seed={seed}"
    
    # Download image
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            # Create output directory if needed
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Save image
            with open(output_path, 'wb') as f:
                f.write(response.read())
        
        print(f"✅ Image saved: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating image: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate images using Pollinations.ai")
    parser.add_argument("prompt", help="Image prompt/description")
    parser.add_argument("-o", "--output", default="output.png", help="Output file path")
    parser.add_argument("-W", "--width", type=int, default=1024, help="Image width")
    parser.add_argument("-H", "--height", type=int, default=1024, help="Image height")
    parser.add_argument("-s", "--seed", type=int, help="Random seed")
    
    args = parser.parse_args()
    
    success = generate_image(args.prompt, args.output, args.width, args.height, args.seed)
    sys.exit(0 if success else 1)
