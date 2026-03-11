#!/bin/bash
# 每日早报生成脚本
# 生成商业、AI、机器人、教育、政治5大领域资讯

CHANNEL="feishu"
TARGET="chat:oc_18507e9893d11a18f9068eb439322f68"

echo "📰 【每日早报】$(date '+%Y年%m月%d日')"
echo ""
echo "为您汇总前一日重要资讯："
echo ""

# 使用web_search获取各领域最新资讯
echo "正在收集各领域资讯..."

# 这里会通过subagent调用搜索并生成早报内容
openclaw sessions spawn \
  --runtime subagent \
  --mode run \
  --agent business-analyst \
  --task "生成今日早报并推送到飞书群聊chat:oc_18507e9893d11a18f9068eb439322f68"
