# HEARTBEAT.md - AI 动态监控系统

## 定时任务配置

### 主监控任务 - 每小时执行
执行命令: 
```bash
cd /root/.openclaw/workspace/knowledge/公众号-想象X/agents/公众号管家 && python3 scripts/ai_monitor_v4.py && python3 scripts/push_notification.py
```

任务列表:
- [x] 运行 AI 动态监控脚本 (v4.2 X + YouTube 双平台)
- [x] 优先使用 Camoufox 获取完整数据
- [x] Camoufox 失败时自动回退到 Nitter RSS
- [x] 监控 YouTube 播客频道更新
- [x] 生成中文深度解读文章
- [x] 自动同步到 GitHub
- [x] **自动推送报告到飞书** (新增)

## 监控账号 (35个)

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

### 其他监控
11. @steipete - Peter Steinberger / OpenClaw 开发者 (中优先级)
12. @realDonaldTrump - 特朗普 (高优先级)
13. @elonmusk - 马斯克 (高优先级)

### AI 视频/短剧
14. @runwayml - Runway - AI视频生成领导者 (高优先级)
15. @pika_labs - Pika Labs - AI视频生成 (中优先级)
16. @HeyGen_Official - HeyGen - AI数字人/视频 (中优先级)
17. @LumaLabsAI - Luma AI - AI 3D/视频生成 (中优先级)
18. @hedra_ai - Hedra - AI角色视频生成 (中优先级)
19. @StableVideo - Stable Video - Stability AI视频 (中优先级)
20. @Kling_AI - 可灵 AI - 快手AI视频 (高优先级)
21. @HailuoAI - 海螺 AI - MiniMax AI视频 (中优先级)

### AI Builders (新增 22个 - 2026-03-22)
22. @swyx - Swyx / Latent Space 创始人 (高优先级)
23. @joshwoodward - Josh Woodward / Google Labs (高优先级)
24. @kevinweil - Kevin Weil / OpenAI产品负责人 (高优先级)
25. @petergyang - Peter Yang (中优先级)
26. @amjadmasad - Amjad Masad / Replit CEO (高优先级)
27. @rauchg - Guillermo Rauch / Vercel CEO (高优先级)
28. @alexalbert__ - Alex Albert / Anthropic (中优先级)
29. @levie - Aaron Levie / Box CEO (高优先级)
30. @garrytan - Garry Tan / YC总裁 (高优先级)
31. @mattturck - Matt Turck / Data Driven NYC (中优先级)
32. @zara__zhang - Zara Zhang (中优先级)
33. @nikunj - Nikunj Kothari (中优先级)
34. @danshipper - Dan Shipper / Every (高优先级)
35. @adityaag - Aditya Agarwal (中优先级)
36. @AmandaAskell - Amanda Askell / Anthropic哲学家 (高优先级)
37. @GoogleLabs - Google Labs 官方 (高优先级)

### AI Builders (补充 6个 - 2026-03-22)
38. @thenanyu - Nan Yu (中优先级)
39. @realmadhuguru - Madhu Guru (中优先级)
40. @_catwu - Cat Wu (中优先级)
41. @trq212 - Thariq (中优先级)
42. @ryolu_ - Ryo Lu (中优先级)
43. @claudeai - Claude 官方账号 (高优先级)

### YouTube 播客监控 (新增 5个 - 2026-03-22)
44. Latent Space - @LatentSpacePod (高优先级)
45. No Priors - @NoPriorsPodcast (高优先级)
46. Unsupervised Learning - @RedpointAI (中优先级)
47. Data Driven NYC - @DataDrivenNYC (中优先级)
48. Training Data - Playlist (中优先级)

## 系统状态
- 状态: ✅ 运行中
- 版本: v4.2 (X + YouTube 双平台版)
- 检测间隔: 30分钟
- 文章保存: data/articles/ (汇总成单文件)
- GitHub 同步: ✅ 自动
- 中文输出: ✅ 已启用
- YouTube监控: ✅ 已启用
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
*上次更新: 2026-03-22*
