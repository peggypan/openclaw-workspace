# AI 动态监控系统 - 定时任务配置
# 每 30 分钟执行一次监控检查

## 任务列表

### 1. AI 动态监控主任务
- **执行频率**: 每 30 分钟
- **执行命令**: python3 scripts/ai_monitor.py
- **功能**: 检查 10 个 AI 账号的最新动态，生成深度解读文章

---

## 手动测试命令

```bash
# 测试单个账号
cd /root/.openclaw/workspace/knowledge/公众号-想象X/agents/公众号管家
python3 scripts/fetch_tweet.py --user OpenAI --limit 5

# 运行完整监控
python3 scripts/ai_monitor.py
```

---

## 监控账号列表（10个）

### 公司官方（5个）
1. @OpenAI - OpenAI 官方
2. @GoogleAI - Google AI 官方
3. @AnthropicAI - Anthropic 官方
4. @AIatMeta - Meta AI 官方
5. @MicrosoftAI - Microsoft AI 官方

### 技术领袖（5个）
6. @sama - Sam Altman (OpenAI CEO)
7. @karpathy - Andrej Karpathy
8. @ylecun - Yann LeCun (Meta 首席科学家)
9. @demishassabis - Demis Hassabis (DeepMind CEO)
10. @drfeifei - 李飞飞 (Stanford HAI)

---

## 注意事项

1. **Camofox 依赖**: 需要安装并运行 Camofox 浏览器插件
   ```bash
   openclaw plugins install @askjo/camofox-browser
   openclaw plugins start @askjo/camofox-browser
   ```

2. **Python 依赖**: 需要安装 pyyaml
   ```bash
   pip install pyyaml feedparser
   ```

3. **存储位置**: 
   - 已处理推文: data/processed_tweets.json
   - 生成文章: data/articles/

---

*最后更新: 2026-03-06*
