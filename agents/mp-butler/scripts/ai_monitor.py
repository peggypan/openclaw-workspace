#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 动态监控核心脚本
- 获取 X 时间线
- 内容过滤与重要性评级
- 生成深度解读文章
- 推送飞书消息
"""

import json
import os
import sys
import yaml
import time
from datetime import datetime, timedelta
from pathlib import Path

# 添加脚本路径
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from fetch_tweet import fetch_timeline

# 配置路径（脚本在 scripts/ 目录，配置在父目录的 config/）
CONFIG_PATH = Path(__file__).parent.parent / "config" / "monitor_config.yaml"
DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_FILE = DATA_DIR / "processed_tweets.json"
ARTICLES_DIR = DATA_DIR / "articles"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
ARTICLES_DIR.mkdir(exist_ok=True)

def load_config():
    """加载监控配置"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_processed_tweets():
    """加载已处理的推文ID"""
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_processed_tweets(processed):
    """保存已处理的推文ID"""
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

def is_content_important(tweet, account_config):
    """
    判断内容是否重要
    - 检查关键词匹配
    - 检查互动数据
    - 检查内容长度
    """
    text = tweet.get('text', '').lower()
    keywords = account_config.get('keywords', [])
    min_likes = account_config.get('min_likes', 500)
    
    # 排除低质量关键词
    exclude_keywords = ["thanks", "congratulations", "happy", "birthday"]
    if any(kw in text for kw in exclude_keywords):
        return False, "excluded_keywords"
    
    # 检查互动数据
    likes = tweet.get('likes', 0)
    if likes < min_likes:
        return False, f"low_engagement ({likes} < {min_likes})"
    
    # 检查关键词匹配
    keyword_match = any(kw.lower() in text for kw in keywords)
    
    # 特殊账号（高优先级）放宽关键词限制
    priority = account_config.get('priority', 'medium')
    if priority == 'high' and likes >= min_likes * 2:
        return True, "high_priority_high_engagement"
    
    if keyword_match:
        return True, "keyword_match"
    
    return False, "no_keyword_match"

def analyze_importance_level(tweet, account_config):
    """分析内容重要性等级"""
    likes = tweet.get('likes', 0)
    retweets = tweet.get('retweets', 0)
    views = tweet.get('views', 0)
    priority = account_config.get('priority', 'medium')
    
    # 计算综合热度分数
    score = likes + retweets * 2 + (views / 1000)
    
    if priority == 'high' and score > 10000:
        return "🔴 重磅"
    elif score > 5000 or (priority == 'high' and score > 3000):
        return "🟠 重要"
    elif score > 1000:
        return "🟡 关注"
    else:
        return "🟢 参考"

def generate_article(tweet, account_info, importance_level):
    """
    生成深度解读文章
    """
    text = tweet.get('text', '')
    author = tweet.get('author', account_info['username'])
    created_at = tweet.get('created_at', '')
    likes = tweet.get('likes', 0)
    retweets = tweet.get('retweets', 0)
    views = tweet.get('views', 0)
    tweet_url = f"https://x.com/{account_info['username']}/status/{tweet.get('tweet_id', '')}"
    
    # 生成文章标题
    title_templates = {
        "🔴 重磅": [
            f"【重磅】{author} 发布重大更新：{text[:30]}...",
            f"AI圈地震！{author} 刚刚宣布{text[:25]}...",
            f"必看！{author} 深夜发文：{text[:30]}..."
        ],
        "🟠 重要": [
            f"【深度】{author} 最新观点：{text[:30]}...",
            f"{author} 谈 AI 发展：{text[:30]}...",
            f"值得关注！{author} 分享{text[:25]}..."
        ],
        "🟡 关注": [
            f"{author} 最新动态：{text[:30]}...",
            f"AI 前沿观察：{author} 谈{text[:25]}..."
        ],
        "🟢 参考": [
            f"{author}：{text[:35]}..."
        ]
    }
    
    import random
    title = random.choice(title_templates.get(importance_level, title_templates["🟢 参考"]))
    
    # 生成正文
    article = f"""# {title}

> **来源**: [{author}]({tweet_url})  
> **时间**: {created_at}  
> **互动数据**: ❤️ {likes:,} | 🔄 {retweets:,} | 👁️ {views:,}

---

## 📌 核心事件

{text}

---

## 🔍 深度解读

### 1. 背景与重要性

{account_info['username']} 作为{'AI领域的领先公司' if account_info['type'] == 'company' else 'AI领域的顶尖专家'}，此次动态具有以下看点：

- **发布方背景**: {'该公司一直在推动大语言模型和通用人工智能的发展，其产品影响着全球数亿用户。' if account_info['type'] == 'company' else '该专家在深度学习、神经网络等领域有着深厚的造诣，其观点往往代表着行业前沿。'}
- **时机因素**: 在当前 AI 竞争白热化的背景下，这一动态可能预示着新的技术趋势或战略方向。

### 2. 核心内容分析

从推文内容来看，主要涉及以下关键点：

{chr(10).join(['- ' + line for line in text.split('.') if len(line.strip()) > 10][:5])}

### 3. 对行业的影响

这一动态可能产生以下影响：

- **技术层面**: 可能推动相关技术方向的快速发展
- **竞争格局**: 可能改变当前 AI 领域的竞争态势
- **应用落地**: 可能加速 AI 技术在更多场景的应用

---

## 💡 我们的观点

对于关注 AI 发展的读者，建议：

1. **持续关注** {account_info['username']} 的后续动态
2. **思考影响** 这一发展对自己工作或学习的潜在影响
3. **保持理性** 在信息爆炸时代，学会甄别真正有价值的信息

---

## 📎 原文链接

🔗 [点击查看原文]({tweet_url})

---

*本文由 公众号管家 AI 监控系统自动生成*  
*生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    
    return {
        "title": title,
        "content": article,
        "importance": importance_level,
        "account": account_info['username'],
        "tweet_url": tweet_url,
        "created_at": datetime.now().isoformat()
    }

def check_account(account, processed_tweets):
    """检查单个账号的最新推文"""
    username = account['username']
    print(f"🔍 正在检查: @{username}...")
    
    try:
        # 获取最近 10 条推文
        result = fetch_timeline(username, limit=10)
        
        if not result or 'tweets' not in result:
            print(f"  ⚠️ 未能获取 @{username} 的时间线")
            return []
        
        new_important_tweets = []
        
        for tweet in result['tweets']:
            tweet_id = tweet.get('tweet_id')
            
            # 检查是否已处理
            if tweet_id in processed_tweets:
                continue
            
            # 检查内容重要性
            is_important, reason = is_content_important(tweet, account)
            
            if is_important:
                importance = analyze_importance_level(tweet, account)
                new_important_tweets.append({
                    'tweet': tweet,
                    'account': account,
                    'importance': importance,
                    'reason': reason
                })
                print(f"  ✅ 发现重要推文: {importance} - {reason}")
            else:
                print(f"  ⏭️ 跳过: {reason}")
            
            # 记录为已处理
            processed_tweets[tweet_id] = {
                'processed_at': datetime.now().isoformat(),
                'username': username,
                'is_important': is_important
            }
        
        return new_important_tweets
        
    except Exception as e:
        print(f"  ❌ 检查 @{username} 时出错: {e}")
        return []

def format_feishu_message(article):
    """格式化飞书消息"""
    importance = article['importance']
    title = article['title']
    account = article['account']
    url = article['tweet_url']
    
    return f"""{importance} 【AI动态监控】

📰 {title}

👤 来源: @{account}
🔗 {url}

💡 深度解读文章已生成，请查看文档...

---
⏰ 监控时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}"""

def main():
    """主函数"""
    print("=" * 60)
    print("🤖 AI 动态监控系统启动")
    print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    accounts = config['accounts']
    
    # 加载已处理记录
    processed_tweets = load_processed_tweets()
    initial_count = len(processed_tweets)
    
    print(f"📊 监控账号数: {len(accounts)}")
    print(f"📊 已处理推文: {initial_count}")
    print("-" * 60)
    
    # 检查所有账号
    all_new_tweets = []
    for account in accounts:
        new_tweets = check_account(account, processed_tweets)
        all_new_tweets.extend(new_tweets)
        time.sleep(2)  # 避免请求过快
    
    print("-" * 60)
    print(f"🎯 共发现 {len(all_new_tweets)} 条重要动态")
    
    # 生成文章并保存
    articles_generated = []
    for item in all_new_tweets:
        article = generate_article(
            item['tweet'],
            item['account'],
            item['importance']
        )
        
        # 保存文章
        article_file = ARTICLES_DIR / f"{int(time.time())}_{item['account']['username']}.md"
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(article['content'])
        
        articles_generated.append({
            'article': article,
            'file': str(article_file)
        })
        
        print(f"📝 已生成文章: {article_file.name}")
    
    # 保存处理记录
    save_processed_tweets(processed_tweets)
    
    # 输出飞书消息格式
    if articles_generated:
        print("\n" + "=" * 60)
        print("📢 飞书推送内容:")
        print("=" * 60)
        for item in articles_generated:
            print(format_feishu_message(item['article']))
            print("-" * 40)
    
    print(f"\n✅ 监控完成，本次新增处理: {len(processed_tweets) - initial_count} 条推文")
    return articles_generated

if __name__ == "__main__":
    main()
