#!/usr/bin/env python3
"""
股票大盘数据抓取脚本
使用东方财富 API 获取 A股、港股、美股大盘指数
"""

import urllib.request
import json
import os
from datetime import datetime

def fetch_eastmoney_a_stock():
    """从东方财富获取A股大盘指数"""
    # 上证指数、深证成指、创业板指
    codes = ['1.000001', '0.399001', '0.399006']  # 1=上海, 0=深圳
    codes_str = ','.join(codes)
    
    url = f"https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f13,f14,f2,f3,f4,f128,f140&secids={codes_str}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://quote.eastmoney.com/',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = []
            if data.get('data') and data['data'].get('diff'):
                for item in data['data']['diff']:
                    # f14=名称, f2=最新价, f3=涨跌幅, f4=涨跌额
                    name = item.get('f14', '')
                    price = item.get('f2', 0)
                    change_pct = item.get('f3', 0)
                    change = item.get('f4', 0)
                    if name and price:
                        results.append({
                            'name': name,
                            'price': float(price) if price != '-' else 0,
                            'change': float(change) if change != '-' else 0,
                            'change_pct': float(change_pct) if change_pct != '-' else 0
                        })
            return results
    except Exception as e:
        print(f"获取A股数据失败: {e}")
        return []

def fetch_eastmoney_hk_stock():
    """从东方财富获取港股大盘指数"""
    # 恒生指数、恒生科技
    codes = ['100.HSI', '100.HSTECH']
    codes_str = ','.join(codes)
    
    url = f"https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f13,f14,f2,f3,f4&secids={codes_str}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://quote.eastmoney.com/',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = []
            if data.get('data') and data['data'].get('diff'):
                for item in data['data']['diff']:
                    name = item.get('f14', '')
                    price = item.get('f2', 0)
                    change_pct = item.get('f3', 0)
                    change = item.get('f4', 0)
                    if name and price:
                        results.append({
                            'name': name,
                            'price': float(price) if price != '-' else 0,
                            'change': float(change) if change != '-' else 0,
                            'change_pct': float(change_pct) if change_pct != '-' else 0
                        })
            return results
    except Exception as e:
        print(f"获取港股数据失败: {e}")
        return []

def fetch_eastmoney_us_stock():
    """从东方财富获取美股大盘指数"""
    # 道琼斯、纳斯达克、标普500
    codes = ['100.DJIA', '100.NDX', '100.SPX']
    codes_str = ','.join(codes)
    
    url = f"https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f13,f14,f2,f3,f4&secids={codes_str}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://quote.eastmoney.com/',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = []
            if data.get('data') and data['data'].get('diff'):
                for item in data['data']['diff']:
                    name_map = {'DJIA': '道琼斯', 'NDX': '纳斯达克', 'SPX': '标普500'}
                    code = item.get('f12', '')
                    name = name_map.get(code, item.get('f14', ''))
                    price = item.get('f2', 0)
                    change_pct = item.get('f3', 0)
                    change = item.get('f4', 0)
                    if name and price:
                        results.append({
                            'name': name,
                            'price': float(price) if price != '-' else 0,
                            'change': float(change) if change != '-' else 0,
                            'change_pct': float(change_pct) if change_pct != '-' else 0
                        })
            return results
    except Exception as e:
        print(f"获取美股数据失败: {e}")
        return []

def generate_markdown(a_shares, hk_shares, us_shares):
    """生成 Markdown 格式的报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    md = f"""# 📈 股票大盘数据 ({today})

> 数据更新时间: {now}

---

## 🇨🇳 A股大盘指数

| 指数名称 | 最新价 | 涨跌额 | 涨跌幅 |
|---------|--------|--------|--------|
"""
    for idx in a_shares:
        emoji = "📈" if idx['change'] >= 0 else "📉"
        md += f"| {emoji} {idx['name']} | {idx['price']:.2f} | {idx['change']:+.2f} | {idx['change_pct']:+.2f}% |\n"
    
    if not a_shares:
        md += "| 暂无数据 | - | - | - |\n"
    
    md += f"""
---

## 🇭🇰 港股大盘指数

| 指数名称 | 最新价 | 涨跌额 | 涨跌幅 |
|---------|--------|--------|--------|
"""
    for idx in hk_shares:
        emoji = "📈" if idx['change'] >= 0 else "📉"
        md += f"| {emoji} {idx['name']} | {idx['price']:.2f} | {idx['change']:+.2f} | {idx['change_pct']:+.2f}% |\n"
    
    if not hk_shares:
        md += "| 暂无数据 | - | - | - |\n"
    
    md += f"""
---

## 🇺🇸 美股大盘指数 (前一交易日)

| 指数名称 | 最新价 | 涨跌额 | 涨跌幅 |
|---------|--------|--------|--------|
"""
    for idx in us_shares:
        emoji = "📈" if idx['change'] >= 0 else "📉"
        md += f"| {emoji} {idx['name']} | {idx['price']:.2f} | {idx['change']:+.2f} | {idx['change_pct']:+.2f}% |\n"
    
    if not us_shares:
        md += "| 暂无数据 | - | - | - |\n"
    
    md += f"""
---

*数据仅供参考，不构成投资建议*
*股市有风险，投资需谨慎*
"""
    return md

def main():
    """主函数"""
    print("开始抓取股票数据...")
    print("数据来源: 东方财富")
    
    # 获取各类指数
    print("获取 A股指数...")
    a_shares = fetch_eastmoney_a_stock()
    
    print("获取 港股指数...")
    hk_shares = fetch_eastmoney_hk_stock()
    
    print("获取 美股指数...")
    us_shares = fetch_eastmoney_us_stock()
    
    # 生成 Markdown
    md_content = generate_markdown(a_shares, hk_shares, us_shares)
    
    # 保存到文件
    today = datetime.now().strftime('%Y-%m-%d')
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(workspace, 'memory', 'stock')
    output_file = os.path.join(output_dir, f'{today}.md')
    
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"数据已保存到: {output_file}")
    
    # 同时更新 latest.md
    latest_file = os.path.join(output_dir, 'latest.md')
    with open(latest_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # 输出抓取结果摘要
    total = len(a_shares) + len(hk_shares) + len(us_shares)
    print(f"✅ 成功获取 {total} 个指数数据")
    print(f"   A股: {len(a_shares)} 个")
    print(f"   港股: {len(hk_shares)} 个")
    print(f"   美股: {len(us_shares)} 个")
    
    return 0 if total > 0 else 1

if __name__ == '__main__':
    exit(main())
