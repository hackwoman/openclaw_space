#!/usr/bin/env python3
"""Daily Market Report - 每日市场分析报告生成器"""

import argparse
import json
import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False


def get_market_overview():
    """获取市场概览"""
    overview = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "indices": [],
        "summary": ""
    }
    
    if not HAS_AKSHARE:
        return overview
    
    try:
        # 主要指数
        indices_map = {
            "上证指数": "sh000001",
            "深证成指": "sz399001",
            "创业板指": "sz399006",
            "沪深300": "sh000300",
            "科创50": "sh000688",
        }
        
        for name, code in indices_map.items():
            try:
                df = ak.stock_zh_index_daily_em(symbol=code)
                if df is not None and len(df) >= 2:
                    latest = df.iloc[-1]
                    prev = df.iloc[-2]
                    change = (latest["close"] - prev["close"]) / prev["close"] * 100
                    overview["indices"].append({
                        "name": name,
                        "close": round(latest["close"], 2),
                        "change": round(change, 2),
                        "volume": latest.get("volume", 0),
                    })
            except:
                pass
    except Exception as e:
        print(f"⚠️ 获取市场概览失败: {e}")
    
    return overview


def get_sector_performance():
    """获取板块表现"""
    if not HAS_AKSHARE:
        return [], []
    
    try:
        df = ak.stock_board_industry_name_em()
        if df is not None:
            # 按涨跌幅排序
            df_sorted = df.sort_values("涨跌幅", ascending=False)
            top5 = df_sorted.head(5)[["板块名称", "涨跌幅"]].to_dict("records")
            bottom5 = df_sorted.tail(5)[["板块名称", "涨跌幅"]].to_dict("records")
            return top5, bottom5
    except Exception as e:
        print(f"⚠️ 获取板块数据失败: {e}")
    
    return [], []


def get_fund_flow():
    """获取资金流向"""
    if not HAS_AKSHARE:
        return {}
    
    try:
        # 主力资金流向
        df = ak.stock_individual_fund_flow_rank(indicator="今日")
        if df is not None:
            # 计算净流入前10
            df_sorted = df.sort_values("主力净流入-净额", ascending=False)
            top10 = df_sorted.head(10)[["代码", "名称", "主力净流入-净额"]].to_dict("records")
            return {"top主力净流入": top10}
    except Exception as e:
        print(f"⚠️ 获取资金流向失败: {e}")
    
    return {}


def get_north_fund_flow():
    """获取北向资金"""
    if not HAS_AKSHARE:
        return None
    
    try:
        df = ak.stock_hsgt_north_net_flow_in_em(symbol="北向")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            return {
                "date": str(latest.get("date", "")),
                "net_flow": latest.get("value", 0),
            }
    except Exception as e:
        print(f"⚠️ 获取北向资金失败: {e}")
    
    return None


def create_charts(output_dir):
    """创建分析图表"""
    if not HAS_AKSHARE:
        return
    
    try:
        # 上证指数近30日走势
        df = ak.stock_zh_index_daily_em(symbol="sh000001")
        if df is not None and len(df) > 30:
            df = df.tail(30)
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # K线图
            ax1.plot(df["date"], df["close"], 'b-', linewidth=2)
            ax1.fill_between(df["date"], df["close"], alpha=0.3)
            ax1.set_title('Shanghai Index - 30 Day Trend', fontsize=14)
            ax1.set_ylabel('Index')
            ax1.grid(True, alpha=0.3)
            
            # 成交量
            ax2.bar(df["date"], df["volume"], color='steelblue', alpha=0.7)
            ax2.set_title('Volume', fontsize=14)
            ax2.set_ylabel('Volume')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(f'{output_dir}/index_trend.png', dpi=150, bbox_inches='tight')
            plt.close()
            print(f"✅ 走势图已保存: {output_dir}/index_trend.png")
            
    except Exception as e:
        print(f"⚠️ 创建图表失败: {e}")


def generate_report(output_dir):
    """生成完整报告"""
    os.makedirs(output_dir, exist_ok=True)
    
    print("📊 生成每日市场分析报告")
    print("=" * 50)
    
    report = {
        "title": f"每日市场分析报告",
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "sections": []
    }
    
    # 1. 市场概览
    print("\n📈 获取市场概览...")
    overview = get_market_overview()
    report["overview"] = overview
    
    # 2. 板块分析
    print("\n📊 获取板块分析...")
    top_sectors, bottom_sectors = get_sector_performance()
    report["top_sectors"] = top_sectors
    report["bottom_sectors"] = bottom_sectors
    
    # 3. 资金流向
    print("\n💰 获取资金流向...")
    fund_flow = get_fund_flow()
    report["fund_flow"] = fund_flow
    
    # 4. 北向资金
    print("\n🌐 获取北向资金...")
    north_flow = get_north_fund_flow()
    report["north_flow"] = north_flow
    
    # 5. 创建图表
    print("\n📊 生成分析图表...")
    create_charts(output_dir)
    
    # 保存报告数据
    with open(f'{output_dir}/report_data.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n✅ 报告数据已保存: {output_dir}/report_data.json")
    
    # 生成文本报告
    generate_text_report(report, output_dir)
    
    return report


def generate_text_report(report, output_dir):
    """生成文本报告"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"📊 每日市场分析报告")
    lines.append(f"📅 {report['date']}")
    lines.append("=" * 60)
    
    # 市场概览
    lines.append("\n📈 一、市场概览")
    lines.append("-" * 40)
    if "indices" in report.get("overview", {}):
        for idx in report["overview"]["indices"]:
            emoji = "🔴" if idx["change"] < 0 else "🟢"
            lines.append(f"{emoji} {idx['name']}: {idx['close']} ({idx['change']:+.2f}%)")
    
    # 板块分析
    lines.append("\n📊 二、板块分析")
    lines.append("-" * 40)
    lines.append("涨幅前5:")
    for s in report.get("top_sectors", []):
        lines.append(f"  🟢 {s.get('板块名称', 'N/A')}: {s.get('涨跌幅', 0):+.2f}%")
    
    lines.append("\n跌幅前5:")
    for s in report.get("bottom_sectors", []):
        lines.append(f"  🔴 {s.get('板块名称', 'N/A')}: {s.get('涨跌幅', 0):+.2f}%")
    
    # 北向资金
    lines.append("\n🌐 三、北向资金")
    lines.append("-" * 40)
    north = report.get("north_flow")
    if north:
        flow = north.get("net_flow", 0)
        direction = "净流入" if flow > 0 else "净流出"
        lines.append(f"北向资金{direction}: {abs(flow):.2f}亿元")
    else:
        lines.append("暂无数据")
    
    # 投资建议
    lines.append("\n💡 四、投资建议")
    lines.append("-" * 40)
    lines.append("基于今日市场表现，建议：")
    lines.append("1. 关注政策面变化，把握结构性机会")
    lines.append("2. 控制仓位，注意风险管理")
    lines.append("3. 关注北向资金流向，把握外资偏好")
    
    # 风险提示
    lines.append("\n⚠️ 风险提示")
    lines.append("-" * 40)
    lines.append("以上分析仅供参考，不构成投资建议。")
    lines.append("股市有风险，投资需谨慎。")
    
    report_text = "\n".join(lines)
    
    with open(f'{output_dir}/daily_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"✅ 文本报告已保存: {output_dir}/daily_report.txt")
    
    print("\n" + report_text)


def main():
    parser = argparse.ArgumentParser(description="Daily Market Report Generator")
    parser.add_argument("--date", "-d", default="today", help="Report date (today/yesterday)")
    parser.add_argument("--output", "-o", default="./reports", help="Output directory")
    
    args = parser.parse_args()
    
    date_str = datetime.now().strftime("%Y%m%d")
    output_dir = f"{args.output}/{date_str}"
    
    generate_report(output_dir)
    
    print(f"\n🎉 报告生成完成！文件保存在: {output_dir}")


if __name__ == "__main__":
    main()
