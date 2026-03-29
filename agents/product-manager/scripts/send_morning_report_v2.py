#!/usr/bin/env python3
"""
今日综合早报 - 使用 news-aggregator-skill
每天早上7:35自动发送科技/AI早报

使用方式:
  python3 send_morning_report_v2.py [--test]
"""

import json
import subprocess
import sys
import argparse
from datetime import datetime
import os

# 配置
SKILL_DIR = "/root/.openclaw/workspace/agents/product-manager/skills/news-aggregator-skill"
FEISHU_CHAT_ID = "oc_a306ee2e3e16416c482f1264e093eae7"

def fetch_news(sources, limit=5):
    """使用 news-aggregator-skill 获取新闻"""
    cmd = [
        "python3", f"{SKILL_DIR}/scripts/fetch_news.py",
        "--source", sources,
        "--limit", str(limit),
        "--no-save"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Error: {result.stderr}", file=sys.stderr)
            return []
    except Exception as e:
        print(f"Fetch error: {e}", file=sys.stderr)
        return []

def format_hackernews(items):
    """格式化 Hacker News"""
    lines = []
    lines.append("## 🦄 硅谷热点 (Hacker News)")
    lines.append("")
    
    for i, item in enumerate(items[:5], 1):
        title = item.get('title', 'N/A')
        url = item.get('url', '#')
        hn_url = item.get('hn_url', url)
        heat = item.get('heat', '0 points')
        time = item.get('time', 'Unknown')
        
        lines.append(f"{i}. **{title}**")
        lines.append(f"   🔗 [原文]({url}) | 💬 [讨论]({hn_url})")
        lines.append(f"   👍 {heat} | ⏰ {time}")
        lines.append("")
    
    return lines

def format_github(items):
    """格式化 GitHub Trending"""
    lines = []
    lines.append("## 🐙 开源趋势 (GitHub Trending)")
    lines.append("")
    
    for i, item in enumerate(items[:5], 1):
        title = item.get('title', 'N/A')
        url = item.get('url', '#')
        heat = item.get('heat', '0 stars')
        
        # 提取仓库名和描述
        parts = title.split(' - ', 1)
        repo_name = parts[0]
        desc = parts[1] if len(parts) > 1 else 'No description'
        
        lines.append(f"{i}. **{repo_name}**")
        lines.append(f"   🔗 {url}")
        lines.append(f"   ⭐ {heat} | {desc[:100]}")
        lines.append("")
    
    return lines

def format_wallstreetcn(items):
    """格式化 华尔街见闻"""
    lines = []
    lines.append("## 📈 华尔街见闻 (WallStreetCN)")
    lines.append("")
    
    for i, item in enumerate(items[:5], 1):
        title = item.get('title', 'N/A')
        url = item.get('url', '#')
        time = item.get('time', 'Unknown')
        
        lines.append(f"{i}. **{title}**")
        lines.append(f"   🔗 {url}")
        lines.append(f"   ⏰ {time}")
        lines.append("")
    
    return lines

def generate_report():
    """生成早报"""
    now = datetime.now()
    date_str = now.strftime('%Y年%m月%d日')
    weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]
    
    lines = []
    lines.append(f"📰 今日综合早报 - {date_str} {weekday}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 获取数据
    print("正在获取 Hacker News...", file=sys.stderr)
    hn_items = fetch_news("hackernews", limit=5)
    if hn_items:
        lines.extend(format_hackernews(hn_items))
    
    print("正在获取 GitHub Trending...", file=sys.stderr)
    gh_items = fetch_news("github", limit=5)
    if gh_items:
        lines.extend(format_github(gh_items))
    
    print("正在获取 华尔街见闻...", file=sys.stderr)
    ws_items = fetch_news("wallstreetcn", limit=5)
    if ws_items:
        lines.extend(format_wallstreetcn(ws_items))
    
    # 添加其他信息源链接
    lines.append("## 🤗 更多资讯")
    lines.append("")
    lines.append("- 📄 [Hugging Face 每日论文](https://huggingface.co/papers)")
    lines.append("- 🧪 [Latent Space AI News](https://www.latent.space/)")
    lines.append("")
    
    # Footer
    lines.append("---")
    lines.append("")
    lines.append(f"🤖 由 AI 助手自动生成 | 📌 每日7:35推送")
    lines.append("🪄 召唤菜单请说：**如意如意**")
    
    return "\n".join(lines)

def send_to_feishu(content):
    """发送早报到飞书"""
    try:
        # 设置完整的环境变量（cron 环境 PATH 不完整）
        env = os.environ.copy()
        env['PATH'] = '/root/.nvm/versions/node/v22.22.0/bin:' + env.get('PATH', '')
        OPENCLAW_BIN = "/root/.nvm/versions/node/v22.22.0/bin/openclaw"
        
        # 将内容写入临时文件
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file = f.name
        
        try:
            # 使用 openclaw 发送
            cmd = [
                OPENCLAW_BIN, 'message', 'send',
                '--channel', 'feishu',
                '--target', FEISHU_CHAT_ID,
                '-m', content
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                env=env
            )
            
            if result.returncode == 0:
                print("✅ 早报已成功推送到飞书", file=sys.stderr)
                return True
            else:
                print(f"❌ 飞书推送失败: {result.stderr}", file=sys.stderr)
                return False
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"❌ 发送异常: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='今日综合早报生成器 v2')
    parser.add_argument('--test', action='store_true', help='测试模式（只打印不发送）')
    args = parser.parse_args()
    
    # 生成早报
    report = generate_report()
    
    if args.test:
        print("="*60)
        print("【测试模式】早报内容预览:")
        print("="*60)
        print(report)
        print("="*60)
    else:
        print(report, file=sys.stderr)
        # 发送到飞书
        send_to_feishu(report)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())