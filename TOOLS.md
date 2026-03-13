# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## 🔐 Git/GitHub 配置

### 用户身份
- **GitHub 用户名**: `peggypan`
- **邮箱**: openclaw@ai.local
- **名称**: OpenClaw Bot

### 认证方式
- **协议**: SSH
- **密钥位置**: `~/.ssh/id_ed25519`
- **权限**: 已配置全局推送权限（所有项目）

### 常用项目
| 项目 | 本地路径 | 远程地址 |
|------|----------|----------|
| knowledge | `/root/.openclaw/workspace/knowledge` | SSH 已配置 |
| filmstudio | `/root/.openclaw/workspace/filmstudio` | `git@github.com:peggypan/filmstudio.git` |

### 推送命令
```bash
git push origin main
```

---
*记录日期: 2026-03-13*
*重要提醒: 有权限，不需要 token，直接用 SSH 推送*
