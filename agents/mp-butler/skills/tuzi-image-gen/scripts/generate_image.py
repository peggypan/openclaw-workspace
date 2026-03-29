#!/usr/bin/env python3
"""
TuziAPI 图片生成脚本
用法: python3 generate_image.py "提示词"
"""

import sys
import requests
import json

API_URL = "https://api.dashu.ai/tuziapi/images_generation"
TOKEN = "sk-ULZz57jJf2lkANMJsbZdxMEhVVWGgWl7xi1pluvfW0zntRtE"

def generate_image(prompt):
    """调用 TuziAPI 生成图片"""
    try:
        response = requests.post(
            API_URL,
            data={"prompt": prompt, "token": TOKEN},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            image_url = data["data"][0].get("url")
            revised_prompt = data["data"][0].get("revised_prompt", "")
            print(f"✅ 图片生成成功!")
            print(f"🖼️  图片地址: {image_url}")
            if revised_prompt:
                print(f"📝 优化提示词: {revised_prompt}")
            return image_url
        else:
            print(f"❌ 响应格式异常: {json.dumps(data, indent=2)}")
            return None
    except requests.exceptions.Timeout:
        print("❌ 请求超时，图片生成可能需要更长时间")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 generate_image.py '图片描述'")
        print("示例: python3 generate_image.py 'a cute cat in space'")
        sys.exit(1)
    
    prompt = sys.argv[1]
    print(f"🎨 正在生成图片: {prompt}")
    generate_image(prompt)
