# HEARTBEAT.md - GitHub Trending Monitor

## 每日任务

### GitHub Trending 监测
- **频率:** 每天一次 (建议上午 10:00 左右)
- **任务:** 抓取 GitHub 每日 Trending 项目，分析 Star 增长最快的仓库
- **数据来源:** https://github.com/trending?since=daily
- **输出:** 
  - 保存到 `memory/github-trending-YYYY-MM-DD.md`
  - 发送摘要到本群聊

### 执行步骤
1. 使用 Camoufox 访问 https://github.com/trending?since=daily
2. 提取前 10 个项目的：名称、描述、总 stars、今日增长、语言
3. 对比历史数据分析趋势
4. 保存完整数据到 memory 文件
5. 发送今日 Top 5 摘要到群聊

---

**注意:** 如果 HEARTBEAT_OK 被触发，且距离上次检查已超过 20 小时，则执行上述任务。
