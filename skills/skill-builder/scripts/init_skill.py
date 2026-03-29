#!/usr/bin/env python3
"""
Skill Builder - 初始化脚本
生成新的 Skill 模板目录
"""

import argparse
import os
import sys
from datetime import datetime

SKILL_MD_TEMPLATE = '''---
name: {skill_name}
description: {description}
---

# {skill_name}

{description}

## 快速开始

[在这里添加快速上手指南]

## 功能

- [ ] 功能 1
- [ ] 功能 2
- [ ] 功能 3

## 使用示例

### 示例 1: [场景描述]

```bash
# 命令示例
```

### 示例 2: [场景描述]

```python
# 代码示例
```

## 详细文档

- 详见 [references/README.md](references/README.md)

## 资源

- `scripts/` - 可执行脚本
- `references/` - 参考资料
- `assets/` - 模板和资源文件
'''

REFERENCE_TEMPLATE = '''# {skill_name} 参考资料

## 目录

1. [概述](#概述)
2. [详细用法](#详细用法)
3. [配置选项](#配置选项)
4. [常见问题](#常见问题)

## 概述

[在这里添加概述]

## 详细用法

### 用法 1

[详细说明]

### 用法 2

[详细说明]

## 配置选项

| 选项 | 类型 | 默认值 | 说明 |
|-----|------|--------|------|
| option1 | string | "default" | 说明 |
| option2 | int | 10 | 说明 |

## 常见问题

**Q: 问题1？**
A: 答案1

**Q: 问题2？**
A: 答案2
'''

SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
"""
{skill_name} - 示例脚本

用法:
    python {script_name}.py [参数]
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="{skill_name} 工具")
    parser.add_argument("input", help="输入文件或目录")
    parser.add_argument("-o", "--output", help="输出路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    # TODO: 实现功能
    print(f"处理: {{args.input}}")
    if args.output:
        print(f"输出到: {{args.output}}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

def create_skill(skill_name, output_path, description=None):
    """创建新的 Skill 目录结构"""
    
    if not description:
        description = f"处理 {skill_name} 相关任务的 Skill"
    
    # 创建主目录
    skill_dir = os.path.join(output_path, skill_name)
    
    if os.path.exists(skill_dir):
        print(f"❌ 错误: 目录已存在: {skill_dir}")
        return False
    
    # 创建目录结构
    dirs = [
        skill_dir,
        os.path.join(skill_dir, "scripts"),
        os.path.join(skill_dir, "references"),
        os.path.join(skill_dir, "assets"),
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✅ 创建目录: {d}")
    
    # 创建 SKILL.md
    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md_path, "w", encoding="utf-8") as f:
        f.write(SKILL_MD_TEMPLATE.format(
            skill_name=skill_name,
            description=description
        ))
    print(f"✅ 创建文件: {skill_md_path}")
    
    # 创建示例脚本
    script_path = os.path.join(skill_dir, "scripts", "example.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(SCRIPT_TEMPLATE.format(
            skill_name=skill_name,
            script_name="example"
        ))
    os.chmod(script_path, 0o755)
    print(f"✅ 创建文件: {script_path}")
    
    # 创建示例参考资料
    ref_path = os.path.join(skill_dir, "references", "README.md")
    with open(ref_path, "w", encoding="utf-8") as f:
        f.write(REFERENCE_TEMPLATE.format(skill_name=skill_name))
    print(f"✅ 创建文件: {ref_path}")
    
    # 创建 assets 占位文件
    assets_placeholder = os.path.join(skill_dir, "assets", ".gitkeep")
    with open(assets_placeholder, "w") as f:
        f.write("")
    print(f"✅ 创建文件: {assets_placeholder}")
    
    print(f"\n🎉 Skill '{skill_name}' 初始化完成！")
    print(f"📁 位置: {skill_dir}")
    print(f"\n下一步:")
    print(f"  1. 编辑 {skill_dir}/SKILL.md")
    print(f"  2. 实现 scripts/ 中的脚本")
    print(f"  3. 添加必要的 references/ 文档")
    print(f"  4. 放入 assets/ 资源文件")
    print(f"  5. 运行 package_skill.py 打包")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="初始化新的 Skill 目录结构"
    )
    parser.add_argument(
        "skill_name",
        help="Skill 名称（使用 kebab-case，如: pdf-processor）"
    )
    parser.add_argument(
        "--path",
        default=".",
        help="输出目录路径（默认: 当前目录）"
    )
    parser.add_argument(
        "--description",
        help="Skill 描述（用于 SKILL.md）"
    )
    
    args = parser.parse_args()
    
    # 验证 skill 名称
    if not args.skill_name.replace("-", "").replace("_", "").isalnum():
        print("❌ 错误: Skill 名称只能包含字母、数字、连字符(-)和下划线(_)")
        sys.exit(1)
    
    success = create_skill(args.skill_name, args.path, args.description)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
