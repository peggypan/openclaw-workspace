# Daily Morning Report Configuration
# 今日综合早报 - 每天早上7:30发送

## Schedule
- **Time**: 每天 07:30
- **Timezone**: Asia/Shanghai (GMT+8)

## Topics 信息源配置

### 1. 🦄 硅谷热点 (Hacker News)
- URL: https://news.ycombinator.com
- API: https://hacker-news.firebaseio.com/v0/
- Content: Top 5 stories

### 2. 🐙 开源趋势 (GitHub Trending)
- URL: https://github.com/trending
- API: https://api.github.com/
- Content: 本周最热门仓库

### 7. 📈 华尔街见闻 (WallStreetCN)
- URL: https://wallstreetcn.com
- Note: 财经新闻

### 9. 🤗 HF 每日论文 (Hugging Face)
- URL: https://huggingface.co/papers
- Content: 最新AI研究论文

### 10. 🧪 Latent Space AINews (swyx)
- URL: https://www.latent.space/
- Content: AI行业深度分析

## Output Format
- Markdown format
- Send to: Feishu group chat
- Include timestamp and source links