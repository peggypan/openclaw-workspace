#!/usr/bin/env python3
"""
打包 writing-style-guide skill
"""

import zipfile
import os
from pathlib import Path

skill_dir = Path("/root/.openclaw/workspace/skills/writing-style-guide")
output_file = Path("/root/.openclaw/workspace/skills/writing-style-guide.skill")

print("📦 打包 writing-style-guide...")

with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
    for file_path in skill_dir.rglob("*"):
        if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
            arcname = file_path.relative_to(skill_dir)
            zf.write(file_path, arcname)
            print(f"  + {arcname}")

size = output_file.stat().st_size
print(f"\n✅ 打包完成!")
print(f"📦 输出: {output_file}")
print(f"📊 大小: {size / 1024:.1f} KB")
