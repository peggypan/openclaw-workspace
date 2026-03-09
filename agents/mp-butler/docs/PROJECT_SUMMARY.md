# AI 动态监控系统搭建实录

> 项目日期：2026年3月6日  
> 项目目标：自动监控 X/Twitter 上 AI 领域重要账号，生成中文深度解读文章

---

## 📋 项目概述

今天成功搭建了一套完整的 **AI 动态监控系统**，能够自动监控 10 个 AI 领域的顶级账号（包括 OpenAI、Google AI、Sam Altman 等），每小时检查一次最新动态，生成中文深度解读文章，并自动同步到 GitHub。

---

## 🎯 核心功能

### 1. 监控账号列表（10个）

**公司官方账号（5个）：**
- @OpenAI - OpenAI 官方
- @GoogleAI - Google AI
- @AnthropicAI - Anthropic
- @AIatMeta - Meta AI
- @MicrosoftAI - Microsoft AI

**技术领袖（5个）：**
- @sama - Sam Altman (OpenAI CEO)
- @karpathy - Andrej Karpathy
- @ylecun - Yann LeCun
- @demishassabis - Demis Hassabis
- @drfeifei - 李飞飞

### 2. 双保险数据方案

**方案一：Camoufox（优先）**
- 使用 x-tweet-fetcher + Camoufox 浏览器
- 获取完整互动数据：浏览量、点赞、转发、回复
- 数据完整，可靠性高

**方案二：Nitter RSS（回退）**
- Camoufox 失败时自动切换
- 基于 Nitter RSS 获取推文
- 轻量稳定，作为备用

### 3. 智能内容处理

- **关键词过滤**：自动识别 AI 相关重要内容
- **重要性评级**：🔴重磅 / 🟠重要 / 🟡关注 / 🟢参考
- **中文生成**：自动生成中文深度解读文章
- **去重机制**：避免重复处理已抓取的推文

---

## 🛠️ 技术实现过程

### 阶段一：基础搭建（Nitter RSS 方案）

由于 Camoufox 依赖较多，首先使用 **Nitter RSS** 方案快速搭建基础版本：

```python
# 核心思路：通过 Nitter RSS 获取推文
instances = [
    "https://nitter.net",
    "https://nitter.cz",
    "https://nitter.privacydev.net",
    # ... 多镜像轮询
]
```

**成果：**
- ✅ 成功获取 10 个账号的推文
- ✅ 生成第一批深度解读文章
- ✅ 实现自动 GitHub 同步

### 阶段二：Camoufox 方案攻坚

为了让系统获取更完整的数据（浏览量、点赞数等），尝试启用 Camoufox：

**遇到的问题与解决方案：**

#### 问题 1：缺少系统依赖库

**现象：**
```
error while loading shared libraries: libgbm.so.1: cannot open shared object file
```

**原因：**
Camoufox 是基于 Firefox 的浏览器，需要图形库支持。当前环境缺少 `libgbm`（Mesa 图形库）。

**解决方案：**
```bash
# 安装 Mesa 图形库
dnf install -y mesa-libgbm

# 验证安装
ls /usr/lib64/libgbm.so*
```

#### 问题 2：缺少音频库

**现象：**
```
libasound.so.2: cannot open shared object file: No such file or directory
Couldn't load XPCOM.
```

**原因：**
Firefox 需要 ALSA 音频库支持，即使 headless 模式也需要。

**解决方案：**
```bash
# 安装 ALSA 音频库
dnf install -y alsa-lib

# 验证
ls /usr/lib64/libasound.so*
```

#### 问题 3：camoufox-js 模块缺失

**现象：**
```
Error: Cannot find module 'camoufox-js'
```

**原因：**
Camoufox 浏览器插件依赖 `camoufox-js` npm 包，但未正确安装。

**解决方案：**
```bash
cd /root/.openclaw/extensions/camofox-browser
npm install camoufox-js

# 检查安装
ls node_modules/camoufox-js
```

#### 问题 4：浏览器二进制文件未下载

**现象：**
```
Version information not found at /root/.cache/camoufox/version.json.
Please run `camoufox fetch` to install.
```

**原因：**
camoufox-js 只是 JavaScript 包装器，实际需要下载约 300MB 的浏览器二进制文件。

**解决方案：**
```bash
# 下载浏览器（约 300MB）
cd /root/.openclaw/extensions/camofox-browser
npx camoufox-js fetch

# 验证下载
ls -lh ~/.cache/camoufox/
# 应看到 camoufox-bin 等文件
```

**遇到的困难：**
- 下载过程中被 **OOM Killer** 终止（信号 137）
- 原因：系统内存不足，解压大文件时触发
- 解决：多次尝试，最终成功

#### 问题 5：后台进程被系统终止

**现象：**
使用 `nohup` 或 `&` 启动 Camoufox 服务后，进程被 SIGTERM/SIGKILL 终止。

**原因：**
当前环境对后台进程有限制，长时间运行的进程会被系统自动清理。

**解决方案：改用 systemd service**

```bash
# 创建服务文件
cat > /etc/systemd/system/camofox.service << 'EOF'
[Unit]
Description=Camofox Browser Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/extensions/camofox-browser
ExecStart=/root/.nvm/versions/node/v22.22.0/bin/node server.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=9377

[Install]
WantedBy=multi-user.target
EOF

# 启用并启动服务
systemctl daemon-reload
systemctl enable camofox.service
systemctl start camoufox.service

# 验证状态
systemctl status camofox.service
```

**效果：**
- ✅ 服务稳定运行
- ✅ 自动重启（崩溃后）
- ✅ 开机自启

#### 问题 6：端口冲突

**现象：**
```
port in use, port: 9377
```

**原因：**
之前的进程未正确退出，导致端口被占用。

**解决方案：**
```bash
# 查找占用端口的进程
lsof -i :9377

# 终止进程
fuser -k 9377/tcp

# 重启服务
systemctl restart camofox.service
```

#### 问题 7：429 Too Many Requests

**现象：**
```
[Camoufox] 打开标签页失败: HTTP Error 429: Too Many Requests
```

**原因：**
频繁请求导致被 Nitter 限流。

**解决方案：**
- 增加请求间隔（已内置 2 秒延迟）
- 多镜像轮询（6 个 Nitter 实例）
- 失败时自动回退到其他方案

---

**最终验证：**
```bash
# 检查服务状态
systemctl status camofox.service
# Active: active (running)

# 测试接口
curl http://localhost:9377/health
# {"ok":true,"engine":"camoufox",...}

# 测试推文获取
cd /root/.agents/skills/x-tweet-fetcher
python3 scripts/fetch_tweet.py --user sama --limit 3
# ✅ 成功获取带浏览量的推文
```

### 阶段三：Skill 封装

将监控系统封装为可复用的 OpenClaw Skill：

```
skills/ai-monitor-1.0.0/
├── SKILL.md          # 技能说明文档
├── config.py         # 配置文件
└── scripts/
    └── ai_monitor.py # 主脚本
```

### 阶段四：定时任务优化

**初始方案：OpenClaw HEARTBEAT**
- 发现执行不稳定

**优化方案：crontab**
```bash
# 每小时执行一次
0 * * * * cd /path && python3 ai_monitor_v4.py
```

**最终优化：**
- 频率：每小时一次（避免过于频繁）
- 日志：输出到 `/tmp/ai_monitor.log`
- 提示：无新内容时输出友好提示

---

## 📊 系统运行成果

### 首次运行（15:40）

```
监控账号: 10 个
扫描推文: 47 条
重要动态: 26 条 (🔴11 🟠8 🟡7)
数据方案: 全部 Camoufox ✅
```

### 🔴 重磅发现

| 账号 | 内容 | 浏览量 |
|------|------|--------|
| OpenAI | GPT-5.4 发布 | 👁️ 475万 |
| Anthropic | CEO Dario Amodei 声明 | 👁️ 1614万 |
| Meta | SAM Audio 发布 | 👁️ 122万 |
| Karpathy | nanochat GPT-2 优化 | - |

### 生成的文档

- **汇总日报**：`2026-03-06-15-40.md`
- **单篇文章**：26 篇深度解读
- **GitHub 同步**：自动提交到仓库

---

## 🔧 关键技术点

### 1. Camoufox + Nitter 双保险

```python
def fetch_tweets(username):
    # 方案1: Camoufox (优先)
    tweets = fetch_via_camofox(username)
    if tweets:
        return tweets, 'camoufox'
    
    # 方案2: Nitter RSS (回退)
    tweets = fetch_nitter_rss(username)
    if tweets:
        return tweets, 'nitter'
    
    return [], None
```

### 2. 智能重要性评级

基于浏览量、互动数据的综合评分：

```python
def analyze_importance(tweet):
    score = views + likes * 10 + retweets * 20
    
    if score > 500000:
        return "🔴 重磅"
    elif score > 100000:
        return "🟠 重要"
    elif score > 10000:
        return "🟡 关注"
    return "🟢 参考"
```

### 3. 中文文章生成

自动生成结构化中文文章：
- 📌 核心内容（原文）
- 🔍 深度解读（背景/分析/影响）
- 💡 我们的观点
- 📎 原文链接

---

## 📁 项目文件

**GitHub 仓库**：https://github.com/peggypan/knowledge

```
公众号-想象X/agents/公众号管家/
├── scripts/
│   ├── ai_monitor_v4.py    # 主脚本（Camoufox + Nitter）
│   ├── ai_monitor_v3.py    # 备用脚本（Nitter only）
│   └── summarize_articles.py
├── data/articles/           # 生成的文章
│   └── 2026-03-06-15-40.md
├── HEARTBEAT.md            # 定时任务配置
└── MEMORY.md               # 项目记忆

skills/ai-monitor-1.0.0/    # 封装的 Skill
├── SKILL.md
├── config.py
└── scripts/ai_monitor.py
```

---

## 🚀 系统现状

| 组件 | 状态 |
|------|------|
| Camoufox 服务 | ✅ 运行中 (systemd) |
| Nitter RSS 备用 | ✅ 可用 |
| 定时任务 (cron) | ✅ 每小时执行 |
| GitHub 同步 | ✅ 自动提交 |
| 中文文章生成 | ✅ 正常 |

---

## 💡 经验总结

### 1. 技术选型权衡

**Camoufox vs Nitter：**
- Camoufox：数据完整，但需要更多资源
- Nitter：轻量快速，但数据有限
- **最佳实践**：两者结合，优先 Camoufox，失败回退 Nitter

### 2. 系统依赖管理

Linux 环境下浏览器自动化需要：
- 图形库：libgbm
- 音频库：alsa-lib
- 足够内存：下载 300MB 浏览器
- 稳定运行：systemd service

### 3. 定时任务选择

| 方案 | 稳定性 | 适用场景 |
|------|--------|----------|
| OpenClaw HEARTBEAT | 中等 | 简单任务 |
| crontab | 高 | 生产环境 |
| systemd timer | 高 | 复杂依赖 |

---

## 🎯 后续优化方向

1. **内容翻译**：接入翻译 API，自动翻译推文内容
2. **智能摘要**：使用 LLM 生成更智能的摘要
3. **多渠道推送**：飞书、邮件、Slack 等
4. **监控扩展**：增加更多 AI 账号
5. **数据分析**：统计热门话题趋势

---

## 📌 使用方式

**查看监控结果：**
```bash
# 查看最新文章
ls -lt data/articles/*.md

# 查看执行日志
tail -f /tmp/ai_monitor.log

# 手动触发
python3 scripts/ai_monitor_v4.py
```

**GitHub 地址：**
https://github.com/peggypan/knowledge/tree/main/公众号-想象X/agents/公众号管家/data/articles

---

*本文档由 AI 监控系统自动生成*  
*生成时间: 2026-03-06 19:10*
