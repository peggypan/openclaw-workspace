#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书通知发送辅助脚本
读取通知文件并发送到飞书群
"""

import sys
import json
from pathlib import Path

# 飞书群 ID
FEISHU_CHAT_ID = "oc_f815b8902d22c11ba7f692193bfabe51"
DATA_DIR = Path(__file__).parent.parent / "data"
NOTIFY_FILE = DATA_DIR / "feishu_notification.txt"
SENT_MARKER = DATA_DIR / "feishu_notification.sent"

def send_via_openclaw(message):
    """使用 openclaw 命令发送飞书消息"""
    import subprocess
    import os
    try:
        # 将消息写入临时文件避免命令行长度问题
        temp_msg = DATA_DIR / ".feishu_msg_temp.txt"
        with open(temp_msg, 'w', encoding='utf-8') as f:
            f.write(message)
        
        # 设置完整的环境变量（cron 环境 PATH 不完整）
        env = os.environ.copy()
        env['PATH'] = '/root/.nvm/versions/node/v22.22.0/bin:' + env.get('PATH', '')
        
        # 使用 openclaw 完整路径
        OPENCLAW_BIN = "/root/.nvm/versions/node/v22.22.0/bin/openclaw"
        cmd = f'cat {temp_msg} | {OPENCLAW_BIN} message send --channel feishu --target {FEISHU_CHAT_ID}'
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            timeout=15,
            env=env
        )
        
        temp_msg.unlink(missing_ok=True)
        
        return result.returncode == 0
    except Exception as e:
        print(f"发送失败: {e}")
        return False

def main():
    if not NOTIFY_FILE.exists():
        print("没有待发送的通知")
        return 0
    
    # 检查是否已经发送过
    if SENT_MARKER.exists():
        notify_mtime = NOTIFY_FILE.stat().st_mtime
        sent_mtime = SENT_MARKER.stat().st_mtime
        if sent_mtime >= notify_mtime:
            print("通知已发送过，跳过")
            return 0
    
    # 读取通知内容
    with open(NOTIFY_FILE, 'r', encoding='utf-8') as f:
        message = f.read()
    
    if not message.strip():
        print("通知内容为空")
        return 0
    
    print(f"发送飞书通知到群 {FEISHU_CHAT_ID}...")
    print(f"消息长度: {len(message)} 字符")
    
    # 尝试发送
    if send_via_openclaw(message):
        print("✅ 飞书消息发送成功")
        # 更新发送标记
        SENT_MARKER.touch()
        return 0
    else:
        print("❌ 飞书消息发送失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
