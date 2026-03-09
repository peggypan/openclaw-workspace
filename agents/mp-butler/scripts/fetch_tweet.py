#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取用户时间线
使用 FxTwitter API (无需 Camofox)
"""

import requests
import json
import sys
import re
from pathlib import Path

def fetch_timeline(username, limit=20):
    """
    获取用户时间线
    
    Args:
        username: X 用户名（不带 @）
        limit: 获取推文数量（最大约 50）
    
    Returns:
        dict: 包含推文列表的结果
    """
    return fetch_via_fxtwitter(username, limit)

def fetch_via_fxtwitter(username, limit=20):
    """
    使用 FxTwitter API 获取用户信息和最近推文
    """
    try:
        # 首先获取用户信息
        user_url = f"https://api.fxtwitter.com/{username}"
        user_resp = requests.get(user_url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
        })
        
        if user_resp.status_code != 200:
            print(f"⚠️ 获取用户信息失败: {user_resp.status_code}")
            return {'tweets': []}
        
        user_data = user_resp.json()
        
        # FxTwitter 现在可能需要不同的端点来获取时间线
        # 尝试使用搜索端点
        tweets = []
        
        # 尝试多种方法获取推文
        # 方法1: 直接获取用户最近推文（如果有端点支持）
        timeline_url = f"https://api.fxtwitter.com/{username}/tweets"
        timeline_resp = requests.get(timeline_url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
        })
        
        if timeline_resp.status_code == 200:
            timeline_data = timeline_resp.json()
            if 'tweets' in timeline_data:
                for tweet in timeline_data['tweets'][:limit]:
                    tweets.append({
                        'tweet_id': tweet.get('id', ''),
                        'text': tweet.get('text', ''),
                        'author': tweet.get('author', {}).get('name', username),
                        'screen_name': username,
                        'created_at': tweet.get('created_at', ''),
                        'likes': tweet.get('likes', 0),
                        'retweets': tweet.get('retweets', 0),
                        'views': tweet.get('views', 0),
                        'replies_count': tweet.get('replies', 0),
                        'is_note_tweet': tweet.get('is_note_tweet', False),
                        'is_article': tweet.get('is_article', False)
                    })
        
        # 如果没有获取到推文，使用模拟数据用于测试
        if not tweets:
            print(f"  ℹ️ 无法获取 @{username} 的时间线，使用测试模式")
            # 返回空列表，让主脚本继续运行
            pass
        
        return {'tweets': tweets}
        
    except Exception as e:
        print(f"⚠️ 获取失败: {e}")
        return {'tweets': []}

def fetch_tweet(url):
    """
    获取单条推文详情（使用 FxTwitter）
    """
    try:
        # 转换 URL 为 FxTwitter API
        if '/status/' in url:
            tweet_id = url.split('/status/')[-1].split('?')[0]
            fx_url = f"https://api.fxtwitter.com/status/{tweet_id}"
            
            resp = requests.get(fx_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
            })
            
            if resp.status_code == 200:
                data = resp.json()
                tweet_data = data.get('tweet', {})
                
                return {
                    'tweet_id': tweet_id,
                    'text': tweet_data.get('text', ''),
                    'author': tweet_data.get('author', {}).get('name', ''),
                    'screen_name': tweet_data.get('author', {}).get('screen_name', ''),
                    'created_at': tweet_data.get('created_at', ''),
                    'likes': tweet_data.get('likes', 0),
                    'retweets': tweet_data.get('retweets', 0),
                    'views': tweet_data.get('views', 0),
                    'replies_count': tweet_data.get('replies', 0),
                    'is_note_tweet': tweet_data.get('is_note_tweet', False),
                    'is_article': False
                }
        
        return None
        
    except Exception as e:
        print(f"❌ 获取推文失败: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_tweet.py --user <username> [--limit 20]")
        print("       python fetch_tweet.py --url <tweet_url>")
        sys.exit(1)
    
    if sys.argv[1] == '--user':
        username = sys.argv[2]
        limit = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[3] == '--limit' else 20
        result = fetch_timeline(username, limit)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif sys.argv[1] == '--url':
        url = sys.argv[2]
        result = fetch_tweet(url)
        print(json.dumps(result, ensure_ascii=False, indent=2))
