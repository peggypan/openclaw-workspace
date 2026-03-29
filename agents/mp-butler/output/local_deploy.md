# 如何本地养虾：OpenClaw 本地部署完整指南

> 把 AI 助手养在家里，数据不出家门

---

## 一、设备选择与准备

### 1.1 可选设备一览

本地养虾的最大优势是利用现有设备，无需额外购买服务器。以下是几种常见的选择：

**旧电脑或闲置笔记本**
- 最低配置：4核 CPU，4GB 内存
- 推荐配置：4核 CPU，8GB 内存
- 优点：性能通常最好，有屏幕键盘方便调试，无需额外购买
- 缺点：功耗较高（50-100W），体积大占地方，风扇可能有噪音
- 适用：有闲置电脑，不介意电费，想要最好性能

**树莓派 4B**
- 最低配置：4GB 内存版本
- 推荐配置：8GB 内存版本
- 优点：超低功耗（5-8W），体积小可随意放置，社区生态丰富
- 缺点：性能较弱（ARM 架构），需要散热片，SD 卡容易损坏
- 适用：追求极致省电，轻度使用，喜欢折腾
- 购买建议：主板 600-800 元，加上电源、散热、存储约 1000 元

**NAS（群晖、威联通）**
- 最低配置：4核 CPU，4GB 内存
- 推荐配置：4核 CPU，8GB+ 内存
- 优点：本来就是 24 小时开机，有完善的备份机制，存储空间大
- 缺点：需要开启 SSH，CPU 性能通常较弱，配置相对复杂
- 适用：已有 NAS，想充分利用现有设备
- 注意：群晖 Docker 部署可能遇到权限问题，建议用虚拟机或 SSH 安装

**迷你主机（推荐新手）**
- 最低配置：Intel N100，4GB 内存
- 推荐配置：Intel i3，8GB 内存
- 优点：性价比高（800-1500 元），x86 架构兼容性好，体积小功耗适中（10-20W）
- 缺点：需要额外购买
- 适用：想要平衡性能、功耗、价格的新手
- 推荐型号：零刻 SER5/6 系列、英特尔 NUC、摩方 M600

**Mac mini**
- 最低配置：M1 芯片，8GB 内存
- 推荐配置：M2 芯片，16GB 内存
- 优点：性能优秀，系统稳定，功耗低
- 缺点：价格较高（3000 元+）
- 适用：已有 Mac mini，或预算充足追求最好体验

### 1.2 功耗与电费估算

设备 24 小时运行的电费（按 0.6 元/度计算）：

- **树莓派 4B**：约 5W，月电费约 2 元
- **迷你主机**：约 15W，月电费约 6 元
- **旧笔记本**：约 50W，月电费约 22 元
- **台式机**：约 150W，月电费约 65 元

如果担心电费，推荐树莓派或迷你主机。

### 1.3 系统要求

OpenClaw 支持以下操作系统：
- **Linux**：Ubuntu 22.04 LTS（推荐）、Debian 11+、CentOS 8+
- **macOS**：macOS 13+（Ventura 或更新）
- **Windows**：通过 WSL2（Windows Subsystem for Linux）运行

---

## 二、macOS 安装指南

### 2.1 安装 Homebrew

Homebrew 是 macOS 上最流行的包管理器。

```bash
# 如果还没有安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2.2 安装 Node.js

```bash
# 使用 Homebrew 安装 Node 22
brew install node@22

# 将 Node 添加到 PATH
echo 'export PATH="/opt/homebrew/opt/node@22/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 验证安装
node --version
npm --version
```

### 2.3 安装 OpenClaw

```bash
# 全局安装
npm install -g openclaw

# 验证
openclaw --version

# 初始化配置
openclaw setup
```

### 2.4 配置开机启动

创建 LaunchAgent 配置文件：

```bash
mkdir -p ~/Library/LaunchAgents

cat > ~/Library/LaunchAgents/com.openclaw.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/openclaw</string>
        <string>gateway</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# 加载配置
launchctl load ~/Library/LaunchAgents/com.openclaw.plist

# 查看状态
launchctl list | grep openclaw
```

---

## 三、Linux 安装指南

适用于 Ubuntu、Debian、CentOS 等 Linux 发行版。

### 3.1 安装 Node.js

```bash
# 安装 nvm（Node 版本管理器）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

# 加载 nvm
source ~/.bashrc

# 安装 Node.js 22
nvm install 22
nvm use 22

# 验证
node --version
npm --version
```

### 3.2 安装 OpenClaw

```bash
# 全局安装
npm install -g openclaw

# 验证
openclaw --version

# 初始化
openclaw setup
```

### 3.3 配置系统服务（推荐）

使用 systemd 让 OpenClaw 作为系统服务运行：

```bash
# 创建服务文件
sudo tee /etc/systemd/system/openclaw.service > /dev/null << 'EOF'
[Unit]
Description=OpenClaw Service
After=network.target

[Service]
Type=simple
User=$USER
Environment="PATH=/home/$USER/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin"
ExecStart=/home/$USER/.nvm/versions/node/v22.22.0/bin/openclaw gateway start
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

常用命令：
```bash
# 停止服务
sudo systemctl stop openclaw

# 重启服务
sudo systemctl restart openclaw

# 查看日志
sudo journalctl -u openclaw --since "1 hour ago"
```

---

## 四、Windows 安装指南

Windows 不是 OpenClaw 的最佳平台，建议通过 WSL2（Windows Subsystem for Linux）运行。

### 4.1 安装 WSL2

以管理员身份打开 PowerShell，执行：

```powershell
# 安装 WSL
wsl --install

# 安装完成后重启电脑
# 然后安装 Ubuntu
wsl --install -d Ubuntu-22.04
```

### 4.2 在 WSL 中安装 OpenClaw

重启后，WSL 会自动启动。接下来的步骤与 Linux 完全相同：

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
source ~/.bashrc
nvm install 22

# 安装 OpenClaw
npm install -g openclaw
openclaw setup
```

### 4.3 配置开机自动启动 WSL

创建一个批处理文件：

```powershell
# 创建启动脚本
@"
@echo off
wsl -d Ubuntu-22.04 -u $env:USERNAME bash -c 'source ~/.bashrc && sudo systemctl start openclaw'
"@ | Out-File -FilePath "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\start-openclaw.bat" -Encoding ASCII
```

或者手动创建：
1. 打开记事本，输入：`wsl -d Ubuntu-22.04 -u 你的用户名 bash -c 'source ~/.bashrc && sudo systemctl start openclaw'`
2. 保存到 `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\start-openclaw.bat`

---

## 五、外网访问与费用说明

### 5.1 外网访问方案

本地部署默认只能在局域网内访问。如果需要在外网访问，有以下几种方案：

**方案 1：Tailscale（强烈推荐）**

Tailscale 是一个免费的 VPN 工具，可以让你在任何地方安全地访问家里的设备。

```bash
# Linux/macOS 安装
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Windows 下载安装包安装
```

使用步骤：
1. 在家里的设备上安装 Tailscale 并登录
2. 在手机或外出电脑上安装 Tailscale App，登录同一账号
3. 手机就能通过 Tailscale 分配的 IP 访问家里的 OpenClaw

优点：免费、简单、安全，无需公网 IP，无需配置路由器

**方案 2：Cloudflare Tunnel**

适合想要绑定自己域名的用户。

```bash
# 下载 cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/

# 登录并创建隧道
cloudflared tunnel login
cloudflared tunnel create openclaw
cloudflared tunnel route dns openclaw yourdomain.com
cloudflared tunnel run openclaw
```

优点：免费，可绑定域名，有访问日志

**方案 3：frp 内网穿透**

需要一台有公网 IP 的云服务器做中转，配置较复杂，这里不展开。

**方案 4：公网 IP**

最理想的方案，但大部分家庭宽带没有公网 IP，需要联系运营商申请。

---

### 5.2 费用说明

本地养虾的费用构成：

**固定成本**
- 设备成本：0 元（利用现有设备）
- 电费：2-65 元/月，取决于设备功耗

**变动成本（AI 模型调用费）**
- Kimi：约 0.001-0.01 元/千字符
- GPT-4：约 0.1-0.3 元/千字符
- 按实际调用量计费，与部署方式无关

**使用成本估算**

轻度使用（每天 100 次调用）：
- 电费：6 元（迷你主机）
- 模型费：约 20 元
- **总计：约 26 元/月**

中度使用（每天 1000 次调用）：
- 电费：6 元
- 模型费：约 150 元
- **总计：约 156 元/月**

相比云服务器，本地部署的主要优势是固定成本极低，主要花费在模型调用上。

---

### 5.3 数据备份

本地部署的数据安全完全靠自己，务必定期备份：

**手动备份**
```bash
# 打包配置目录
tar czf openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/

# 复制到外部存储（U盘、移动硬盘等）
cp openclaw-backup-*.tar.gz /mnt/external-drive/
```

**自动备份（推荐）**
```bash
# 创建备份目录
mkdir -p ~/backups

# 编辑定时任务
crontab -e

# 添加以下行（每天凌晨 3 点备份，保留 30 天）
0 3 * * * tar czf ~/backups/openclaw-backup-$(date +\%Y\%m\%d).tar.gz ~/.openclaw/ && find ~/backups/ -name "openclaw-backup-*.tar.gz" -mtime +30 -delete
```

**云备份（可选）**
```bash
# 备份后同步到云盘（以 rclone 为例）
rclone sync ~/backups/ remote:backup-folder/
```

---

**写在最后**

本地养虾的核心价值是**掌控感**——数据完全不出家门，想怎么改就怎么改，没有任何限制。

这种掌控感需要付出一些代价：设备要一直开机，外网访问需要配置，维护靠自己。但正是这些折腾，让你更了解这个系统，也让你的 AI 助手真正成为「你的」。

如果你追求隐私、喜欢 DIY、或者单纯想省点钱，本地养虾是一个很好的选择。

祝你的本地龙虾健康成长！🏠🦞
