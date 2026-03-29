#!/usr/bin/env python3
"""
今日综合早报 - 飞书版
每天早上7:30自动发送科技/AI早报到飞书群

使用方式:
  python3 send_morning_report.py [--test]
"""

import json
import urllib.request
import urllib.error
import subprocess
import sys
import argparse
from datetime import datetime, timedelta

# 飞书群配置
FEISHU_CHAT_ID = "oc_a306ee2e3e16416c482f1264e093eae7"

def get_hacker_news():
    """获取 Hacker News Top Stories"""
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        with urllib.request.urlopen(url, timeout=10) as response:
            story_ids = json.loads(response.read())[:5]
        
        stories = []
        for story_id in story_ids:
            url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read())
                stories.append({
                    'title': data.get('title', 'N/A'),
                    'score': data.get('score', 0),
                    'url': data.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    'comments': data.get('descendants', 0)
                })
        return stories
    except Exception as e:
        return [{'title': f'获取失败: {str(e)}', 'score': 0, 'url': '#', 'comments': 0}]

def get_github_trending():
    """获取 GitHub Trending Repositories"""
    try:
        last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        url = f"https://api.github.com/search/repositories?q=stars:>100+created:>{last_week}&sort=stars&order=desc&per_page=5"
        headers = {'User-Agent': 'Morning-Report-Bot'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            repos = []
            for item in data.get('items', [])[:5]:
                repos.append({
                    'name': item.get('full_name', 'N/A'),
                    'description': item.get('description', 'No description') or 'No description',
                    'stars': item.get('stargazers_count', 0),
                    'url': item.get('html_url', ''),
                    'language': item.get('language', 'Unknown') or 'Unknown'
                })
            return repos
    except Exception as e:
        return [{'name': f'获取失败', 'description': str(e), 'stars': 0, 'url': '#', 'language': 'N/A'}]

def generate_report():
    """生成早报内容"""
    now = datetime.now()
    date_str = now.strftime('%Y年%m月%d日')
    weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]
    
    lines = []
    lines.append(f"📰 今日综合早报 - {date_str} {weekday}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 1. Hacker News
    lines.append("## 🦄 硅谷热点 (Hacker News)")
    lines.append("")
    hn_stories = get_hacker_news()
    for i, story in enumerate(hn_stories, 1):
        lines.append(f"{i}. **{story['title']}**")
        lines.append(f"   🔗 {story['url']}")
        lines.append(f"   👍 {story['score']} pts | 💬 {story['comments']} comments")
        lines.append("")
    
    # 2. GitHub Trending
    lines.append("## 🐙 开源趋势 (GitHub Trending)")
    lines.append("")
    gh_repos = get_github_trending()
    for i, repo in enumerate(gh_repos, 1):
        desc = repo['description'][:80] + '...' if len(repo['description']) > 80 else repo['description']
        lines.append(f"{i}. **{repo['name']}**")
        lines.append(f"   🔗 {repo['url']}")
        lines.append(f"   ⭐ {repo['stars']} | 📝 {repo['language']}")
        lines.append(f"   {desc}")
        lines.append("")
    
    # 9. Hugging Face Papers
    lines.append("## 🤗 HF 每日论文 (Hugging Face)")
    lines.append("")
    lines.append("📄 https://huggingface.co/papers")
    lines.append("")
    
    # 10. Latent Space
    lines.append("## 🧪 Latent Space AI News")
    lines.append("")
    lines.append("📰 https://www.latent.space/")
    lines.append("")
    
    # Footer
    lines.append("---")
    lines.append("")
    lines.append(f"🤖 由 AI 助手自动生成 | 📌 每日7:30推送")
    
    return "\n".join(lines)

def send_to_feishu(content, test_mode=False):
    """发送消息到飞书"""
    if test_mode:
        print("="*60)
        print("【测试模式】早报内容预览:")
        print("="*60)
        print(content)
        print("="*60)
        return True
    
    # 这里可以通过调用 message 工具或 API 发送到飞书
    # 实际发送由 OpenClaw 的 message 工具处理
    print(content)
    return True

def main():
    parser = argparse.ArgumentParser(description='今日综合早报生成器')
    parser.add_argument('--test', action='store_true', help='测试模式（只打印不发送）')
    args = parser.parse_args()
    
    # 生成早报
    report = generate_report()
    
    # 发送或打印
    send_to_feishu(report, test_mode=args.test)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())