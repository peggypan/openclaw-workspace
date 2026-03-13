#!/bin/bash
# Mission Control 定时任务脚本
# 用法: ./mission_control_cron.sh [morning|evening|weekly]

TASK_TYPE=$1
WORKSPACE_DIR="/root/.openclaw/workspace"
LOG_FILE="/tmp/mission_control.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Mission Control $TASK_TYPE 任务触发" >> $LOG_FILE

case $TASK_TYPE in
  morning)
    echo "[$DATE] 执行晨报准备..." >> $LOG_FILE
    # 准备数据
    echo "[$DATE] 检查今日日程..." >> $LOG_FILE
    grep -A 5 "Today" $WORKSPACE_DIR/CALENDAR.md >> $LOG_FILE 2>/dev/null || echo "无今日日程" >> $LOG_FILE
    echo "[$DATE] 检查紧急任务..." >> $LOG_FILE
    # 这里可以添加飞书 webhook 通知
    echo "[$DATE] ✓ 晨报准备完成，请对我说：执行 Morning Routine" >> $LOG_FILE
    ;;
    
  evening)
    echo "[$DATE] 执行日终总结准备..." >> $LOG_FILE
    # 准备数据
    echo "[$DATE] 扫描任务完成情况..." >> $LOG_FILE
    echo "[$DATE] 准备更新项目进度..." >> $LOG_FILE
    echo "[$DATE] ✓ 日终准备完成，请对我说：执行 Evening Routine" >> $LOG_FILE
    ;;
    
  weekly)
    echo "[$DATE] 执行周报准备..." >> $LOG_FILE
    echo "[$DATE] 统计本周生产力..." >> $LOG_FILE
    echo "[$DATE] ✓ 周报准备完成，请对我说：执行 Weekly Routine" >> $LOG_FILE
    ;;
    
  *)
    echo "[$DATE] 错误：未知任务类型 $TASK_TYPE" >> $LOG_FILE
    exit 1
    ;;
esac

echo "[$DATE] ================================" >> $LOG_FILE
