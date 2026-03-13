#!/bin/bash
# Mission Control 定时任务脚本
# 用法: ./mission_control_cron.sh [morning|evening|weekly]

TASK_TYPE=$1
WORKSPACE_DIR="/root/.openclaw/workspace"
LOG_FILE="/tmp/mission_control.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Mission Control $TASK_TYPE 任务触发" >> $LOG_FILE

# 创建通知消息文件
NOTIFY_FILE="/tmp/mission_control_notify.txt"

case $TASK_TYPE in
  morning)
    echo "[$DATE] 执行晨报准备..." >> $LOG_FILE
    
    cat > "$NOTIFY_FILE" << 'EOF'
🌅 Mission Control - 晨报时间

早上好！☀️ 该执行晨报了。

📋 请对我说："执行 Morning Routine"

---
今日待办已准备好，等待你的指令 🎬
EOF
    
    echo "[$DATE] ✓ 晨报准备完成" >> $LOG_FILE
    ;;
    
  evening)
    echo "[$DATE] 执行日终总结准备..." >> $LOG_FILE
    
    cat > "$NOTIFY_FILE" << 'EOF'
🌙 Mission Control - 日终总结时间

晚上好！🌙 该执行日终总结了。

📋 请对我说："执行 Evening Routine"

---
今天过得怎么样？让我帮你总结一下 📊
EOF
    
    echo "[$DATE] ✓ 日终准备完成" >> $LOG_FILE
    ;;
    
  weekly)
    echo "[$DATE] 执行周报准备..." >> $LOG_FILE
    
    cat > "$NOTIFY_FILE" << 'EOF'
📊 Mission Control - 周报时间

周日晚上好！📊 该生成本周报告了。

📋 请对我说："执行 Weekly Routine"

---
让我们一起回顾本周的成就 🎯
EOF
    
    echo "[$DATE] ✓ 周报准备完成" >> $LOG_FILE
    ;;
    
  *)
    echo "[$DATE] 错误：未知任务类型 $TASK_TYPE" >> $LOG_FILE
    exit 1
    ;;
esac

# 尝试发送飞书通知（如果 openclaw 可用）
if command -v openclaw &> /dev/null; then
    echo "[$DATE] 尝试发送飞书通知..." >> $LOG_FILE
    # 使用 send_feishu_notify.py 方式或记录到日志
    echo "[$DATE] 飞书通知内容已保存到: $NOTIFY_FILE" >> $LOG_FILE
else
    echo "[$DATE] openclaw 命令不可用，跳过飞书通知" >> $LOG_FILE
fi

echo "[$DATE] ================================" >> $LOG_FILE
