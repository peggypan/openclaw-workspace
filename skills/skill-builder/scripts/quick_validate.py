#!/usr/bin/env python3
"""
Skill Builder - 快速验证脚本
检查 Skill 是否符合规范
"""

import argparse
import os
import sys
from pathlib import Path
import re


def check_skill(skill_path):
    """快速检查 Skill 合规性"""
    
    skill_path = Path(skill_path)
    issues = []
    suggestions = []
    
    print(f"🔍 检查: {skill_path.name}\n")
    
    # 1. 检查 SKILL.md 存在
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        issues.append("❌ 缺少 SKILL.md")
        return issues, suggestions
    else:
        print("✅ SKILL.md 存在")
    
    # 2. 读取并检查 frontmatter
    content = skill_md.read_text(encoding="utf-8")
    
    if not content.startswith("---"):
        issues.append("❌ SKILL.md 必须以 '---' 开头")
    else:
        # 提取 frontmatter
        end_match = re.search(r'\n---\s*\n', content[3:])
        if not end_match:
            issues.append("❌ 找不到 frontmatter 结束标记")
        else:
            frontmatter = content[3:3+end_match.start()]
            
            # 检查 name
            name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
            if not name_match:
                issues.append("❌ 缺少 name 字段")
            else:
                name = name_match.group(1).strip()
                print(f"✅ name: {name}")
            
            # 检查 description
            desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE | re.DOTALL)
            if not desc_match:
                issues.append("❌ 缺少 description 字段")
            else:
                desc = desc_match.group(1).strip().replace('\n', ' ')
                if len(desc) < 20:
                    suggestions.append(f"⚠️  description 较短 ({len(desc)} 字符)，建议更详细")
                else:
                    print(f"✅ description: {desc[:50]}...")
    
    # 3. 检查目录结构
    has_scripts = (skill_path / "scripts").exists()
    has_refs = (skill_path / "references").exists()
    has_assets = (skill_path / "assets").exists()
    
    if has_scripts:
        scripts = list((skill_path / "scripts").glob("*"))
        scripts = [s for s in scripts if s.is_file() and not s.name.startswith('.')]
        print(f"✅ scripts/: {len(scripts)} 个文件")
    
    if has_refs:
        refs = list((skill_path / "references").glob("*"))
        refs = [r for r in refs if r.is_file() and not r.name.startswith('.')]
        print(f"✅ references/: {len(refs)} 个文件")
    
    if has_assets:
        assets = list((skill_path / "assets").glob("*"))
        assets = [a for a in assets if not a.name.startswith('.')]
        print(f"✅ assets/: {len(assets)} 个文件")
    
    # 4. 检查不应存在的文件
    forbidden = ["README.md", "CHANGELOG.md", "INSTALL.md", "LICENSE.md"]
    for f in forbidden:
        if (skill_path / f).exists():
            suggestions.append(f"⚠️  发现不必要的文件: {f}")
    
    return issues, suggestions


def main():
    parser = argparse.ArgumentParser(
        description="快速验证 Skill 是否符合规范"
    )
    parser.add_argument(
        "skill_path",
        help="Skill 目录路径"
    )
    
    args = parser.parse_args()
    
    issues, suggestions = check_skill(args.skill_path)
    
    print("\n" + "="*50)
    
    if issues:
        print(f"\n❌ 发现 {len(issues)} 个问题:")
        for i in issues:
            print(f"   {i}")
    
    if suggestions:
        print(f"\n💡 建议:")
        for s in suggestions:
            print(f"   {s}")
    
    if not issues and not suggestions:
        print("\n✅ 检查通过！Skill 符合规范。")
    elif not issues:
        print("\n✅ 基本符合规范，但有一些建议。")
    else:
        print(f"\n❌ 请修复上述问题后再打包。")
        sys.exit(1)


if __name__ == "__main__":
    main()
