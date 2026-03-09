# HEARTBEAT.md - AI 动态监控系统

## 定时任务配置

### 主监控任务 - 每小时执行
执行命令: 
```bash
cd /root/.openclaw/workspace/knowledge/公众号-想象X/agents/公众号管家 && python3 scripts/ai_monitor_v4.py
```

任务列表:
- [x] 运行 AI 动态监控脚本 (v4.0 Camoufox + Nitter 双方案)
- [x] 优先使用 Camoufox 获取完整数据
- [x] Camoufox 失败时自动回退到 Nitter RSS
- [x] 生成中文深度解读文章
- [x] 自动同步到 GitHub

## 监控账号 (13个)

### AI 行业
1. @sama - Sam Altman (高优先级)
2. @OpenAI - OpenAI (高优先级)
3. @GoogleAI - Google AI (高优先级)
4. @AnthropicAI - Anthropic (高优先级)
5. @AIatMeta - Meta AI (中优先级)
6. @MicrosoftAI - Microsoft AI (中优先级)
7. @karpathy - Andrej Karpathy (高优先级)
8. @ylecun - Yann LeCun (高优先级)
9. @demishassabis - Demis Hassabis (中优先级)
10. @drfeifei - 李飞飞 (中优先级)

### 新增监控
11. @steipete - Peter Steinberger / OpenClaw 开发者 (中优先级)
12. @realDonaldTrump - 特朗普 (高优先级)
13. @elonmusk - 马斯克 (高优先级)

## 系统状态
- 状态: ✅ 运行中
- 版本: v4.1 (重磅汇总版)
- 检测间隔: 30分钟
- 文章保存: data/articles/ (汇总成单文件)
- GitHub 同步: ✅ 自动
- 中文输出: ✅ 已启用
- 新增功能:
  - ✅ 显示原文 + 中文翻译
  - ✅ 重磅内容合并成一篇汇总文件
  - ✅ 新增 3 个监控账号 (Peter Steinberger、特朗普、马斯克)

## GitHub 同步
- 仓库: peggypan/knowledge
- 分支: main
- 提交信息: auto: AI监控更新 [时间戳]
- 同步内容: 新生成的文章、processed_tweets.json

---
*上次更新: 2026-03-06*
