#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汇总现有文章为一个文档
"""

import os
import re
from datetime import datetime
from pathlib import Path

ARTICLES_DIR = Path("/root/.openclaw/workspace/knowledge/公众号-想象X/agents/公众号管家/data/articles")

# 获取所有文章文件（排除demo文件）
article_files = sorted([f for f in ARTICLES_DIR.glob("*.md") if not f.name.startswith("demo")])

print(f"找到 {len(article_files)} 篇文章需要汇总")

# 读取所有文章内容
articles_data = []
for file in article_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取信息
    # 标题通常是第一行
    lines = content.split('\n')
    title = lines[0].replace('# ', '') if lines else file.name
    
    # 提取重要性
    importance = "🟡 关注"
    if "🔴 重磅" in title or "🔴 重磅" in content:
        importance = "🔴 重磅"
    elif "🟠 重要" in title or "🟠 重要" in content:
        importance = "🟠 重要"
    
    # 提取账号
    account = file.name.replace('.md', '').split('_')[-1]
    
    # 提取原文链接
    url_match = re.search(r'https://x\.com/[^\s\)]+', content)
    url = url_match.group(0) if url_match else ""
    
    articles_data.append({
        'file': file.name,
        'title': title,
        'importance': importance,
        'account': account,
        'content': content,
        'url': url
    })

# 按重要性排序
importance_order = {"🔴 重磅": 0, "🟠 重要": 1, "🟡 关注": 2, "🟢 参考": 3}
articles_data.sort(key=lambda x: importance_order.get(x['importance'], 4))

# 统计
counts = {"🔴 重磅": 0, "🟠 重要": 0, "🟡 关注": 0}
for art in articles_data:
    if art['importance'] in counts:
        counts[art['importance']] += 1

# 生成汇总文档
now = datetime.now()
filename = now.strftime('%Y-%m-%d-%H-%M') + '.md'
filepath = ARTICLES_DIR / filename

summary = f"""# AI 动态监控日报 - {now.strftime('%Y年%m月%d日 %H:%M')}

> 📊 本次整理时间: {now.strftime('%Y-%m-%d %H:%M')}
> 📈 整理文章数: {len(articles_data)} 篇
> 🎯 重要动态: 🔴{counts['🔴 重磅']} 🟠{counts['🟠 重要']} 🟡{counts['🟡 关注']}

---

## 📋 今日要点速览

"""

# 重磅内容
if counts["🔴 重磅"] > 0:
    summary += "### 🔴 重磅\n\n"
    for art in articles_data:
        if art['importance'] == "🔴 重磅":
            clean_title = art['title'].replace('【🔴 重磅】', '').replace('【🟠 重要】', '').replace('【🟡 关注】', '')
            summary += f"- **{art['account']}**: {clean_title[:60]}...\n"
            summary += f"  👉 [查看原文]({art['url']})\n\n"

# 重要内容
if counts["🟠 重要"] > 0:
    summary += "### 🟠 重要\n\n"
    for art in articles_data:
        if art['importance'] == "🟠 重要":
            clean_title = art['title'].replace('【🔴 重磅】', '').replace('【🟠 重要】', '').replace('【🟡 关注】', '')
            summary += f"- **{art['account']}**: {clean_title[:60]}...\n"
            summary += f"  👉 [查看原文]({art['url']})\n\n"

# 关注内容
if counts["🟡 关注"] > 0:
    summary += "### 🟡 关注\n\n"
    for art in articles_data:
        if art['importance'] == "🟡 关注":
            clean_title = art['title'].replace('【🔴 重磅】', '').replace('【🟠 重要】', '').replace('【🟡 关注】', '')
            summary += f"- **{art['account']}**: {clean_title[:50]}...\n\n"

summary += """---

## 📰 详细内容

"""

# 详细内容
for i, art in enumerate(articles_data, 1):
    summary += f"""### {i}. {art['importance']} {art['account']}

> **原文**: [{art['url']}]({art['url']})

{art['content'].split('## 📌 核心内容')[1].split('---')[0] if '## 📌 核心内容' in art['content'] else art['content'][:500]}

---

"""

summary += f"""## 📊 监控账号列表

| 账号 | 类型 | 说明 |
|------|------|------|
| @sama | 个人 | Sam Altman (OpenAI CEO) |
| @OpenAI | 公司 | OpenAI 官方 |
| @GoogleAI | 公司 | Google AI |
| @AnthropicAI | 公司 | Anthropic |
| @AIatMeta | 公司 | Meta AI |
| @MicrosoftAI | 公司 | Microsoft AI |
| @karpathy | 个人 | Andrej Karpathy |
| @ylecun | 个人 | Yann LeCun |
| @demishassabis | 个人 | Demis Hassabis |
| @drfeifei | 个人 | 李飞飞 |

---

*本文由 公众号管家 AI 监控系统整理生成*  
*文件名: {filename}*  
*整理时间: {now.strftime('%Y-%m-%d %H:%M')}*
"""

# 保存汇总文档
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(summary)

print(f"✅ 汇总文档已生成: {filepath.name}")
print(f"📄 包含 {len(articles_data)} 篇文章")

# 删除单个文件
print("\n🗑️ 删除单个文章文件...")
for art in articles_data:
    file_path = ARTICLES_DIR / art['file']
    if file_path.exists():
        file_path.unlink()
        print(f"  已删除: {art['file']}")

# 删除demo文件
demo_files = list(ARTICLES_DIR.glob("demo_*.md"))
for demo in demo_files:
    demo.unlink()
    print(f"  已删除: {demo.name}")

print(f"\n✅ 清理完成！")
print(f"📁 只保留汇总文档: {filepath.name}")
