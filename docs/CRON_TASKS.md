# ⏰ 定时任务统一管理文档

> 所有自动化任务的统一配置和说明

---

## 📋 任务总览

| 任务名称 | 执行时间 | 类型 | 功能描述 |
|---------|---------|------|---------|
| Mission Control - 晨报 | 每天 07:30 | 飞书推送 | 推送晨报提醒，执行 Morning Routine |
| Mission Control - 日终 | 每天 19:30 | 飞书推送 | 推送日终提醒，执行 Evening Routine |
| Mission Control - 周报 | 每周日 20:00 | 飞书推送 | 推送周报提醒，执行 Weekly Routine |
| AI 动态监控 | 每小时 | 数据收集 | 监控 AI 大佬推文，生成中文解读 |
| 代码自动同步 | 每小时 | 系统维护 | 检查并同步代码更新 |
| Stargate 监控 | 每5分钟 | 系统服务 | 腾讯云监控服务保活 |

---

## 🔧 配置详情

### 1. Mission Control - 项目管理系统

**入口脚本**: `/root/.openclaw/workspace/scripts/unified_cron.sh`

#### 1.1 晨报 (mission-morning)
- **时间**: 每天 07:30
- **Crontab**: `30 7 * * *`
- **动作**: 发送飞书消息提醒执行 Morning Routine
- **日志**: `/tmp/mission_control.log`
- **消息内容**:
  ```
  🌅 Mission Control - 晨报时间
  早上好！☀️ 现在是 {time}。
  📋 请回复：执行 Morning Routine
  ```

#### 1.2 日终总结 (mission-evening)
- **时间**: 每天 19:30
- **Crontab**: `30 19 * * *`
- **动作**: 发送飞书消息提醒执行 Evening Routine
- **日志**: `/tmp/mission_control.log`
- **消息内容**:
  ```
  🌙 Mission Control - 日终总结时间
  晚上好！🌙 现在是 {time}。
  📋 请回复：执行 Evening Routine
  ```

#### 1.3 周报 (mission-weekly)
- **时间**: 每周日 20:00
- **Crontab**: `0 20 * * 0`
- **动作**: 发送飞书消息提醒执行 Weekly Routine
- **日志**: `/tmp/mission_control.log`
- **消息内容**:
  ```
  📊 Mission Control - 周报时间
  周日晚上好！📊 现在是 {time}。
  📋 请回复：执行 Weekly Routine
  ```

---

### 2. AI 动态监控系统 (公众号管家)

**入口脚本**: `/root/.openclaw/workspace/scripts/unified_cron.sh ai-monitor`

- **时间**: 每小时 (整点)
- **Crontab**: `0 * * * *`
- **工作目录**: `/root/.openclaw/workspace/knowledge/公众号-想象X/agents/公众号管家`
- **执行脚本**:
  ```bash
  python3 scripts/ai_monitor_v4.py
  python3 scripts/send_feishu_notify.py
  ```
- **功能**:
  1. 爬取 13 个 AI 大佬账号的最新推文
  2. 筛选重要/重磅内容
  3. 生成中文深度解读
  4. 推送到飞书
  5. 同步到 GitHub
- **日志**: `/tmp/ai_monitor.log`
- **监控账号**:
  - @sama (Sam Altman)
  - @OpenAI / @GoogleAI / @AnthropicAI / @AIatMeta / @MicrosoftAI
  - @karpathy (Andrej Karpathy)
  - @ylecun (Yann LeCun)
  - @demishassabis (DeepMind CEO)
  - @drfeifei (李飞飞)
  - @steipete (Peter Steinberger)
  - @realDonaldTrump (特朗普)
  - @elonmusk (马斯克)

---

### 3. 代码自动同步

**入口脚本**: `/root/.openclaw/workspace/scripts/unified_cron.sh auto-sync`

- **时间**: 每小时 (整点)
- **Crontab**: `0 * * * *`
- **执行脚本**: `/root/yawen-workspace/scripts/auto-sync.sh`
- **功能**: 自动检查并同步代码更新
- **日志**: `/tmp/unified_cron.log`

---

### 4. Stargate 系统监控

- **时间**: 每5分钟
- **Crontab**: `*/5 * * * *`
- **执行命令**:
  ```bash
  flock -xn /tmp/stargate.lock -c '/usr/local/qcloud/stargate/admin/start.sh > /dev/null 2>&1 &'
  ```
- **功能**: 腾讯云监控服务保活（系统自带）
- **日志**: 无（静默运行）

---

## 📁 相关文件

### 脚本文件
```
/root/.openclaw/workspace/scripts/
├── unified_cron.sh          # 统一入口脚本
├── mission_control_cron.py  # Mission Control Python脚本
└── mission_control_cron.sh  # 旧版脚本（已弃用）
```

### 日志文件
```
/tmp/
├── unified_cron.log         # 统一日志
├── mission_control.log      # Mission Control日志
└── ai_monitor.log           # AI监控日志
```

### 配置文件
```
/root/.openclaw/workspace/
├── TASKS.md                 # 任务列表
├── PROJECTS.md              # 项目索引
├── CALENDAR.md              # 日程安排
└── HEARTBEAT.md             # 自动化规则
```

---

## 🛠️ 手动操作

### 查看当前 Crontab
```bash
crontab -l
```

### 手动触发任务
```bash
# Mission Control
/root/.openclaw/workspace/scripts/unified_cron.sh mission-morning
/root/.openclaw/workspace/scripts/unified_cron.sh mission-evening
/root/.openclaw/workspace/scripts/unified_cron.sh mission-weekly

# AI 监控
/root/.openclaw/workspace/scripts/unified_cron.sh ai-monitor

# 代码同步
/root/.openclaw/workspace/scripts/unified_cron.sh auto-sync
```

### 查看日志
```bash
# 查看最新日志
tail -f /tmp/unified_cron.log

# 查看 Mission Control 日志
tail -f /tmp/mission_control.log

# 查看 AI 监控日志
tail -f /tmp/ai_monitor.log
```

---

## ⏱️ 执行时间表

```
时间轴 (24小时制):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
00:00  ┃  AI监控 | 代码同步
01:00  ┃  AI监控 | 代码同步
02:00  ┃  AI监控 | 代码同步
03:00  ┃  AI监控 | 代码同步
04:00  ┃  AI监控 | 代码同步
05:00  ┃  AI监控 | 代码同步
06:00  ┃  AI监控 | 代码同步
07:00  ┃  AI监控 | 代码同步
07:30  ┃  🌅 Mission Control 晨报 ⭐
08:00  ┃  AI监控 | 代码同步
09:00  ┃  AI监控 | 代码同步
10:00  ┃  AI监控 | 代码同步
11:00  ┃  AI监控 | 代码同步
12:00  ┃  AI监控 | 代码同步
13:00  ┃  AI监控 | 代码同步
14:00  ┃  AI监控 | 代码同步
15:00  ┃  AI监控 | 代码同步
16:00  ┃  AI监控 | 代码同步
17:00  ┃  AI监控 | 代码同步
18:00  ┃  AI监控 | 代码同步
19:00  ┃  AI监控 | 代码同步
19:30  ┃  🌙 Mission Control 日终 ⭐
20:00  ┃  AI监控 | 代码同步 | 📊 周报(周日)
21:00  ┃  AI监控 | 代码同步
22:00  ┃  AI监控 | 代码同步
23:00  ┃  AI监控 | 代码同步
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
每5分钟: Stargate 系统监控（后台）
```

---

## 📝 修改记录

| 日期 | 修改内容 |
|-----|---------|
| 2026-03-13 | 创建统一入口脚本 `unified_cron.sh` |
| 2026-03-13 | 配置 Mission Control 定时任务（早/晚/周报） |
| 2026-03-13 | 集成 AI 动态监控系统 |
| 2026-03-13 | 集成代码自动同步任务 |
| 2026-03-13 | 飞书推送功能测试通过 |

---

## 🔄 更新方法

如需修改定时任务：

1. **编辑入口脚本**:
   ```bash
   vim /root/.openclaw/workspace/scripts/unified_cron.sh
   ```

2. **编辑 Crontab**:
   ```bash
   crontab -e
   ```

3. **重新加载 Crontab**:
   ```bash
   crontab /tmp/new_crontab.txt
   ```

4. **推送更新到 GitHub**:
   ```bash
   cd /root/.openclaw/workspace
   git add -A
   git commit -m "update: 定时任务配置"
   git push origin master
   ```

---

*文档更新时间: 2026-03-13*
