#!/usr/bin/env python3
"""Stock Analysis - 个股分析工具"""

import argparse
import json
import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False


def get_stock_info(code):
    """获取股票基本信息"""
    if not HAS_AKSHARE:
        return None
    
    try:
        # 获取个股信息
        df = ak.stock_individual_info_em(symbol=code)
        return df
    except Exception as e:
        print(f"⚠️ 获取股票信息失败: {e}")
        return None


def get_stock_history(code, days=90):
    """获取股票历史数据"""
    if not HAS_AKSHARE:
        return None
    
    try:
        df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
        if df is not None and len(df) > days:
            df = df.tail(days)
        return df
    except Exception as e:
        print(f"⚠️ 获取历史数据失败: {e}")
        return None


def calculate_ma(df, periods=[5, 10, 20, 60]):
    """计算均线"""
    for period in periods:
        df[f'MA{period}'] = df['收盘'].rolling(window=period).mean()
    return df


def calculate_macd(df, fast=12, slow=26, signal=9):
    """计算MACD"""
    exp1 = df['收盘'].ewm(span=fast, adjust=False).mean()
    exp2 = df['收盘'].ewm(span=slow, adjust=False).mean()
    df['DIF'] = exp1 - exp2
    df['DEA'] = df['DIF'].ewm(span=signal, adjust=False).mean()
    df['MACD'] = (df['DIF'] - df['DEA']) * 2
    return df


def calculate_kdj(df, n=9, m1=3, m2=3):
    """计算KDJ"""
    low_n = df['最低'].rolling(window=n).min()
    high_n = df['最高'].rolling(window=n).max()
    rsv = (df['收盘'] - low_n) / (high_n - low_n) * 100
    
    df['K'] = rsv.ewm(com=m1-1, adjust=False).mean()
    df['D'] = df['K'].ewm(com=m2-1, adjust=False).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    return df


def calculate_rsi(df, periods=[6, 12, 24]):
    """计算RSI"""
    for period in periods:
        delta = df['收盘'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df[f'RSI{period}'] = 100 - (100 / (1 + rs))
    return df


def analyze_technical(df):
    """技术分析"""
    if df is None or len(df) < 30:
        return {}
    
    # 计算技术指标
    df = calculate_ma(df)
    df = calculate_macd(df)
    df = calculate_kdj(df)
    df = calculate_rsi(df)
    
    latest = df.iloc[-1]
    
    analysis = {
        "current_price": round(latest['收盘'], 2),
        "ma_analysis": {},
        "macd_analysis": {},
        "kdj_analysis": {},
        "rsi_analysis": {},
    }
    
    # 均线分析
    for ma in ['MA5', 'MA10', 'MA20', 'MA60']:
        if ma in latest and not pd.isna(latest[ma]):
            price = latest['收盘']
            ma_val = latest[ma]
            position = "上方" if price > ma_val else "下方"
            analysis["ma_analysis"][ma] = {
                "value": round(ma_val, 2),
                "position": position,
                "distance": round((price - ma_val) / ma_val * 100, 2)
            }
    
    # MACD分析
    if 'DIF' in latest and 'DEA' in latest:
        dif = latest['DIF']
        dea = latest['DEA']
        macd = latest['MACD']
        
        if dif > dea and dif > 0:
            signal = "多头排列，强势"
        elif dif > dea and dif < 0:
            signal = "金叉，弱势反弹"
        elif dif < dea and dif < 0:
            signal = "空头排列，弱势"
        else:
            signal = "死叉，注意风险"
        
        analysis["macd_analysis"] = {
            "DIF": round(dif, 4),
            "DEA": round(dea, 4),
            "MACD": round(macd, 4),
            "signal": signal
        }
    
    # KDJ分析
    if 'K' in latest and 'D' in latest:
        k = latest['K']
        d = latest['D']
        j = latest['J']
        
        if k > 80:
            position = "超买区"
        elif k < 20:
            position = "超卖区"
        else:
            position = "正常区间"
        
        analysis["kdj_analysis"] = {
            "K": round(k, 2),
            "D": round(d, 2),
            "J": round(j, 2),
            "position": position
        }
    
    # RSI分析
    for rsi in ['RSI6', 'RSI12', 'RSI24']:
        if rsi in latest and not pd.isna(latest[rsi]):
            val = latest[rsi]
            if val > 70:
                status = "超买"
            elif val < 30:
                status = "超卖"
            else:
                status = "正常"
            analysis["rsi_analysis"][rsi] = {
                "value": round(val, 2),
                "status": status
            }
    
    return analysis


def get_fund_flow(code):
    """获取个股资金流向"""
    if not HAS_AKSHARE:
        return None
    
    try:
        df = ak.stock_individual_fund_flow(stock=code, market="sh" if code.startswith("6") else "sz")
        return df
    except:
        return None


def create_charts(df, code, name, output_dir):
    """创建分析图表"""
    if df is None or len(df) < 30:
        return
    
    df = calculate_ma(df)
    df = calculate_macd(df)
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # K线和均线
    ax1 = axes[0]
    ax1.plot(df['日期'], df['收盘'], 'k-', label='Close', linewidth=1.5)
    for ma in ['MA5', 'MA10', 'MA20']:
        if ma in df.columns:
            ax1.plot(df['日期'], df[ma], label=ma, linewidth=1)
    ax1.set_title(f'{name} ({code}) Price & MA', fontsize=12)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # 成交量
    ax2 = axes[1]
    colors = ['red' if df.iloc[i]['收盘'] >= df.iloc[i-1]['收盘'] else 'green' 
              for i in range(1, len(df))]
    colors.insert(0, 'green')
    ax2.bar(df['日期'], df['成交手数'], color=colors, alpha=0.7)
    ax2.set_title('Volume', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # MACD
    ax3 = axes[2]
    if 'DIF' in df.columns:
        ax3.plot(df['日期'], df['DIF'], 'b-', label='DIF', linewidth=1)
        ax3.plot(df['日期'], df['DEA'], 'r-', label='DEA', linewidth=1)
        ax3.bar(df['日期'], df['MACD'], color=['red' if v >= 0 else 'green' for v in df['MACD']], alpha=0.5)
        ax3.axhline(y=0, color='gray', linestyle='--')
        ax3.set_title('MACD', fontsize=12)
        ax3.legend(loc='upper left')
        ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{code}_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 分析图表已保存: {output_dir}/{code}_analysis.png")


def generate_stock_report(code, output_dir):
    """生成个股分析报告"""
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📊 个股分析: {code}")
    print("=" * 50)
    
    # 获取基本信息
    print("\n📋 获取基本信息...")
    info = get_stock_info(code)
    
    # 获取历史数据
    print("\n📈 获取历史数据...")
    df = get_stock_history(code, days=90)
    
    if df is None or len(df) == 0:
        print("❌ 无法获取股票数据")
        return
    
    # 获取股票名称
    name = "Unknown"
    if info is not None:
        for _, row in info.iterrows():
            if row.get('item') == '股票简称':
                name = row.get('value', 'Unknown')
    
    # 技术分析
    print("\n🔧 技术分析...")
    technical = analyze_technical(df)
    
    # 资金流向
    print("\n💰 获取资金流向...")
    fund_flow = get_fund_flow(code)
    
    # 创建图表
    print("\n📊 生成分析图表...")
    create_charts(df, code, name, output_dir)
    
    # 生成报告
    report = {
        "code": code,
        "name": name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "technical_analysis": technical,
        "latest_data": {
            "close": round(df.iloc[-1]['收盘'], 2),
            "high": round(df.iloc[-1]['最高'], 2),
            "low": round(df.iloc[-1]['最低'], 2),
            "volume": int(df.iloc[-1]['成交手数']),
        } if len(df) > 0 else {}
    }
    
    # 保存报告
    with open(f'{output_dir}/{code}_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n✅ 分析报告已保存: {output_dir}/{code}_report.json")
    
    # 生成文本报告
    generate_text_report(report, output_dir, code, name)
    
    return report


def generate_text_report(report, output_dir, code, name):
    """生成文本报告"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"📊 个股分析报告")
    lines.append(f"股票: {name} ({code})")
    lines.append(f"日期: {report['date']}")
    lines.append("=" * 60)
    
    # 最新数据
    lines.append("\n📈 最新行情")
    lines.append("-" * 40)
    data = report.get("latest_data", {})
    lines.append(f"收盘价: {data.get('close', 'N/A')}")
    lines.append(f"最高价: {data.get('high', 'N/A')}")
    lines.append(f"最低价: {data.get('low', 'N/A')}")
    lines.append(f"成交量: {data.get('volume', 'N/A')}")
    
    # 技术分析
    ta = report.get("technical_analysis", {})
    
    # 均线分析
    lines.append("\n📊 均线分析")
    lines.append("-" * 40)
    for ma, info in ta.get("ma_analysis", {}).items():
        lines.append(f"{ma}: {info['value']} (股价在均线{info['position']}, 距离{info['distance']:+.2f}%)")
    
    # MACD分析
    lines.append("\n📈 MACD分析")
    lines.append("-" * 40)
    macd = ta.get("macd_analysis", {})
    if macd:
        lines.append(f"DIF: {macd.get('DIF', 'N/A')}")
        lines.append(f"DEA: {macd.get('DEA', 'N/A')}")
        lines.append(f"MACD: {macd.get('MACD', 'N/A')}")
        lines.append(f"信号: {macd.get('signal', 'N/A')}")
    
    # KDJ分析
    lines.append("\n📉 KDJ分析")
    lines.append("-" * 40)
    kdj = ta.get("kdj_analysis", {})
    if kdj:
        lines.append(f"K: {kdj.get('K', 'N/A')}")
        lines.append(f"D: {kdj.get('D', 'N/A')}")
        lines.append(f"J: {kdj.get('J', 'N/A')}")
        lines.append(f"位置: {kdj.get('position', 'N/A')}")
    
    # 投资建议
    lines.append("\n💡 投资建议")
    lines.append("-" * 40)
    
    # 基于技术指标给出建议
    score = 0
    reasons = []
    
    # 均线分析
    price = ta.get("current_price", 0)
    for ma, info in ta.get("ma_analysis", {}).items():
        if info["position"] == "上方":
            score += 1
            reasons.append(f"股价在{ma}上方")
        else:
            score -= 1
            reasons.append(f"股价在{ma}下方")
    
    # MACD分析
    macd_signal = macd.get("signal", "")
    if "多头" in macd_signal or "金叉" in macd_signal:
        score += 2
        reasons.append(macd_signal)
    elif "空头" in macd_signal or "死叉" in macd_signal:
        score -= 2
        reasons.append(macd_signal)
    
    # KDJ分析
    if kdj.get("position") == "超卖":
        score += 2
        reasons.append("KDJ超卖，可能反弹")
    elif kdj.get("position") == "超买":
        score -= 2
        reasons.append("KDJ超买，注意风险")
    
    # 给出建议
    if score >= 3:
        suggestion = "建议关注/买入"
    elif score <= -3:
        suggestion = "建议谨慎/减持"
    else:
        suggestion = "建议持有观望"
    
    lines.append(f"综合评分: {score}")
    lines.append(f"建议: {suggestion}")
    lines.append("\n分析依据:")
    for r in reasons:
        lines.append(f"  • {r}")
    
    # 风险提示
    lines.append("\n⚠️ 风险提示")
    lines.append("-" * 40)
    lines.append("以上分析基于技术指标，仅供参考，不构成投资建议。")
    lines.append("股市有风险，投资需谨慎。")
    
    report_text = "\n".join(lines)
    
    with open(f'{output_dir}/{code}_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"✅ 文本报告已保存: {output_dir}/{code}_report.txt")
    
    print("\n" + report_text)


def main():
    parser = argparse.ArgumentParser(description="Stock Analysis Tool")
    parser.add_argument("--code", "-c", required=True, help="Stock code (e.g., 600519)")
    parser.add_argument("--output", "-o", default="./stock_reports", help="Output directory")
    
    args = parser.parse_args()
    
    generate_stock_report(args.code, args.output)
    
    print(f"\n🎉 分析完成！")


if __name__ == "__main__":
    main()
