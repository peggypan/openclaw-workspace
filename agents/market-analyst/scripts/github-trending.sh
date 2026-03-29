#!/bin/bash
# GitHub Trending Scraper Script
# 获取 GitHub 每日 Trending 项目

OUTPUT_FILE="/root/.openclaw/workspace/agents/market-analyst/memory/github-trending-$(date +%Y-%m-%d).md"
DATE=$(date +"%Y-%m-%d")

echo "# GitHub Trending - $DATE" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "_自动抓取于 $(date)_" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## 今日热门项目 (按 Star 增长排序)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "数据已准备，请使用 Camoufox 浏览器抓取 GitHub Trending 页面"
