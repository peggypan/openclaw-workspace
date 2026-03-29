# HEARTBEAT.md - 定时任务配置
# 每天早上7:30发送今日综合早报

## 早报任务
**Schedule**: cron(30 7 * * *)
**Timezone**: Asia/Shanghai

### 任务内容
运行早报生成脚本并发送到飞书群：

```bash
# 生成早报
python3 /root/.openclaw/workspace/agents/product-manager/scripts/daily_morning_report.py

# 发送早报到飞书（通过message工具）
```

### 信息源 Topics
1. 🦄 硅谷热点 (Hacker News) - Top 5 stories
2. 🐙 开源趋势 (GitHub Trending) - 本周热门仓库
9. 🤗 HF 每日论文 (Hugging Face) - AI论文链接
10. 🧪 Latent Space AINews - AI行业分析

### 早报示例
- 标题：📰 今日综合早报 - 2026年03月24日 周二
- 格式：Markdown
- 包含：标题、链接、评分/Stars、评论数

### 手动触发测试
如需立即测试早报，运行：
```bash
python3 /root/.openclaw/workspace/agents/product-manager/scripts/daily_morning_report.py
```