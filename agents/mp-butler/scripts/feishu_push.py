#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书消息推送脚本
用于推送监控到的重要 AI 动态
"""

import json
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def push_to_feishu(article_data, chat_id=None):
    """
    推送文章到飞书
    
    Args:
        article_data: 包含 title, content, importance, account, tweet_url
        chat_id: 飞书聊天 ID（可选，默认使用当前会话）
    """
    importance = article_data['importance']
    title = article_data['title']
    account = article_data['account']
    url = article_data['tweet_url']
    
    # 构建消息
    message = f"""{importance} 【AI动态监控】

📰 {title}

👤 来源: @{account}
🔗 原文链接: {url}

💡 深度解读文章已生成，请查看下方文档或询问我获取完整内容。

---
🤖 公众号管家 AI 监控系统"""
    
    # 输出消息（OpenClaw 会自动发送到飞书）
    print(message)
    
    return True

def push_digest(articles, count=0):
    """
    推送摘要报告（当没有新内容或心跳时使用）
    """
    if not articles:
        print(f"""💚 【AI动态监控】30分钟扫描完成

本次扫描未发现重大 AI 动态。

监控账号: OpenAI, GoogleAI, AnthropicAI, MetaAI, MicrosoftAI, Sam Altman, Andrej Karpathy, Yann LeCun, Demis Hassabis, 李飞飞
监控间隔: 30分钟
内容风格: 深度解读型

---
🤖 公众号管家 AI 监控系统""")
        return
    
    # 生成摘要
    important_count = sum(1 for a in articles if '🔴' in a['importance'] or '🟠' in a['importance'])
    
    digest = f"""📊 【AI动态监控报告】

本次扫描发现 {len(articles)} 条重要动态：

"""
    for i, article in enumerate(articles[:5], 1):  # 最多显示5条
        digest += f"{i}. {article['importance']} {article['title'][:50]}...\n"
    
    if len(articles) > 5:
        digest += f"\n... 还有 {len(articles) - 5} 条动态，请查看详细报告\n"
    
    digest += f"""
---
🤖 公众号管家 AI 监控系统"""
    
    print(digest)

if __name__ == "__main__":
    # 测试推送
    test_article = {
        "title": "OpenAI 发布 GPT-5 预览版：多模态能力大幅提升",
        "importance": "🔴 重磅",
        "account": "OpenAI",
        "tweet_url": "https://x.com/OpenAI/status/123456"
    }
    push_to_feishu(test_article)
