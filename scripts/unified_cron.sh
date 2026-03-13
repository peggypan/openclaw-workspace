#!/bin/bash
# ============================================
# Unified Cron Tasks Manager
# 所有定时任务统一入口
# ============================================

TASK_TYPE=$1
LOG_FILE="/tmp/unified_cron.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] ========== Unified Cron: $TASK_TYPE ==========" >> $LOG_FILE

case $TASK_TYPE in
  # ============================================
  # Mission Control - 项目管理系统
  # ============================================
  mission-morning)
    echo "[$DATE] Mission Control - Morning Routine" >> $LOG_FILE
    cd /root/.openclaw/workspace && /usr/bin/python3 scripts/mission_control_cron.py morning >> $LOG_FILE 2>&1
    ;;
    
  mission-evening)
    echo "[$DATE] Mission Control - Evening Routine" >> $LOG_FILE
    cd /root/.openclaw/workspace && /usr/bin/python3 scripts/mission_control_cron.py evening >> $LOG_FILE 2>&1
    ;;
    
  mission-weekly)
    echo "[$DATE] Mission Control - Weekly Routine" >> $LOG_FILE
    cd /root/.openclaw/workspace && /usr/bin/python3 scripts/mission_control_cron.py weekly >> $LOG_FILE 2>&1
    ;;
    
  # ============================================
  # AI动态监控系统 (公众号管家)
  # ============================================
  ai-monitor)
    echo "[$DATE] AI Monitor - 公众号管家" >> $LOG_FILE
    cd /root/.openclaw/workspace/knowledge/公众号-想象X/agents/公众号管家 && \
      /usr/bin/python3 scripts/ai_monitor_v4.py >> /tmp/ai_monitor.log 2>&1 && \
      /usr/bin/python3 scripts/send_feishu_notify.py >> /tmp/ai_monitor.log 2>&1
    echo "[$DATE] AI Monitor 完成" >> $LOG_FILE
    ;;
    
  # ============================================
  # 代码自动同步
  # ============================================
  auto-sync)
    echo "[$DATE] Auto Sync - 代码同步" >> $LOG_FILE
    /root/yawen-workspace/scripts/auto-sync.sh >> $LOG_FILE 2>&1
    ;;
    
  # ============================================
  # 系统监控 (保留)
  # ============================================
  stargate)
    # 系统自带，不记录日志
    flock -xn /tmp/stargate.lock -c '/usr/local/qcloud/stargate/admin/start.sh > /dev/null 2>&1 &'
    ;;
    
  *)
    echo "[$DATE] 错误：未知任务类型 $TASK_TYPE" >> $LOG_FILE
    exit 1
    ;;
esac

echo "[$DATE] ========== 完成 ==========" >> $LOG_FILE
