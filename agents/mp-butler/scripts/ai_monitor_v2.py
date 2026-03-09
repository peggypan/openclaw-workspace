#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 动态监控系统 v2.0 - Playwright 版
使用 Playwright 直接获取 X/Twitter 数据
"""

import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ 请先安装 Playwright: pip install playwright && playwright install chromium")
    exit(1)

# 监控账号
ACCOUNTS = [
    {"username": "sama", "name": "Sam Altman", "type": "person", "priority": "high"},
    {"username": "OpenAI", "name": "OpenAI", "type": "company", "priority": "high"},
    {"username": "GoogleAI", "name": "Google AI", "type": "company", "priority": "high"},
    {"username": "AnthropicAI", "name": "Anthropic", "type": "company", "priority": "high"},
    {"username": "AIatMeta", "name": "Meta AI", "type": "company", "priority": "medium"},
    {"username": "MicrosoftAI", "name": "Microsoft AI", "type": "company", "priority": "medium"},
    {"username": "karpathy", "name": "Andrej Karpathy", "type": "person", "priority": "high"},
    {"username": "ylecun", "name": "Yann LeCun", "type": "person", "priority": "high"},
    {"username": "demishassabis", "name": "Demis Hassabis", "type": "person", "priority": "medium"},
    {"username": "drfeifei", "name": "李飞飞", "type": "person", "priority": "medium"},
]

DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_FILE = DATA_DIR / "processed_tweets.json"
ARTICLES_DIR = DATA_DIR / "articles"
DATA_DIR.mkdir(exist_ok=True)
ARTICLES_DIR.mkdir(exist_ok=True)

def load_processed():
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_processed(processed):
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

def fetch_with_playwright(username, limit=5):
    """使用 Playwright 获取用户最新推文"""
    tweets = []
    
    # Nitter 镜像站点
    nitter_instances = [
        "https://nitter.net",
        "https://nitter.cz",
        "https://nitter.privacydev.net",
        "https://nitter.unixfox.eu",
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()
        
        for instance in nitter_instances:
            try:
                url = f"{instance}/{username}"
                print(f"  🔍 尝试 {instance}...", end=" ")
                
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                page.wait_for_timeout(3000)  # 等待 JS 渲染
                
                # 获取推文
                tweet_elements = page.query_selector_all(".timeline-item")[:limit]
                
                for elem in tweet_elements:
                    try:
                        text_elem = elem.query_selector(".tweet-content .tweet-text")
                        text = text_elem.inner_text() if text_elem else ""
                        
                        time_elem = elem.query_selector(".tweet-date a")
                        time_text = time_elem.inner_text() if time_elem else ""
                        
                        link_elem = elem.query_selector(".tweet-link")
                        tweet_url = link_elem.get_attribute("href") if link_elem else ""
                        tweet_id = tweet_url.split("/")[-1] if tweet_url else ""
                        
                        # 获取互动数据
                        stats_elem = elem.query_selector(".tweet-stats")
                        stats_text = stats_elem.inner_text() if stats_elem else ""
                        
                        likes = re.search(r'(\d+)\s*like', stats_text, re.I)
                        likes = int(likes.group(1)) if likes else 0
                        
                        retweets = re.search(r'(\d+)\s*retweet', stats_text, re.I)
                        retweets = int(retweets.group(1)) if retweets else 0
                        
                        tweets.append({
                            "tweet_id": tweet_id,
                            "text": text.strip(),
                            "username": username,
                            "author": username,
                            "created_at": time_text,
                            "likes": likes,
                            "retweets": retweets,
                            "tweet_url": f"https://x.com/{username}/status/{tweet_id}"
                        })
                    except:
                        continue
                
                if tweets:
                    print(f"✅ 获取到 {len(tweets)} 条")
                    break
                else:
                    print("❌ 无数据")
                    
            except Exception as e:
                print(f"❌ 失败")
                continue
        
        browser.close()
    
    return tweets

def is_important(tweet, account):
    """判断是否重要"""
    text = tweet.get('text', '').lower()
    keywords = ['model', 'gpt', 'ai', 'release', 'launch', 'announce', 'paper', 
                'research', 'update', 'product', 'feature', 'api', 'claude', 'gemini']
    has_keyword = any(kw in text for kw in keywords)
    likes = tweet.get('likes', 0)
    min_likes = 1000 if account['priority'] == 'high' else 500
    return (has_keyword or account['priority'] == 'high') and likes >= min_likes

def analyze_importance(tweet, account):
    """分析重要性"""
    likes = tweet.get('likes', 0)
    if account['priority'] == 'high' and likes > 10000:
        return "🔴 重磅"
    elif likes > 5000:
        return "🟠 重要"
    elif likes > 1000:
        return "🟡 关注"
    return "🟢 参考"

def generate_article(tweet, account, importance):
    """生成文章"""
    title = f"【{importance}】{account['name']}：{tweet['text'][:50]}..."
    
    article = f"""# {title}

> **来源**: [{account['name']}]({tweet['tweet_url']})  
> **时间**: {tweet['created_at']}  
> **互动**: ❤️ {tweet.get('likes', 0):,} | 🔄 {tweet.get('retweets', 0):,}

---

## 📌 核心内容

{tweet['text']}

---

## 🔍 深度解读

### 1. 背景分析

{account['name']} 作为{'AI领域的顶尖专家' if account['type'] == 'person' else 'AI行业的领先公司'}，
此次发布/观点值得关注：

- **发布方影响力**: {'其观点往往代表着行业前沿方向' if account['type'] == 'person' else '其产品和技术影响着全球数亿用户'}
- **时机背景**: 当前 AI 竞争白热化，这一动态可能预示新的技术趋势

### 2. 核心要点

{tweet['text'][:200]}...

### 3. 行业影响

- **技术层面**: 可能推动相关方向快速发展
- **竞争格局**: 可能改变当前 AI 领域态势
- **应用落地**: 可能加速 AI 在更多场景的应用

---

💡 建议持续关注 {account['name']} 的后续动态

---

📎 [查看原文]({tweet['tweet_url']})

---

*本文由 公众号管家 AI 监控系统自动生成*  
*监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    return {
        "title": title,
        "content": article,
        "importance": importance,
        "account": account['username'],
        "tweet_url": tweet['tweet_url'],
        "created_at": datetime.now().isoformat()
    }

def main():
    print("=" * 70)
    print("🤖 AI 动态监控系统 v2.0")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    processed = load_processed()
    new_articles = []
    
    print(f"📊 监控账号: {len(ACCOUNTS)} 个")
    print("-" * 70)
    
    # 先测试一个账号
    test_account = ACCOUNTS[0]  # Sam Altman
    print(f"\n🔍 测试检查 @{test_account['username']}...")
    
    try:
        tweets = fetch_with_playwright(test_account['username'], limit=5)
        
        if tweets:
            print(f"\n📋 获取到的推文:")
            for i, tweet in enumerate(tweets, 1):
                print(f"\n{i}. [{tweet['created_at']}] {tweet['text'][:80]}...")
                print(f"   ❤️ {tweet['likes']} | 🔄 {tweet['retweets']}")
        else:
            print("  ⚠️ 未能获取推文")
            
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")

if __name__ == "__main__":
    main()
