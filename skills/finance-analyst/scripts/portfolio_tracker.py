#!/usr/bin/env python3
"""Portfolio Tracker - 投资组合跟踪工具"""

import argparse
import json
import os
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial']

try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False


def get_stock_realtime(code):
    """获取股票实时数据"""
    if not HAS_AKSHARE:
        return None
    
    try:
        df = ak.stock_zh_a_spot_em()
        if df is not None:
            stock = df[df['代码'] == code]
            if len(stock) > 0:
                return stock.iloc[0].to_dict()
    except:
        pass
    
    return None


def get_stock_history(code, days=30):
    """获取历史数据"""
    if not HAS_AKSHARE:
        return None
    
    try:
        df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
        if df is not None and len(df) > days:
            df = df.tail(days)
        return df
    except:
        return None


def calculate_portfolio_stats(portfolio_data):
    """计算组合统计"""
    stats = {
        "total_market_value": 0,
        "total_cost": 0,
        "total_profit": 0,
        "total_profit_pct": 0,
        "stocks": []
    }
    
    for stock in portfolio_data:
        market_value = stock["current_price"] * stock["shares"]
        cost = stock["cost_price"] * stock["shares"]
        profit = market_value - cost
        profit_pct = (stock["current_price"] - stock["cost_price"]) / stock["cost_price"] * 100
        
        stats["total_market_value"] += market_value
        stats["total_cost"] += cost
        stats["total_profit"] += profit
        
        stats["stocks"].append({
            "code": stock["code"],
            "name": stock["name"],
            "shares": stock["shares"],
            "cost_price": stock["cost_price"],
            "current_price": stock["current_price"],
            "market_value": round(market_value, 2),
            "profit": round(profit, 2),
            "profit_pct": round(profit_pct, 2),
        })
    
    stats["total_market_value"] = round(stats["total_market_value"], 2)
    stats["total_cost"] = round(stats["total_cost"], 2)
    stats["total_profit"] = round(stats["total_profit"], 2)
    stats["total_profit_pct"] = round(
        (stats["total_market_value"] - stats["total_cost"]) / stats["total_cost"] * 100, 2
    )
    
    return stats


def create_portfolio_charts(portfolio_data, output_dir):
    """创建组合分析图表"""
    if not portfolio_data:
        return
    
    # 饼图：持仓分布
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    labels = [f"{s['name']}" for s in portfolio_data]
    values = [s["current_price"] * s["shares"] for s in portfolio_data]
    profits = [s.get("profit", 0) for s in portfolio_data]
    colors = ['#ff6b6b' if p < 0 else '#00b894' for p in profits]
    
    # 持仓市值分布
    ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Portfolio Distribution')
    
    # 盈亏分布
    bars = ax2.bar(labels, profits, color=colors)
    ax2.axhline(y=0, color='gray', linestyle='--')
    ax2.set_title('Profit/Loss by Stock')
    ax2.set_ylabel('Profit/Loss')
    
    # 添加数值标签
    for bar, val in zip(bars, profits):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{val:.2f}', ha='center', va='bottom' if val >= 0 else 'top')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/portfolio_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 组合分析图已保存: {output_dir}/portfolio_analysis.png")


def generate_portfolio_report(stocks_input, output_dir, portfolio_name="My Portfolio"):
    """生成组合分析报告"""
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📊 投资组合分析: {portfolio_name}")
    print("=" * 50)
    
    # 解析输入的股票列表
    portfolio_data = []
    
    for item in stocks_input:
        parts = item.split(",")
        code = parts[0]
        shares = int(parts[1]) if len(parts) > 1 else 100
        cost_price = float(parts[2]) if len(parts) > 2 else None
        
        print(f"\n📈 获取 {code} 数据...")
        realtime = get_stock_realtime(code)
        
        if realtime:
            name = realtime.get("名称", code)
            current_price = float(realtime.get("最新价", 0))
            
            # 如果没有提供成本价，使用当前价格
            if cost_price is None:
                cost_price = current_price
            
            portfolio_data.append({
                "code": code,
                "name": name,
                "shares": shares,
                "cost_price": cost_price,
                "current_price": current_price,
            })
        else:
            print(f"⚠️ 无法获取 {code} 数据")
    
    if not portfolio_data:
        print("❌ 没有有效的股票数据")
        return
    
    # 计算组合统计
    stats = calculate_portfolio_stats(portfolio_data)
    
    # 创建图表
    create_portfolio_charts(stats["stocks"], output_dir)
    
    # 生成报告
    report = {
        "portfolio_name": portfolio_name,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "stats": stats,
    }
    
    with open(f'{output_dir}/portfolio_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 报告数据已保存: {output_dir}/portfolio_report.json")
    
    # 生成文本报告
    generate_text_report(report, output_dir)
    
    return report


def generate_text_report(report, output_dir):
    """生成文本报告"""
    stats = report["stats"]
    
    lines = []
    lines.append("=" * 60)
    lines.append(f"📊 投资组合分析报告")
    lines.append(f"组合名称: {report['portfolio_name']}")
    lines.append(f"日期: {report['date']}")
    lines.append("=" * 60)
    
    # 组合概览
    lines.append("\n💰 组合概览")
    lines.append("-" * 40)
    lines.append(f"总市值: {stats['total_market_value']:,.2f} 元")
    lines.append(f"总成本: {stats['total_cost']:,.2f} 元")
    
    profit_emoji = "🟢" if stats['total_profit'] >= 0 else "🔴"
    lines.append(f"{profit_emoji} 总盈亏: {stats['total_profit']:,.2f} 元 ({stats['total_profit_pct']:+.2f}%)")
    
    # 持仓明细
    lines.append("\n📋 持仓明细")
    lines.append("-" * 40)
    lines.append(f"{'股票':<10} {'持仓':>8} {'成本':>10} {'现价':>10} {'市值':>12} {'盈亏':>12} {'盈亏%':>8}")
    lines.append("-" * 70)
    
    for s in stats["stocks"]:
        emoji = "🟢" if s['profit'] >= 0 else "🔴"
        lines.append(
            f"{s['name']:<10} {s['shares']:>8} {s['cost_price']:>10.2f} "
            f"{s['current_price']:>10.2f} {s['market_value']:>12.2f} "
            f"{emoji}{s['profit']:>11.2f} {s['profit_pct']:>+7.2f}%"
        )
    
    # 投资建议
    lines.append("\n💡 投资建议")
    lines.append("-" * 40)
    
    # 分析持仓
    profitable = [s for s in stats["stocks"] if s["profit"] > 0]
    losing = [s for s in stats["stocks"] if s["profit"] < 0]
    
    if stats["total_profit_pct"] > 10:
        lines.append("📈 组合盈利良好，可考虑部分止盈")
    elif stats["total_profit_pct"] < -10:
        lines.append("⚠️ 组合亏损较大，建议审视持仓逻辑")
    
    if len(losing) > len(profitable):
        lines.append("📉 多数持仓亏损，建议关注止损")
    
    if profitable:
        best = max(profitable, key=lambda x: x["profit_pct"])
        lines.append(f"🏆 最佳持仓: {best['name']} ({best['profit_pct']:+.2f}%)")
    
    if losing:
        worst = min(losing, key=lambda x: x["profit_pct"])
        lines.append(f"⚠️ 最差持仓: {worst['name']} ({worst['profit_pct']:+.2f}%)")
    
    # 风险提示
    lines.append("\n⚠️ 风险提示")
    lines.append("-" * 40)
    lines.append("以上分析仅供参考，不构成投资建议。")
    lines.append("股市有风险，投资需谨慎。")
    
    report_text = "\n".join(lines)
    
    with open(f'{output_dir}/portfolio_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"✅ 文本报告已保存: {output_dir}/portfolio_report.txt")
    
    print("\n" + report_text)


def main():
    parser = argparse.ArgumentParser(description="Portfolio Tracker")
    parser.add_argument("--stocks", "-s", required=True, 
                       help="Stock list (format: code,shares,cost_price; separated by semicolon)")
    parser.add_argument("--name", "-n", default="My Portfolio", help="Portfolio name")
    parser.add_argument("--output", "-o", default="./portfolio_reports", help="Output directory")
    
    args = parser.parse_args()
    
    stocks_input = args.stocks.split(";")
    
    generate_portfolio_report(stocks_input, args.output, args.name)
    
    print(f"\n🎉 分析完成！")


if __name__ == "__main__":
    main()
