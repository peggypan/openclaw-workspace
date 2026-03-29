# GitHub Trending Monitor Configuration

## ✅ 定时任务已配置

### 任务详情
| 配置项 | 值 |
|--------|-----|
| **任务名称** | github-trending-daily |
| **任务ID** | 6e4c480e-28c7-4df2-aa7f-c77839bbf7ce |
| **执行时间** | 每天北京时间 06:00 |
| **时区** | Asia/Shanghai (北京时间) |
| **状态** | 已启用 ✅ |

### 推送规则
1. **每日摘要** - 每天早上6:00自动推送 Top 10 项目摘要
2. **不限制语言** - 所有编程语言的项目都会监测
3. **详细报告触发条件** - 当某个项目 **单日增长 > 10,000 stars** 时，自动生成详细分析报告

### 推送内容格式
```
📊 GitHub Trending 日报 - YYYY-MM-DD

Top 5 热门项目：
1. [项目名] - ⭐ 今日增长 / 总 Stars
   [描述]

🔥 超热门项目（增长>1万）：
[详细分析报告]
```

### 管理命令
```bash
# 查看任务列表
openclaw cron list

# 立即运行一次（测试）
openclaw cron run github-trending-daily

# 查看运行历史
openclaw cron runs github-trending-daily

# 禁用/启用
openclaw cron disable github-trending-daily
openclaw cron enable github-trending-daily

# 删除任务
openclaw cron rm github-trending-daily
```

---

## 📁 历史数据存档
每日详细数据保存在：`memory/github-trending-YYYY-MM-DD.md`

## 📌 今日数据 (2026-03-18)
已保存至: [github-trending-2026-03-18.md](./github-trending-2026-03-18.md)
