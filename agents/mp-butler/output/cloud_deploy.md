# 如何进行云养虾：OpenClaw 云端自部署完整指南

> 把 AI 助手养在云端，24小时随时待命

---

## 一、准备工作：选购云服务器

### 1.1 确定你的需求

在购买服务器之前，先想清楚：
- 主要访问国内资源还是海外资源？
- 预算范围是多少？
- 需要多大的计算能力？

**访问国内资源**：选择阿里云、腾讯云的国内节点，访问速度快，但需要 ICP 备案。

**访问海外资源**：选择 Vultr、DigitalOcean 的海外节点（东京、新加坡、洛杉矶），免备案，访问 OpenAI、Claude 等海外服务速度快。

**兼顾两者**：选择阿里云香港节点，不用备案，国内访问速度也不错。

### 1.2 服务商推荐

**阿里云 ECS**
- 价格：60-200 元/月
- 特点：国内生态最完善，文档丰富，学生有优惠
- 适合：主要访问国内资源的用户
- 注意：需要备案，审核周期约 1-2 周

**腾讯云 CVM**
- 价格：60-200 元/月
- 特点：国内访问速度快，经常有活动优惠
- 适合：主要访问国内资源的用户
- 注意：同样需要备案

**Vultr**
- 价格：5-20 美元/月（约 35-140 元）
- 特点：按小时计费，随时可删，节点遍布全球
- 适合：需要访问海外资源，追求性价比
- 推荐节点：东京（国内访问快）、新加坡、洛杉矶

**DigitalOcean**
- 价格：6-24 美元/月（约 40-170 元）
- 特点：界面友好，文档丰富，适合新手
- 适合：第一次海外部署，不想折腾

### 1.3 配置选择

**个人尝鲜**
- 配置：1核 CPU，2GB 内存，40GB SSD
- 价格：约 50-70 元/月
- 说明：够跑基础功能，同时运行 1-2 个简单任务

**日常使用**
- 配置：2核 CPU，4GB 内存，80GB SSD
- 价格：约 100-150 元/月
- 说明：流畅运行，可同时运行多个 Agent，响应速度快

**重度使用**
- 配置：4核 CPU，8GB 内存，160GB SSD
- 价格：约 200-300 元/月
- 说明：大任务、复杂流程也能应对，适合团队使用

**系统选择**：强烈推荐 Ubuntu 22.04 LTS，最稳定，遇到问题最容易搜索到解决方案。

### 1.4 购买后获取连接信息

购买完成后，你会收到：
- 服务器 IP 地址
-  root 用户名和密码（或 SSH 密钥）
-  控制面板地址

保存好这些信息，下一步连接服务器需要用到。

---

## 二、服务器初始化配置

### 2.1 连接服务器

**Mac/Linux 用户**：
打开终端，执行：
```bash
ssh root@你的服务器IP
```
输入密码后即可连接。

**Windows 用户**：
推荐使用 PowerShell（Win10/11 自带）或 PuTTY。

PowerShell 命令：
```powershell
ssh root@你的服务器IP
```

**首次连接提示**：
如果提示 "Are you sure you want to continue connecting?"，输入 `yes` 回车。

### 2.2 更新系统

连接成功后，先更新系统到最新版本：

```bash
# 更新软件包列表
apt update

# 升级已安装的软件包
apt upgrade -y

# 安装常用工具
git curl wget vim htop
```

这个过程可能需要几分钟，取决于服务器的网络速度。

### 2.3 创建普通用户（推荐）

为了安全，建议创建一个普通用户，日常操作都用这个用户：

```bash
# 创建新用户，用户名可以自定义，这里用 openclaw
adduser openclaw

# 按提示设置密码，其他信息可以直接回车跳过

# 将用户添加到 sudo 组，使其有管理员权限
usermod -aG sudo openclaw

# 切换到新用户
su - openclaw
```

以后连接服务器，建议先用普通用户登录，需要管理员权限时再加 `sudo`。

### 2.4 配置防火墙

防火墙可以保护服务器免受未经授权的访问：

```bash
# 允许 SSH 连接（必须，否则你会被锁在外面）
sudo ufw allow 22

# 如果需要 Web 访问，允许 HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# 启用防火墙
sudo ufw enable

# 查看防火墙状态
sudo ufw status
```

---

## 三、安装 OpenClaw

### 3.1 安装 Node.js

OpenClaw 基于 Node.js 构建，需要 22.x 或更高版本。

```bash
# 安装 nvm（Node 版本管理器）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

# 加载 nvm 到当前会话
source ~/.bashrc

# 安装 Node.js 22
nvm install 22
nvm use 22

# 验证安装
node --version
# 应显示 v22.x.x

npm --version
# 应显示 10.x.x
```

如果 `source ~/.bashrc` 后命令找不到，尝试关闭 SSH 连接重新登录。

### 3.2 安装 OpenClaw

```bash
# 全局安装 OpenClaw CLI
npm install -g openclaw

# 验证安装
openclaw --version
```

如果安装速度慢，可以切换国内 npm 镜像：
```bash
npm config set registry https://registry.npmmirror.com
npm install -g openclaw
```

### 3.3 运行初始化向导

```bash
openclaw setup
```

向导会引导你完成：
1. **选择默认 AI 模型**：推荐选择 kimi-coding/kimi-for-coding，性价比高，中文支持好
2. **配置消息渠道**：如果要连接飞书，需要准备 webhook 地址
3. **设置工作目录**：默认即可，按回车
4. **启用插件**：建议启用 browser（浏览器自动化）和 healthcheck（健康检查）

### 3.4 配置飞书消息（可选）

如果你想让 OpenClaw 能在飞书里回复你：

**步骤 1：创建飞书群机器人**
1. 打开飞书，进入你想连接的群聊
2. 点击右上角「设置」→「群机器人」→「添加机器人」
3. 选择「自定义机器人」
4. 复制 webhook 地址（类似 https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx）

**步骤 2：配置 OpenClaw**
```bash
# 编辑配置文件
nano ~/.openclaw/config.yaml
```

找到 channels 部分，添加：
```yaml
channels:
  feishu:
    enabled: true
    webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx"
```

按 Ctrl+O 保存，Ctrl+X 退出。

**步骤 3：测试**
在飞书群里 @机器人，发送「你好」，看是否能收到回复。

---

## 四、保持服务运行

### 4.1 为什么需要守护进程

直接在 SSH 中运行 `openclaw gateway start`，关闭 SSH 连接后服务就会停止。我们需要一个"守护进程"，让服务在后台持续运行，即使退出 SSH 也不断开。

### 4.2 使用 PM2 守护（推荐）

PM2 是 Node.js 应用最流行的进程管理工具。

**安装 PM2**：
```bash
npm install -g pm2
```

**创建启动脚本**：
```bash
cat > ~/openclaw-start.sh << 'EOF'
#!/bin/bash
export PATH="$HOME/.nvm/versions/node/v22.22.0/bin:$PATH"
openclaw gateway start
EOF

chmod +x ~/openclaw-start.sh
```

**启动并设置开机自启**：
```bash
# 用 PM2 启动
pm2 start ~/openclaw-start.sh --name openclaw

# 生成开机启动脚本
pm2 startup

# 保存当前进程列表
pm2 save
```

**常用 PM2 命令**：
```bash
# 查看状态
pm2 status

# 查看日志
pm2 logs openclaw

# 重启服务
pm2 restart openclaw

# 停止服务
pm2 stop openclaw

# 删除服务
pm2 delete openclaw
```

### 4.3 使用 systemd（Linux 系统服务）

如果你更喜欢系统原生的服务管理方式：

```bash
# 创建服务文件
sudo cat > /etc/systemd/system/openclaw.service << 'EOF'
[Unit]
Description=OpenClaw Service
After=network.target

[Service]
Type=simple
User=openclaw
WorkingDirectory=/home/openclaw
Environment="PATH=/home/openclaw/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin"
ExecStart=/home/openclaw/.nvm/versions/node/v22.22.0/bin/openclaw gateway start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start openclaw

# 设置开机自启
sudo systemctl enable openclaw

# 查看状态
sudo systemctl status openclaw

# 查看日志
sudo journalctl -u openclaw -f
```

---

## 五、费用说明与优化

### 5.1 费用构成

云养虾的总成本包括两部分：

**固定成本（服务器费用）**
- 1核 2GB：约 50-70 元/月
- 2核 4GB：约 100-150 元/月
- 4核 8GB：约 200-300 元/月

这部分费用是固定的，不管你用不用都要付。

**变动成本（AI 模型调用费）**
- Kimi：约 0.001-0.01 元/千字符
- GPT-4：约 0.1-0.3 元/千字符
- 按实际调用量计费，用得多花得多

### 5.2 使用成本估算

**轻度使用**（每天约 100 次调用，每次 500 字）
- 服务器：70 元/月
- 模型费：约 20-50 元/月
- **总计：约 90-120 元/月**

**中度使用**（每天约 1000 次调用）
- 服务器：100 元/月
- 模型费：约 100-200 元/月
- **总计：约 200-300 元/月**

**重度使用**（每天超过 5000 次调用）
- 服务器：150 元/月
- 模型费：约 300-800 元/月
- **总计：约 450-950 元/月**

### 5.3 成本优化建议

**选择合适的 AI 模型**
- 日常任务用 Kimi，性价比高
- 复杂任务才用 GPT-4，能力更强但更贵
- 简单任务可以用免费模型或本地模型

**优化 Prompt**
- 越清晰的 Prompt，AI 输出越精准，减少不必要的调用
- 设置合理的上下文长度，不要每次都传很长的历史记录

**使用缓存**
- 对于重复的问题，缓存答案直接返回，不再调用 API

**定期清理日志**
```bash
# PM2 清理日志
pm2 flush

# 清理系统日志
sudo journalctl --vacuum-time=7d
```

### 5.4 数据备份

定期备份配置，防止数据丢失：

```bash
# 打包配置目录
tar czf openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/

# 下载到本地（在本地终端执行）
scp root@服务器IP:~/openclaw-backup-*.tar.gz ./
```

建议设置自动备份：
```bash
crontab -e

# 添加以下行（每天凌晨 3 点备份，保留 7 天）
0 3 * * * tar czf ~/backups/openclaw-backup-$(date +\%Y\%m\%d).tar.gz ~/.openclaw/ && find ~/backups/ -name "openclaw-backup-*.tar.gz" -mtime +7 -delete
```

---

**遇到问题？**
- OpenClaw 文档：https://docs.openclaw.ai
- 社区 Discord：https://discord.com/invite/clawd

*祝你的云端龙虾健康成长！☁️🦞*
