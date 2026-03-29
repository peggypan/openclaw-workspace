# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## 🗞️ News Aggregator Skill

**Location**: `skills/news-aggregator-skill/`
**Source**: https://github.com/cclank/news-aggregator-skill

### 魔法咒语
召唤交互菜单：**如意如意**

### 支持的28个信息源
- 🦄 Hacker News (`hackernews`)
- 🐙 GitHub Trending (`github`)
- 📈 华尔街见闻 (`wallstreetcn`)
- 🤗 Hugging Face Papers (`huggingface`)
- 🧪 Latent Space (`latentspace`)
- 🚀 36氪 (`36kr`)
- 🔴 微博热搜 (`weibo`)
- 更多...

### 使用示例
```bash
# 获取单个源
python3 scripts/fetch_news.py --source hackernews --limit 5

# 获取多个源
python3 scripts/fetch_news.py --source hackernews,github,wallstreetcn --limit 5

# 深度抓取（使用 Playwright 绕过防爬）
python3 scripts/fetch_news.py --source hackernews --deep --limit 3

# 生成场景化早报
python3 scripts/daily_briefing.py --profile tech
```

### 早报定时任务
- **时间**: 每天 07:35
- **脚本**: `scripts/send_morning_report_v2.py`
- **日志**: `/tmp/morning_report.log`
