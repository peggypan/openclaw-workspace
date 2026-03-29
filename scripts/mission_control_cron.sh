#!/bin/bash
# Mission Control 定时任务脚本
# 用法: ./mission_control_cron.sh [morning|evening|weekly]

# 设置 PATH 确保能找到 openclaw（cron 环境不完整）
export PATH="/root/.nvm/versions/node/v22.22.0/bin:$PATH"
OPENCLAW_BIN="/root/.nvm/versions/node/v22.22.0/bin/openclaw"

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

# 尝试发送飞书通知
if [ -x "$OPENCLAW_BIN" ]; then
    echo "[$DATE] 尝试发送飞书通知..." >> $LOG_FILE
    # 读取通知内容并发送
    MESSAGE=$(cat "$NOTIFY_FILE")
    $OPENCLAW_BIN message send --channel feishu --target "oc_f815b8902d22c11ba7f692193bfabe51" -m "$MESSAGE" >> $LOG_FILE 2>&1
    if [ $? -eq 0 ]; then
        echo "[$DATE] ✓ 飞书通知发送成功" >> $LOG_FILE
    else
        echo "[$DATE] ✗ 飞书通知发送失败" >> $LOG_FILE
    fi
else
    echo "[$DATE] openclaw 命令不可用，跳过飞书通知" >> $LOG_FILE
fi

echo "[$DATE] ================================" >> $LOG_FILE
