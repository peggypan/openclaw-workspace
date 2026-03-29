#!/bin/bash
# 股票数据推送脚本

# 设置 PATH 确保能找到 openclaw（cron 环境不完整）
export PATH="/root/.nvm/versions/node/v22.22.0/bin:$PATH"
OPENCLAW_BIN="/root/.nvm/versions/node/v22.22.0/bin/openclaw"

CHAT_ID="oc_855010346c6dc7c60126df4470ec7972"
WORKSPACE="/root/.openclaw/workspace/agents/stock-expert"
DATE=$(date +%Y-%m-%d)
STOCK_FILE="$WORKSPACE/memory/stock/$DATE.md"

echo "准备推送股票数据..."
echo "聊天ID: $CHAT_ID"
echo "文件: $STOCK_FILE"

# 检查文件是否存在
if [ ! -f "$STOCK_FILE" ]; then
    echo "错误: 股票数据文件不存在"
    exit 1
fi

# 读取 Markdown 内容
CONTENT=$(cat "$STOCK_FILE")

# 发送消息到飞书
# 使用 openclaw 的 message 工具发送
$OPENCLAW_BIN message send \
    --channel feishu \
    --target "chat:$CHAT_ID" \
    --message "📈 每日大盘数据已更新 ($DATE)

$(echo "$CONTENT" | head -50)

详细数据请查看文件: memory/stock/$DATE.md"

echo "推送完成"
