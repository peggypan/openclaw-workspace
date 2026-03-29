# HEARTBEAT.md - 股票专家定时任务

## 每日股票数据抓取与推送任务

每天早上 9:30 后自动执行一次股票数据抓取并推送到飞书

```bash
#!/bin/bash
# 获取今天的日期
TODAY=$(date +%Y-%m-%d)
WORKSPACE="/root/.openclaw/workspace/agents/stock-expert"
STOCK_DIR="$WORKSPACE/memory/stock"
LOCK_FILE="$STOCK_DIR/.last_run"
CHAT_ID="oc_855010346c6dc7c60126df4470ec7972"

# 检查今天是否已经执行过
if [ -f "$LOCK_FILE" ]; then
    LAST_RUN=$(cat "$LOCK_FILE")
    if [ "$LAST_RUN" = "$TODAY" ]; then
        # 今天已经执行过，静默退出
        exit 0
    fi
fi

# 检查当前时间是否在 09:00 之后（A股开盘前）
HOUR=$(date +%H)
if [ $HOUR -lt 9 ]; then
    # 还未到执行时间
    exit 0
fi

# 执行数据抓取
cd "$WORKSPACE"
python3 "$WORKSPACE/scripts/stock_fetcher.py"
FETCH_RESULT=$?

# 检查执行结果
if [ $FETCH_RESULT -eq 0 ]; then
    # 记录今天已执行
    echo "$TODAY" > "$LOCK_FILE"
    
    # 发送飞书通知
    STOCK_FILE="$STOCK_DIR/$TODAY.md"
    if [ -f "$STOCK_FILE" ]; then
        # 提取关键数据生成摘要
        echo "📈 每日大盘数据已更新 ($TODAY)"
        echo ""
        echo "📁 详细数据: memory/stock/$TODAY.md"
        echo ""
        echo "---"
        # 输出 markdown 内容给 OpenClaw 处理
        cat "$STOCK_FILE"
    fi
else
    echo "⚠️ 股票数据抓取失败，请检查日志"
fi
```
