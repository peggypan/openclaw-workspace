#!/usr/bin/env python3
"""
Skill Builder - 打包脚本
验证并打包 Skill 为 .skill 文件
"""

import argparse
import os
import sys
import zipfile
import re
from pathlib import Path


def validate_frontmatter(content):
    """验证 YAML frontmatter"""
    errors = []
    
    # 检查是否有 frontmatter
    if not content.startswith("---"):
        errors.append("SKILL.md 必须以 '---' 开头")
        return errors
    
    # 提取 frontmatter
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        errors.append("找不到 frontmatter 结束标记 '---'")
        return errors
    
    frontmatter = content[3:3+end_match.start()]
    
    # 检查必需字段
    if "name:" not in frontmatter:
        errors.append("缺少必需字段: name")
    
    if "description:" not in frontmatter:
        errors.append("缺少必需字段: description")
    
    return errors


def validate_skill(skill_path):
    """验证 Skill 结构"""
    errors = []
    warnings = []
    
    skill_path = Path(skill_path)
    
    if not skill_path.exists():
        errors.append(f"路径不存在: {skill_path}")
        return errors, warnings
    
    if not skill_path.is_dir():
        errors.append(f"路径不是目录: {skill_path}")
        return errors, warnings
    
    # 检查 SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("缺少必需文件: SKILL.md")
    else:
        # 验证 frontmatter
        content = skill_md.read_text(encoding="utf-8")
        fm_errors = validate_frontmatter(content)
        errors.extend(fm_errors)
        
        # 检查内容长度
        body_start = content.find("\n---\n", 3)
        if body_start > 0:
            body = content[body_start + 5:]
            lines = body.strip().split("\n")
            if len(lines) > 500:
                warnings.append(f"SKILL.md 主体超过 500 行 ({len(lines)} 行)，建议拆分内容到 references/")
    
    # 检查不应存在的文件
    forbidden_files = ["README.md", "INSTALLATION.md", "CHANGELOG.md"]
    for ff in forbidden_files:
        if (skill_path / ff).exists():
            warnings.append(f"发现不必要的文件: {ff} (Skill 不需要辅助文档)")
    
    # 检查目录结构
    if (skill_path / "scripts").exists():
        scripts = list((skill_path / "scripts").glob("*"))
        if scripts:
            print(f"  ℹ️  发现 {len(scripts)} 个脚本")
    
    if (skill_path / "references").exists():
        refs = list((skill_path / "references").glob("*"))
        if refs:
            print(f"  ℹ️  发现 {len(refs)} 个参考资料文件")
    
    return errors, warnings


def package_skill(skill_path, output_dir=None):
    """打包 Skill 为 .skill 文件"""
    
    skill_path = Path(skill_path).resolve()
    skill_name = skill_path.name
    
    print(f"\n📦 打包 Skill: {skill_name}")
    print(f"📁 源目录: {skill_path}")
    
    # 验证
    print("\n🔍 正在验证...")
    errors, warnings = validate_skill(skill_path)
    
    if errors:
        print("\n❌ 验证失败:")
        for e in errors:
            print(f"   - {e}")
        return False
    
    if warnings:
        print("\n⚠️  警告:")
        for w in warnings:
            print(f"   - {w}")
    
    print("\n✅ 验证通过!")
    
    # 确定输出路径
    if output_dir:
        output_path = Path(output_dir).resolve()
    else:
        output_path = skill_path.parent
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 创建 .skill 文件（zip 格式）
    skill_file = output_path / f"{skill_name}.skill"
    
    print(f"\n🗜️  创建压缩包...")
    
    with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_path.rglob("*"):
            if file_path.is_file():
                # 跳过隐藏文件
                if any(part.startswith('.') for part in file_path.parts):
                    continue
                
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
                print(f"   + {arcname}")
    
    # 显示结果
    size = skill_file.stat().st_size
    print(f"\n✅ 打包完成!")
    print(f"📦 输出文件: {skill_file}")
    print(f"📊 文件大小: {size / 1024:.1f} KB")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="验证并打包 Skill 为 .skill 文件"
    )
    parser.add_argument(
        "skill_path",
        help="Skill 目录路径"
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        help="输出目录（默认: Skill 所在目录）"
    )
    
    args = parser.parse_args()
    
    success = package_skill(args.skill_path, args.output_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
