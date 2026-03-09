#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 动态监控系统 v3.0 - 纯 HTTP 版
使用 requests + BeautifulSoup，无需浏览器
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ 请先安装: pip install requests beautifulsoup4")
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
    # 新增监控账号
    {"username": "steipete", "name": "Peter Steinberger", "type": "person", "priority": "medium"},
    {"username": "realDonaldTrump", "name": "特朗普", "type": "person", "priority": "high"},
    {"username": "elonmusk", "name": "马斯克", "type": "person", "priority": "high"},
]

DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_FILE = DATA_DIR / "processed_tweets.json"
ARTICLES_DIR = DATA_DIR / "articles"
DATA_DIR.mkdir(exist_ok=True)
ARTICLES_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
}

def load_processed():
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_processed(processed):
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

def fetch_nitter_rss(username):
    """使用 Nitter RSS 获取推文"""
    tweets = []
    
    # Nitter 镜像列表
    instances = [
        "https://nitter.net",
        "https://nitter.cz", 
        "https://nitter.privacydev.net",
        "https://nitter.unixfox.eu",
        "https://nitter.moomoo.me",
        "https://nitter.fdn.fr",
    ]
    
    for instance in instances:
        try:
            url = f"{instance}/{username}/rss"
            print(f"  🔍 尝试 {instance}...", end=" ", flush=True)
            
            resp = requests.get(url, headers=HEADERS, timeout=15)
            
            if resp.status_code != 200:
                print(f"HTTP {resp.status_code}")
                continue
            
            # 解析 RSS
            from xml.etree import ElementTree as ET
            
            try:
                root = ET.fromstring(resp.content)
            except:
                print("解析失败")
                continue
            
            # RSS 2.0 格式
            channel = root.find('.//channel')
            if channel is None:
                print("无内容")
                continue
            
            items = channel.findall('.//item')
            
            for item in items:
                try:
                    title = item.find('title')
                    text = title.text if title is not None else ""
                    
                    link = item.find('link')
                    tweet_url = link.text if link is not None else ""
                    
                    pub_date = item.find('pubDate')
                    created_at = pub_date.text if pub_date is not None else ""
                    
                    # 提取推文 ID
                    tweet_id = ""
                    if tweet_url:
                        parts = tweet_url.split('/')
                        if len(parts) > 0:
                            tweet_id = parts[-1]
                    
                    # 从 description 提取互动数据（如果有）
                    description = item.find('description')
                    desc_text = description.text if description is not None else ""
                    
                    tweets.append({
                        "tweet_id": tweet_id,
                        "text": text,
                        "username": username,
                        "author": username,
                        "created_at": created_at,
                        "likes": 0,  # RSS 通常不包含实时互动数据
                        "retweets": 0,
                        "tweet_url": tweet_url.replace('nitter.', 'x.com').replace('.net/', '/').replace('.cz/', '/').replace('x.comnet', 'x.com').replace('x.comprivacydev', 'x.com').replace('x.comunixfox', 'x.com').replace('.net', '')
                    })
                except:
                    continue
            
            if tweets:
                print(f"✅ 获取到 {len(tweets)} 条")
                return tweets
            else:
                print("无数据")
                
        except requests.exceptions.Timeout:
            print("超时")
            continue
        except Exception as e:
            print(f"错误: {str(e)[:30]}")
            continue
    
    return tweets

def fetch_via_html(username, limit=5):
    """备用方案：直接解析 HTML"""
    tweets = []
    
    instances = [
        "https://nitter.net",
        "https://nitter.cz",
        "https://nitter.privacydev.net",
    ]
    
    for instance in instances:
        try:
            url = f"{instance}/{username}"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            
            if resp.status_code != 200:
                continue
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 查找推文元素
            tweet_elements = soup.find_all('div', class_='timeline-item')[:limit]
            
            for elem in tweet_elements:
                try:
                    # 提取文本
                    text_elem = elem.find('div', class_='tweet-content')
                    if text_elem:
                        text_div = text_elem.find('div', class_='tweet-text')
                        text = text_div.get_text(strip=True) if text_div else ""
                    else:
                        continue
                    
                    # 提取时间
                    time_elem = elem.find('span', class_='tweet-date')
                    time_text = time_elem.get_text(strip=True) if time_elem else ""
                    
                    # 提取链接
                    link_elem = elem.find('a', class_='tweet-link')
                    if link_elem:
                        href = link_elem.get('href', '')
                        tweet_id = href.split('/')[-1] if href else ""
                    else:
                        tweet_id = ""
                    
                    tweets.append({
                        "tweet_id": tweet_id,
                        "text": text,
                        "username": username,
                        "author": username,
                        "created_at": time_text,
                        "likes": 0,
                        "retweets": 0,
                        "tweet_url": f"https://x.com/{username}/status/{tweet_id}"
                    })
                except:
                    continue
            
            if tweets:
                return tweets
                
        except:
            continue
    
    return tweets

def is_important(tweet, account):
    """判断是否重要"""
    text = tweet.get('text', '').lower()
    keywords = ['model', 'gpt', 'ai', 'release', 'launch', 'announce', 'paper', 
                'research', 'update', 'product', 'feature', 'api', 'claude', 'gemini',
                'agi', 'openai', 'new', 'introducing', 'available', 'today']
    has_keyword = any(kw in text for kw in keywords)
    return has_keyword

def analyze_importance(tweet, account):
    """分析重要性"""
    text = tweet.get('text', '')
    priority = account['priority']
    
    # 重磅关键词
    if any(kw in text.lower() for kw in ['gpt-5', 'agi', 'breaking', 'major', 'announce']):
        return "🔴 重磅"
    elif priority == 'high':
        return "🟠 重要"
    return "🟡 关注"

# 简单翻译映射表（常用科技词汇）
TRANSLATION_MAP = {
    # 常见AI术语
    "artificial intelligence": "人工智能",
    "machine learning": "机器学习",
    "deep learning": "深度学习",
    "neural network": "神经网络",
    "large language model": "大语言模型",
    "LLM": "大语言模型",
    "generative AI": "生成式 AI",
    "AGI": "通用人工智能",
    "AI agent": "AI 智能体",
    "fine-tuning": "微调",
    "prompt engineering": "提示工程",
    "multimodal": "多模态",
    "inference": "推理",
    "training": "训练",
    "open source": "开源",
    "released": "发布",
    "announced": "宣布",
    "launched": "推出",
    "available": "可用",
    "beta": "测试版",
    "API": "API",
    "model": "模型",
    "update": "更新",
    "feature": "功能",
    # 通用词汇
    "excited": "令人兴奋",
    "today": "今天",
    "tomorrow": "明天",
    "yesterday": "昨天",
    "just": "刚刚",
    "new": "新",
    "great": "很棒",
    "amazing": "令人惊叹",
    "looking forward": "期待",
    "thank": "感谢",
    "congratulations": "祝贺",
}

def translate_text(text):
    """简单翻译 - 将英文文本翻译成中文（保留原文）"""
    # 这是一个简化版本，实际可以接入翻译API
    # 这里先做一个简单的术语替换 + 保留原文
    translated = text
    for en, zh in TRANSLATION_MAP.items():
        # 不区分大小写替换
        import re
        translated = re.sub(r'\b' + re.escape(en) + r'\b', zh, translated, flags=re.IGNORECASE)
    return translated

def generate_article(tweet, account, importance):
    """生成深度解读文章"""
    title = f"【{importance}】{account['name']}最新动态：{tweet['text'][:50]}..."
    
    # 简单翻译（实际可以接入 DeepL / Google Translate API）
    translated_text = translate_text(tweet['text'])
    
    article = f"""# {title}

> **来源**: [{account['name']}]({tweet['tweet_url']})  
> **发布时间**: {tweet['created_at']}  
> **监控账号**: @{account['username']}  
> **重要性**: {importance}

---

## 📝 原文与翻译

### 原文 (Original)
{tweet['text']}

### 中文翻译 (Translation)
{translated_text}

---

## 🔍 深度解读

### 1. 背景与重要性

{account['name']} 作为{'AI领域的顶尖专家' if account['type'] == 'person' else 'AI行业的领先公司'}，
此次动态具有以下看点：

- **发布方影响力**: {'其观点往往代表着行业前沿方向，对 AI 从业者具有重要参考价值' if account['type'] == 'person' else '其产品和技术影响着全球数亿用户，每次更新都备受关注'}
- **时机因素**: 在当前 AI 竞争白热化的背景下，这一动态可能预示着新的技术趋势或战略方向

### 2. 核心内容分析

从推文内容来看，主要涉及以下关键点：

"""
    
    # 分析推文要点
    sentences = [s.strip() for s in tweet['text'].split('.') if len(s.strip()) > 10]
    for i, sent in enumerate(sentences[:5], 1):
        article += f"{i}. {sent}\n"
    
    article += f"""
### 3. 对行业的影响

这一动态可能产生以下影响：

- **技术层面**: 可能推动相关技术方向的快速发展
- **竞争格局**: 可能改变当前 AI 领域的竞争态势
- **应用落地**: 可能加速 AI 技术在更多场景的应用
- **市场反应**: 可能引起资本市场的关注和反应

---

## 💡 我们的观点

对于关注 AI 发展的读者，建议：

1. **持续关注** {account['name']} 的后续动态
2. **思考影响** 这一发展对自己工作或学习的潜在影响
3. **保持理性** 在信息爆炸时代，学会甄别真正有价值的信息
4. **实践验证** 如有条件，亲自体验相关技术或产品

---

## 📎 原文链接

🔗 [点击查看原文]({tweet['tweet_url']})

---

*本文由 公众号管家 AI 监控系统自动生成*  
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*  
*监控账号: {len(ACCOUNTS)} 个 | 检测间隔: 30分钟*
"""
    
    return {
        "title": title,
        "content": article,
        "importance": importance,
        "account": account['username'],
        "name": account['name'],
        "tweet_url": tweet['tweet_url'],
        "tweet_text": tweet['text'],
        "tweet_translated": translated_text,
        "created_at": datetime.now().isoformat()
    }

import subprocess

def git_sync():
    """自动同步到 GitHub"""
    try:
        print("\n" + "-" * 70)
        print("🔄 正在同步到 GitHub...")
        
        # 获取脚本所在目录的父目录（即知识库根目录）
        knowledge_dir = Path(__file__).parent.parent.parent.parent.parent
        
        # 检查是否在 git 仓库中
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=knowledge_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("  ⚠️ 当前目录不是 Git 仓库")
            return False
        
        # 添加所有更改
        subprocess.run(
            ["git", "add", "-A"],
            cwd=knowledge_dir,
            capture_output=True
        )
        
        # 检查是否有更改要提交
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=knowledge_dir,
            capture_output=True
        )
        
        if result.returncode == 0:
            print("  ℹ️ 没有新的更改需要提交")
            return True
        
        # 提交更改
        commit_msg = f"auto: AI监控更新 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n- 新增监控数据\n- 更新文章列表"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=knowledge_dir,
            capture_output=True
        )
        
        # 推送到远程
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=knowledge_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  ✅ 成功同步到 GitHub")
            return True
        else:
            print(f"  ⚠️ 推送失败: {result.stderr[:100]}")
            return False
            
    except Exception as e:
        print(f"  ❌ Git 同步出错: {e}")
        return False

def generate_summary_document(articles, all_tweets_count):
    """生成汇总文档，将所有监控对象的重要内容统一梳理成一篇文件"""
    now = datetime.now()
    filename = now.strftime('%Y-%m-%d-%H-%M') + '-重磅汇总.md'
    filepath = ARTICLES_DIR / filename
    
    # 按重要性排序
    importance_order = {"🔴 重磅": 0, "🟠 重要": 1, "🟡 关注": 2, "🟢 参考": 3}
    sorted_articles = sorted(articles, key=lambda x: importance_order.get(x['importance'], 4))
    
    # 生成分级统计
    counts = {"🔴 重磅": 0, "🟠 重要": 0, "🟡 关注": 0, "🟢 参考": 0}
    for article in articles:
        if article['importance'] in counts:
            counts[article['importance']] += 1
    
    content = f"""# AI 动态监控日报 - {now.strftime('%Y年%m月%d日 %H:%M')}

> 📊 本次监控时间: {now.strftime('%Y-%m-%d %H:%M')}
> 📈 监控账号: {len(ACCOUNTS)} 个 | 扫描推文: {all_tweets_count} 条
> 🎯 重要动态: {len(articles)} 条 | 🔴{counts['🔴 重磅']} 🟠{counts['🟠 重要']} 🟡{counts['🟡 关注']} 🟢{counts['🟢 参考']}

---

## 📋 今日要点速览

"""
    
    # 重磅内容摘要
    if counts["🔴 重磅"] > 0:
        content += "### 🔴 重磅\n\n"
        for article in sorted_articles:
            if article['importance'] == "🔴 重磅":
                content += f"- **{article['name']}** (@{article['account']}): {article['tweet_text'][:80]}...\n"
                content += f"  👉 [查看原文]({article['tweet_url']})\n\n"
    
    # 重要内容摘要
    if counts["🟠 重要"] > 0:
        content += "### 🟠 重要\n\n"
        for article in sorted_articles:
            if article['importance'] == "🟠 重要":
                content += f"- **{article['name']}** (@{article['account']}): {article['tweet_text'][:80]}...\n"
                content += f"  👉 [查看原文]({article['tweet_url']})\n\n"
    
    # 关注和参考
    if counts["🟡 关注"] > 0 or counts["🟢 参考"] > 0:
        content += "### 🟡 其他动态\n\n"
        for article in sorted_articles:
            if article['importance'] in ["🟡 关注", "🟢 参考"]:
                content += f"- **{article['name']}** (@{article['account']}): {article['tweet_text'][:60]}...\n\n"
    
    content += """---

## 📰 详细内容与解读

"""
    
    # 详细内容 - 包含原文和翻译
    for i, article in enumerate(sorted_articles, 1):
        content += f"""### {i}. {article['importance']} {article['name']} (@{article['account']})

> **原文链接**: [{article['tweet_url']}]({article['tweet_url']})

**📜 原文 (Original)**:
{article['tweet_text']}

**🌐 中文翻译**:
{article['tweet_translated']}

---

"""
    
    content += f"""## 📊 监控账号列表

| 账号 | 名称 | 类型 | 优先级 |
|------|------|------|--------|
| @sama | Sam Altman | 个人 | 🔴 高 |
| @OpenAI | OpenAI | 公司 | 🔴 高 |
| @GoogleAI | Google AI | 公司 | 🔴 高 |
| @AnthropicAI | Anthropic | 公司 | 🔴 高 |
| @AIatMeta | Meta AI | 公司 | 🟠 中 |
| @MicrosoftAI | Microsoft AI | 公司 | 🟠 中 |
| @karpathy | Andrej Karpathy | 个人 | 🔴 高 |
| @ylecun | Yann LeCun | 个人 | 🔴 高 |
| @demishassabis | Demis Hassabis | 个人 | 🟠 中 |
| @drfeifei | 李飞飞 | 个人 | 🟠 中 |
| @steipete | Peter Steinberger | 个人 | 🟠 中 |
| @realDonaldTrump | 特朗普 | 个人 | 🔴 高 |
| @elonmusk | 马斯克 | 个人 | 🔴 高 |

---

*本文由 公众号管家 AI 监控系统自动生成*  
*文件名: {filename}*  
*生成时间: {now.strftime('%Y-%m-%d %H:%M')}*
"""
    
    # 保存汇总文档
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📄 汇总文档已生成: {filepath.name}")
    return filepath.name

def main():
    print("=" * 70)
    print("🤖 AI 动态监控系统 v3.2 - 重磅汇总版")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 监控账号: {len(ACCOUNTS)} 个 (含新增: 特朗普、马斯克、Peter Steinberger)")
    print("=" * 70)
    
    processed = load_processed()
    new_articles = []
    all_tweets_count = 0
    
    print(f"📊 监控账号: {len(ACCOUNTS)} 个")
    print("-" * 70)
    
    for account in ACCOUNTS:
        print(f"\n🔍 检查 @{account['username']} ({account['name']})...")
        
        try:
            # 先尝试 RSS
            tweets = fetch_nitter_rss(account['username'])
            
            # 如果 RSS 失败，尝试 HTML
            if not tweets:
                print("  🔄 尝试 HTML 解析...", end=" ")
                tweets = fetch_via_html(account['username'])
                if tweets:
                    print(f"✅ 获取到 {len(tweets)} 条")
            
            if not tweets:
                print("  ⚠️ 未能获取推文")
                continue
            
            all_tweets_count += len(tweets)
            print(f"\n  📋 找到 {len(tweets)} 条推文:")
            
            for i, tweet in enumerate(tweets[:3], 1):  # 只处理前3条
                print(f"\n  {i}. [{tweet['created_at'][:20]}...]")
                print(f"     {tweet['text'][:100]}...")
                
                # 检查是否已处理
                if tweet['tweet_id'] in processed:
                    print(f"     ⏭️ 已处理过")
                    continue
                
                # 检查是否重要
                if is_important(tweet, account):
                    importance = analyze_importance(tweet, account)
                    print(f"     ✅ {importance} 重要内容！")
                    
                    # 生成文章内容
                    article = generate_article(tweet, account, importance)
                    
                    # 只生成汇总文档，不再单独保存每篇文章
                    new_articles.append(article)
                    
                    processed[tweet['tweet_id']] = {
                        'time': datetime.now().isoformat(),
                        'account': account['username'],
                        'important': True,
                        'title': article['title']
                    }
                else:
                    processed[tweet['tweet_id']] = {
                        'time': datetime.now().isoformat(),
                        'account': account['username'],
                        'important': False
                    }
            
            save_processed(processed)
            time.sleep(2)  # 避免请求过快
            
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            continue
    
    print("\n" + "=" * 70)
    print(f"🎯 本次发现 {len(new_articles)} 条重要动态")
    print(f"📊 共扫描 {all_tweets_count} 条推文")
    
    if new_articles:
        # 先生成汇总文档
        summary_file = generate_summary_document(new_articles, all_tweets_count)
        
        print("\n📢 飞书推送内容:")
        print("-" * 70)
        for article in new_articles:
            print(f"\n{article['importance']} 【AI动态监控】")
            print(f"📰 {article['name']} (@{article['account']})")
            print(f"📝 原文: {article['tweet_text'][:100]}...")
            print(f"🌐 翻译: {article['tweet_translated'][:100]}...")
            print(f"🔗 {article['tweet_url']}")
        print(f"\n📄 所有内容已汇总至: {summary_file}")
    
    print("\n" + "=" * 70)
    print("✅ 监控完成")
    print(f"📁 文章保存位置: {ARTICLES_DIR}")
    print(f"📝 已处理推文总数: {len(processed)}")
    
    # 自动同步到 GitHub
    git_sync()
    
    print("=" * 70)

if __name__ == "__main__":
    main()
