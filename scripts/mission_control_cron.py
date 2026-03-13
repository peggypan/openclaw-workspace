#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mission Control 定时任务 + 飞书推送
用法: python3 mission_control_cron.py [morning|evening|weekly]
"""

import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# 配置
FEISHU_CHAT_ID = "oc_f815b8902d22c11ba7f692193bfabe51"  # 与你的私聊ID
WORKSPACE_DIR = Path("/root/.openclaw/workspace")
LOG_FILE = Path("/tmp/mission_control.log")

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')

def send_feishu_message(content):
    """发送飞书消息 - 使用 OpenClaw 命令"""
    try:
        import subprocess
        import tempfile
        import os
        
        # 创建临时文件存储消息
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(content.strip())
            temp_file = f.name
        
        try:
            # 读取消息内容
            with open(temp_file, 'r', encoding='utf-8') as f:
                message_content = f.read().strip()
            
            # 使用 -m 参数发送（根据 help 信息）
            cmd = [
                'openclaw', 'message', 'send',
                '--channel', 'feishu',
                '--target', FEISHU_CHAT_ID,
                '-m', message_content
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                log("✓ 飞书消息发送成功")
                return True
            else:
                log(f"✗ 飞书消息发送失败: {result.stderr}")
                return False
        finally:
            # 清理临时文件
            os.unlink(temp_file)
            
    except Exception as e:
        log(f"✗ 发送异常: {e}")
        return False

def morning_routine():
    """晨报"""
    log("执行 Morning Routine...")
    
    # 读取今日日程
    calendar_file = WORKSPACE_DIR / "CALENDAR.md"
    today_tasks = "暂无"
    if calendar_file.exists():
        content = calendar_file.read_text(encoding='utf-8')
        # 简单提取今天的任务
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Today' in line or '今天' in line:
                today_tasks = '\n'.join(lines[i:i+10])
                break
    
    message = f"""🌅 Mission Control - 晨报时间

早上好！☀️ 现在是 {datetime.now().strftime('%H:%M')}。

📋 请回复：执行 Morning Routine

让我帮你：
• 查看今日日程
• 检查本周重点  
• 扫描紧急事项
• 生成每日简报

---
今日待办已准备好，等待你的指令 🎬"""
    
    if send_feishu_message(message):
        log("Morning Routine 提醒已发送")
    else:
        log("Morning Routine 提醒发送失败，但任务已记录")
    
    # 同时创建一个标记文件，表示已触发
    trigger_file = WORKSPACE_DIR / ".mission_control_trigger"
    trigger_file.write_text(f"morning_{datetime.now().strftime('%Y-%m-%d')}", encoding='utf-8')

def evening_routine():
    """日终总结"""
    log("执行 Evening Routine...")
    
    message = f"""🌙 Mission Control - 日终总结时间

晚上好！🌙 现在是 {datetime.now().strftime('%H:%M')}。

📋 请回复：执行 Evening Routine

让我帮你：
• 回顾今日完成情况
• 更新项目进度
• 归档已完成任务
• 预览明日待办

---
今天过得怎么样？让我帮你总结一下 📊"""
    
    send_feishu_message(message)
    log("Evening Routine 提醒已发送")

def weekly_routine():
    """周报"""
    log("执行 Weekly Routine...")
    
    message = f"""📊 Mission Control - 周报时间

周日晚上好！📊 现在是 {datetime.now().strftime('%H:%M')}。

📋 请回复：执行 Weekly Routine

让我帮你：
• 生成本周生产力报告
• 更新所有项目进度
• 检查下周里程碑
• 规划下周重点

---
让我们一起回顾本周的成就 🎯"""
    
    send_feishu_message(message)
    log("Weekly Routine 提醒已发送")

def main():
    if len(sys.argv) < 2:
        log("错误：缺少任务类型参数")
        log("用法: python3 mission_control_cron.py [morning|evening|weekly]")
        sys.exit(1)
    
    task_type = sys.argv[1].lower()
    log(f"Mission Control {task_type} 任务触发")
    
    if task_type == "morning":
        morning_routine()
    elif task_type == "evening":
        evening_routine()
    elif task_type == "weekly":
        weekly_routine()
    else:
        log(f"错误：未知任务类型 {task_type}")
        sys.exit(1)
    
    log("=" * 40)

if __name__ == "__main__":
    main()
