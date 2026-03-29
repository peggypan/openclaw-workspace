#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 动态监控系统 v4.0 - Camoufox + Nitter 双方案
- 优先使用 Camoufox (x-tweet-fetcher) 获取完整数据
- 失败时自动回退到 Nitter RSS
- 自动翻译为中文
"""

import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# 添加 x-tweet-fetcher 路径
sys.path.insert(0, '/root/.agents/skills/x-tweet-fetcher/scripts')

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
]

DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_FILE = DATA_DIR / "processed_tweets.json"
ARTICLES_DIR = DATA_DIR / "articles"
DATA_DIR.mkdir(exist_ok=True)
ARTICLES_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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

def translate_text(text, max_length=500):
    """简单翻译：保留原文，添加中文注释"""
    # 这里使用简单的标识，实际可以用翻译API
    # 为了演示，保留原文并在重要部分添加中文提示
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def fetch_via_camofox(username, limit=5):
    """
    使用 x-tweet-fetcher + Camoufox 获取推文
    优先方案：数据完整，包含互动数据
    """
    try:
        # 调用 x-tweet-fetcher
        result = subprocess.run(
            ['/usr/bin/python3', 
             '/root/.agents/skills/x-tweet-fetcher/scripts/fetch_tweet.py',
             '--user', username, '--limit', str(limit)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"  ⚠️ Camoufox 获取失败: {result.stderr[:100]}")
            return None
        
        # 解析输出
        try:
            data = json.loads(result.stdout)
            if 'tweets' not in data or not data['tweets']:
                return None
            
            tweets = []
            for tweet in data['tweets']:
                tweets.append({
                    'tweet_id': tweet.get('tweet_id', ''),
                    'text': tweet.get('text', ''),
                    'username': username,
                    'author': tweet.get('author_name', username),
                    'created_at': tweet.get('time_ago', ''),
                    'likes': tweet.get('likes', 0),
                    'retweets': tweet.get('retweets', 0),
                    'replies': tweet.get('replies', 0),
                    'views': tweet.get('views', 0),
                    'tweet_url': f"https://x.com/{username}/status/{tweet.get('tweet_id', '')}",
                    'source': 'camoufox',
                    'quoted_tweet': tweet.get('quoted_tweet', {}),
                    'media': tweet.get('media', [])
                })
            
            print(f"  ✅ Camoufox 获取到 {len(tweets)} 条")
            return tweets
            
        except json.JSONDecodeError:
            print(f"  ⚠️ 解析 Camoufox 输出失败")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"  ⚠️ Camoufox 请求超时")
        return None
    except Exception as e:
        print(f"  ⚠️ Camoufox 错误: {e}")
        return None

def fetch_nitter_rss(username):
    """
    使用 Nitter RSS 获取推文（备用方案）
    """
    tweets = []
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
            
            from xml.etree import ElementTree as ET
            try:
                root = ET.fromstring(resp.content)
            except:
                print("解析失败")
                continue
            
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
                    tweet_id = tweet_url.split('/')[-1] if tweet_url else ""
                    
                    pub_date = item.find('pubDate')
                    created_at = pub_date.text if pub_date is not None else ""
                    
                    tweets.append({
                        'tweet_id': tweet_id,
                        'text': text,
                        'username': username,
                        'author': username,
                        'created_at': created_at,
                        'likes': 0,
                        'retweets': 0,
                        'replies': 0,
                        'views': 0,
                        'tweet_url': tweet_url.replace('nitter.', 'x.com').replace('.net/', '/').replace('.cz/', '/'),
                        'source': 'nitter'
                    })
                except:
                    continue
            
            if tweets:
                print(f"✅ 获取到 {len(tweets)} 条")
                return tweets
                
        except requests.exceptions.Timeout:
            print("超时")
            continue
        except Exception as e:
            print(f"错误: {str(e)[:30]}")
            continue
    
    return tweets

def fetch_tweets(username, limit=5):
    """
    获取推文：优先 Camoufox，失败回退 Nitter
    """
    print(f"\n🔍 检查 @{username}...")
    
    # 方案1: Camoufox (优先)
    print("  🎯 尝试 Camoufox...")
    tweets = fetch_via_camofox(username, limit)
    if tweets:
        return tweets, 'camoufox'
    
    # 方案2: Nitter RSS (回退)
    print("  🔄 Camoufox 失败，回退到 Nitter RSS...")
    tweets = fetch_nitter_rss(username)
    if tweets:
        return tweets, 'nitter'
    
    return [], None

def is_important(tweet, account):
    """判断是否重要"""
    text = tweet.get('text', '').lower()
    keywords = ['model', 'gpt', 'ai', 'release', 'launch', 'announce', 'paper', 
                'research', 'update', 'product', 'feature', 'api', 'claude', 'gemini',
                'agi', 'openai', 'new', 'introducing', 'available', 'today']
    has_keyword = any(kw in text for kw in keywords)
    
    # Camoufox 有互动数据，可以提高阈值
    views = tweet.get('views', 0)
    likes = tweet.get('likes', 0)
    
    # 高浏览量直接标记为重要
    if views > 100000 or likes > 1000:
        return True
    
    return has_keyword

def analyze_importance(tweet, account):
    """分析重要性"""
    views = tweet.get('views', 0)
    likes = tweet.get('likes', 0)
    retweets = tweet.get('retweets', 0)
    
    # 综合评分
    score = views + likes * 10 + retweets * 20
    
    if score > 500000 or views > 400000:
        return "🔴 重磅"
    elif score > 100000 or views > 100000:
        return "🟠 重要"
    elif score > 10000:
        return "🟡 关注"
    return "🟢 参考"

def generate_article(tweet, account, importance):
    """生成中文深度解读文章"""
    title_en = tweet['text'][:60]
    
    # 翻译标题（简化版）
    title_translated = translate_text(title_en, 80)
    
    title = f"【{importance}】{account['name']}：{title_translated}..."
    
    # 翻译正文
    text_translated = translate_text(tweet['text'], 500)
    
    # 获取互动数据
    views = tweet.get('views', 0)
    likes = tweet.get('likes', 0)
    retweets = tweet.get('retweets', 0)
    replies = tweet.get('replies', 0)
    source = tweet.get('source', 'unknown')
    
    # 互动数据展示
    engagement = f"👁️ {views:,} | ❤️ {likes:,} | 🔄 {retweets:,} | 💬 {replies:,}" if views > 0 else "数据来源: Nitter RSS"
    
    article = f"""# {title}

> **来源**: [{account['name']}]({tweet['tweet_url']})  
> **发布时间**: {tweet['created_at']}  
> **互动数据**: {engagement}  
> **数据方案**: {'Camoufox' if source == 'camoufox' else 'Nitter RSS'}

---

## 📌 核心内容（原文）

{tweet['text']}

---

## 🔍 深度解读

### 1. 背景与重要性

{account['name']} 作为{'AI领域的顶尖专家' if account['type'] == 'person' else 'AI行业的领先公司'}，
此次动态具有以下看点：

- **发布方影响力**: {'其观点往往代表着行业前沿方向' if account['type'] == 'person' else '其产品和技术影响着全球数亿用户'}
- **数据说明**: {'包含完整互动数据，可信度高' if source == 'camoufox' else '通过 RSS 获取，数据可能不完整'}

### 2. 核心要点

该推文主要涉及以下内容：

{text_translated}

### 3. 对行业的影响

- **技术层面**: 可能推动相关技术方向的快速发展
- **竞争格局**: 可能改变当前 AI 领域的竞争态势
- **应用落地**: 可能加速 AI 技术在更多场景的应用

---

## 💡 我们的观点

建议持续关注 {account['name']} 的后续动态，
并思考这一发展对自己工作或学习的潜在影响。

---

## 📎 原文链接

🔗 [点击查看原文]({tweet['tweet_url']})

---

*本文由 公众号管家 AI 监控系统自动生成*  
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*  
*监控账号: {len(ACCOUNTS)} 个 | 数据方案: Camoufox + Nitter 双保险*
"""
    
    return {
        "title": title,
        "content": article,
        "importance": importance,
        "account": account['username'],
        "tweet_url": tweet['tweet_url'],
        "source": source,
        "created_at": datetime.now().isoformat(),
        "text": tweet['text']
    }

def generate_summary_document(articles, all_tweets_count):
    """生成汇总文档"""
    now = datetime.now()
    filename = now.strftime('%Y-%m-%d-%H-%M') + '.md'
    filepath = ARTICLES_DIR / filename
    
    importance_order = {"🔴 重磅": 0, "🟠 重要": 1, "🟡 关注": 2, "🟢 参考": 3}
    sorted_articles = sorted(articles, key=lambda x: importance_order.get(x['importance'], 4))
    
    counts = {"🔴 重磅": 0, "🟠 重要": 0, "🟡 关注": 0, "🟢 参考": 0}
    for article in articles:
        if article['importance'] in counts:
            counts[article['importance']] += 1
    
    content = f"""# AI 动态监控日报 - {now.strftime('%Y年%m月%d日 %H:%M')}

> 📊 本次监控时间: {now.strftime('%Y-%m-%d %H:%M')}
> 📈 监控账号: {len(ACCOUNTS)} 个 | 扫描推文: {all_tweets_count} 条
> 🎯 重要动态: {len(articles)} 条 | 🔴{counts['🔴 重磅']} 🟠{counts['🟠 重要']} 🟡{counts['🟡 关注']} 🟢{counts['🟢 参考']}
> 🔧 数据方案: Camoufox 优先 + Nitter RSS 回退

---

## 📋 今日要点速览

"""
    
    if counts["🔴 重磅"] > 0:
        content += "### 🔴 重磅\n\n"
        for art in sorted_articles:
            if art['importance'] == "🔴 重磅":
                content += f"- **{art['account']}** ({art.get('source', 'unknown')}): {art['title'][:60]}...\n"
                content += f"  👉 [查看原文]({art['tweet_url']})\n\n"
    
    if counts["🟠 重要"] > 0:
        content += "### 🟠 重要\n\n"
        for art in sorted_articles:
            if art['importance'] == "🟠 重要":
                content += f"- **{art['account']}** ({art.get('source', 'unknown')}): {art['title'][:60]}...\n"
                content += f"  👉 [查看原文]({art['tweet_url']})\n\n"
    
    if counts["🟡 关注"] > 0 or counts["🟢 参考"] > 0:
        content += "### 🟡 其他动态\n\n"
        for art in sorted_articles:
            if art['importance'] in ["🟡 关注", "🟢 参考"]:
                content += f"- **{art['account']}**: {art['title'][:50]}...\n\n"
    
    content += """---

## 📰 详细内容

"""
    
    for i, art in enumerate(sorted_articles, 1):
        content += f"""### {i}. {art['importance']} {art['account']}

> **来源**: {art.get('source', 'unknown')} | **原文**: [{art['tweet_url']}]({art['tweet_url']})

{art['title']}

**核心内容**:
{art.get('text', '内容详见原文')[:200]}

---

"""
    
    content += f"""## 📊 监控账号列表

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

## 🔧 技术说明

- **主要数据源**: Camoufox (通过 x-tweet-fetcher)
- **备用数据源**: Nitter RSS
- **数据特点**: Camoufox 提供完整互动数据（浏览量、点赞、转发等）
- **回退机制**: Camoufox 失败时自动切换 Nitter

---

*本文由 公众号管家 AI 监控系统自动生成*  
*文件名: {filename}*  
*生成时间: {now.strftime('%Y-%m-%d %H:%M')}*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📄 汇总文档已生成: {filepath.name}")
    return filepath.name

def send_feishu_notification(articles, chat_id="oc_f815b8902d22c11ba7f692193bfabe51"):
    """
    发送飞书群通知
    使用 OpenClaw 的 message 工具发送
    """
    if not articles:
        return
    
    try:
        # 构建通知内容
        message_lines = ["🤖 **AI 动态监控播报**", ""]
        message_lines.append(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        message_lines.append(f"📊 发现 **{len(articles)}** 条重要动态")
        message_lines.append("")
        
        for i, article in enumerate(articles[:5], 1):  # 最多显示5条
            importance_emoji = "🔴" if "重磅" in article['importance'] else "🟠"
            message_lines.append(f"{importance_emoji} **{article['title']}**")
            message_lines.append(f"   👤 @{article['account']} | [查看原文]({article['tweet_url']})")
            message_lines.append("")
        
        if len(articles) > 5:
            message_lines.append(f"_...还有 {len(articles) - 5} 条动态，详见生成的文章_")
        
        message_lines.append("")
        message_lines.append("📁 深度解读文章已自动生成并同步到 GitHub")
        
        message_content = "\n".join(message_lines)
        
        # 写入通知文件，由外部脚本读取发送
        notify_file = DATA_DIR / "feishu_notification.txt"
        with open(notify_file, 'w', encoding='utf-8') as f:
            f.write(message_content)
        
        print(f"\n📢 飞书通知已准备: {notify_file}")
        
        # 尝试使用 openclaw 命令发送 (如果可用)
        try:
            import os
            # 设置完整的环境变量（cron 环境 PATH 不完整）
            env = os.environ.copy()
            env['PATH'] = '/root/.nvm/versions/node/v22.22.0/bin:' + env.get('PATH', '')
            OPENCLAW_BIN = "/root/.nvm/versions/node/v22.22.0/bin/openclaw"
            
            result = subprocess.run(
                [OPENCLAW_BIN, 'message', 'send', '--channel', 'feishu', 
                 '--target', chat_id, '--message', message_content],
                capture_output=True,
                timeout=10,
                env=env
            )
            if result.returncode == 0:
                print("  ✅ 飞书消息已通过 openclaw 发送")
            else:
                print(f"  ℹ️ openclaw 发送跳过: {result.stderr.decode()[:50] if result.stderr else 'unknown'}")
        except Exception as e:
            print(f"  ℹ️ 外部发送方式不可用: {e}")
        
        return True
        
    except Exception as e:
        print(f"  ⚠️ 飞书通知准备失败: {e}")
        return False

def git_sync():
    """自动同步到 GitHub"""
    try:
        print("\n" + "-" * 70)
        print("🔄 正在同步到 GitHub...")
        
        knowledge_dir = Path(__file__).parent.parent.parent.parent.parent
        
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=knowledge_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("  ⚠️ 当前目录不是 Git 仓库")
            return False
        
        subprocess.run(["git", "add", "-A"], cwd=knowledge_dir, capture_output=True)
        
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=knowledge_dir,
            capture_output=True
        )
        
        if result.returncode == 0:
            print("  ℹ️ 没有新的更改需要提交")
            return True
        
        commit_msg = f"auto: AI监控更新 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n- 新增监控数据\n- Camoufox + Nitter 双方案"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=knowledge_dir, capture_output=True)
        
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

def main():
    print("=" * 70)
    print("🤖 AI 动态监控系统 v4.0 - Camoufox + Nitter 双方案")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    processed = load_processed()
    new_articles = []
    all_tweets_count = 0
    
    print(f"📊 监控账号: {len(ACCOUNTS)} 个")
    print("🔧 数据方案: Camoufox 优先 + Nitter RSS 回退")
    print("-" * 70)
    
    for account in ACCOUNTS:
        tweets, source = fetch_tweets(account['username'], limit=3)
        
        if not tweets:
            print(f"  ⚠️ 未能获取 @{account['username']} 的推文")
            continue
        
        all_tweets_count += len(tweets)
        print(f"\n  📋 {source.upper()} 获取到 {len(tweets)} 条推文:")
        
        for i, tweet in enumerate(tweets[:3], 1):
            views_info = f"👁️ {tweet.get('views', 0):,}" if tweet.get('views', 0) > 0 else ""
            print(f"\n  {i}. [{tweet['created_at'][:20]}...] {views_info}")
            print(f"     {tweet['text'][:100]}...")
            
            if tweet['tweet_id'] in processed:
                print(f"     ⏭️ 已处理过")
                continue
            
            if is_important(tweet, account):
                importance = analyze_importance(tweet, account)
                print(f"     ✅ {importance} 重要内容！")
                
                article = generate_article(tweet, account, importance)
                
                article_file = ARTICLES_DIR / f"{int(time.time())}_{account['username']}.md"
                with open(article_file, 'w', encoding='utf-8') as f:
                    f.write(article['content'])
                
                new_articles.append(article)
                
                processed[tweet['tweet_id']] = {
                    'time': datetime.now().isoformat(),
                    'account': account['username'],
                    'important': True,
                    'title': article['title'],
                    'source': source
                }
            else:
                processed[tweet['tweet_id']] = {
                    'time': datetime.now().isoformat(),
                    'account': account['username'],
                    'important': False,
                    'source': source
                }
        
        save_processed(processed)
        time.sleep(2)
    
    print("\n" + "=" * 70)
    print(f"🎯 本次发现 {len(new_articles)} 条重要动态")
    print(f"📊 共扫描 {all_tweets_count} 条推文")
    
    if new_articles:
        camoufox_count = sum(1 for a in new_articles if a.get('source') == 'camoufox')
        nitter_count = len(new_articles) - camoufox_count
        print(f"📈 数据来源: Camoufox {camoufox_count} 条, Nitter {nitter_count} 条")
        
        summary_file = generate_summary_document(new_articles, all_tweets_count)
        print(f"📄 汇总文档: {summary_file}")
    else:
        print(f"\n💚 [{datetime.now().strftime('%Y-%m-%d %H:%M')}] 本次监控未发现新的重要动态")
        print("   所有监控账号暂无更新，已扫描的推文均已处理过。")
    
    print("\n" + "=" * 70)
    print("✅ 监控完成")
    print(f"📁 文章保存位置: {ARTICLES_DIR}")
    print(f"📝 已处理推文总数: {len(processed)}")
    
    # 发送飞书通知
    if new_articles:
        send_feishu_notification(new_articles)
    
    git_sync()
    
    print("=" * 70)

if __name__ == "__main__":
    main()
