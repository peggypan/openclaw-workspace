#!/usr/bin/env python3
"""
今日综合早报生成器
每天早上7:30自动发送科技/AI早报

Topics:
1. 🦄 硅谷热点 (Hacker News)
2. 🐙 开源趋势 (GitHub Trending)  
7. 📈 华尔街见闻 (WallStreetCN)
9. 🤗 HF 每日论文 (Hugging Face)
10. 🧪 Latent Space AINews
"""

import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
import sys

def get_hacker_news():
    """获取 Hacker News Top Stories"""
    try:
        # 获取 top stories IDs
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
        # 获取最近一周创建的、star 数超过100的仓库，按 star 排序
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
        return [{'name': f'获取失败: {str(e)}', 'description': '请检查网络连接', 'stars': 0, 'url': '#', 'language': 'N/A'}]

def generate_report():
    """生成早报"""
    now = datetime.now()
    date_str = now.strftime('%Y年%m月%d日')
    weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]
    
    report = []
    report.append(f"# 📰 今日综合早报 - {date_str} {weekday}")
    report.append("")
    report.append("---")
    report.append("")
    
    # 1. Hacker News
    report.append("## 🦄 硅谷热点 (Hacker News)")
    report.append("")
    hn_stories = get_hacker_news()
    for i, story in enumerate(hn_stories, 1):
        report.append(f"{i}. [{story['title']}]({story['url']})")
        report.append(f"   👍 {story['score']} pts | 💬 {story['comments']} comments")
        report.append("")
    
    # 2. GitHub Trending
    report.append("## 🐙 开源趋势 (GitHub Trending)")
    report.append("")
    gh_repos = get_github_trending()
    for i, repo in enumerate(gh_repos, 1):
        desc = repo['description'][:100] + '...' if len(repo['description']) > 100 else repo['description']
        report.append(f"{i}. [{repo['name']}]({repo['url']})")
        report.append(f"   ⭐ {repo['stars']} | 📝 {repo['language']} | {desc}")
        report.append("")
    
    # 9. Hugging Face Papers
    report.append("## 🤗 HF 每日论文 (Hugging Face)")
    report.append("")
    report.append("📄 [查看今日最新论文](https://huggingface.co/papers)")
    report.append("")
    
    # 10. Latent Space
    report.append("## 🧪 Latent Space AI News")
    report.append("")
    report.append("📰 [查看最新AI分析](https://www.latent.space/)")
    report.append("")
    
    # Footer
    report.append("---")
    report.append("")
    report.append(f"🤖 由 AI 助手自动生成于 {now.strftime('%H:%M')}")
    report.append("📌 每日7:30准时推送")
    
    return "\n".join(report)

if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # 保存到文件（可选）
    # with open(f"/tmp/morning_report_{datetime.now().strftime('%Y%m%d')}.md", "w") as f:
    #     f.write(report)