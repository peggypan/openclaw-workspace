#!/bin/bash
# 今日综合早报生成器
# 每天早上7:30自动发送

REPORT_FILE="/tmp/morning_report_$(date +%Y%m%d).md"
DATE_STR=$(date '+%Y年%m月%d日')

echo "# 📰 今日综合早报 - ${DATE_STR}" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 获取 Hacker News 热点
echo "## 🦄 硅谷热点 (Hacker News)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
curl -s "https://hacker-news.firebaseio.com/v0/topstories.json" | \
  python3 -c "
import sys, json
ids = json.load(sys.stdin)[:5]
for i, id in enumerate(ids, 1):
    import urllib.request
    url = f'https://hacker-news.firebaseio.com/v0/item/{id}.json'
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
        title = data.get('title', 'N/A')
        score = data.get('score', 0)
        link = data.get('url', f'https://news.ycombinator.com/item?id={id}')
        print(f'{i}. [{title}]({link}) ({score} pts)')
" 2>/dev/null >> "$REPORT_FILE" || echo "- 获取中..." >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 获取 GitHub Trending
echo "## 🐙 开源趋势 (GitHub Trending)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
curl -s "https://api.github.com/search/repositories?q=stars:>100+created:>$(date -d '7 days ago' +%Y-%m-%d)&sort=stars&order=desc&per_page=5" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
for i, repo in enumerate(data.get('items', [])[:5], 1):
    name = repo.get('full_name', 'N/A')
    desc = repo.get('description', 'No description') or 'No description'
    stars = repo.get('stargazers_count', 0)
    url = repo.get('html_url', '')
    print(f'{i}. [{name}]({url}) ⭐ {stars}')
    print(f'   {desc[:80]}...')
" 2>/dev/null >> "$REPORT_FILE" || echo "- 获取中..." >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Hugging Face 论文
echo "## 🤗 HF 每日论文 (Hugging Face)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "访问: https://huggingface.co/papers" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Latent Space AINews
echo "## 🧪 Latent Space AI News" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "访问: https://www.latent.space/" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "---" >> "$REPORT_FILE"
echo "🤖 由你的 AI 助手自动生成" >> "$REPORT_FILE"

cat "$REPORT_FILE"