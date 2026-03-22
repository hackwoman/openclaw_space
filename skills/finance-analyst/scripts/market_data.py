#!/usr/bin/env python3
"""Market Data Fetcher - 获取股票、指数、期货等市场数据"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import numpy as np

try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False
    print("⚠️ akshare not installed, some features unavailable")

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False


def get_a_stock_realtime():
    """获取A股实时行情"""
    if not HAS_AKSHARE:
        print("❌ 需要安装 akshare")
        return None
    
    try:
        # 获取实时行情
        df = ak.stock_zh_a_spot_em()
        return df
    except Exception as e:
        print(f"❌ 获取A股行情失败: {e}")
        return None


def get_index_realtime():
    """获取主要指数实时数据"""
    if not HAS_AKSHARE:
        return None
    
    try:
        indices = {
            "上证指数": "sh000001",
            "深证成指": "sz399001",
            "创业板指": "sz399006",
            "科创50": "sh000688",
            "沪深300": "sh000300",
            "中证500": "sh000905",
        }
        
        results = []
        for name, code in indices.items():
            try:
                df = ak.stock_zh_index_daily_em(symbol=code)
                if df is not None and len(df) > 0:
                    latest = df.iloc[-1]
                    results.append({
                        "名称": name,
                        "代码": code,
                        "最新价": latest.get("close", "N/A"),
                        "日期": latest.get("date", "N/A"),
                    })
            except:
                pass
        
        return pd.DataFrame(results)
    except Exception as e:
        print(f"❌ 获取指数数据失败: {e}")
        return None


def get_sector_funds():
    """获取板块资金流向"""
    if not HAS_AKSHARE:
        return None
    
    try:
        # 行业板块资金流向
        df = ak.stock_sector_fund_flow_rank(indicator="今日")
        return df
    except Exception as e:
        print(f"❌ 获取板块资金流向失败: {e}")
        return None


def get_north_funds():
    """获取北向资金数据"""
    if not HAS_AKSHARE:
        return None
    
    try:
        df = ak.stock_hsgt_north_net_flow_in_em(symbol="北向")
        return df
    except Exception as e:
        print(f"❌ 获取北向资金失败: {e}")
        return None


def get_us_stock(symbol):
    """获取美股数据"""
    if not HAS_YFINANCE:
        print("❌ 需要安装 yfinance")
        return None
    
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")
        return hist
    except Exception as e:
        print(f"❌ 获取美股数据失败: {e}")
        return None


def get_hk_stock_realtime():
    """获取港股实时数据"""
    if not HAS_AKSHARE:
        return None
    
    try:
        df = ak.stock_hk_spot_em()
        return df
    except Exception as e:
        print(f"❌ 获取港股数据失败: {e}")
        return None


def get_macro_data():
    """获取宏观经济数据"""
    if not HAS_AKSHARE:
        return None
    
    try:
        # GDP数据
        gdp = ak.macro_china_gdp_yearly()
        # CPI数据
        cpi = ak.macro_china_cpi_monthly()
        # PMI数据
        pmi = ak.macro_china_pmi()
        
        return {
            "gdp": gdp.tail(5) if gdp is not None else None,
            "cpi": cpi.tail(12) if cpi is not None else None,
            "pmi": pmi.tail(12) if pmi is not None else None,
        }
    except Exception as e:
        print(f"❌ 获取宏观数据失败: {e}")
        return None


def get_dragon_tiger_list():
    """获取龙虎榜数据"""
    if not HAS_AKSHARE:
        return None
    
    try:
        df = ak.stock_lhb_detail_em()
        return df
    except Exception as e:
        print(f"❌ 获取龙虎榜数据失败: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Market Data Fetcher")
    parser.add_argument("--market", "-m", choices=["A", "HK", "US", "all"], default="A", help="Market type")
    parser.add_argument("--type", "-t", choices=["realtime", "index", "sector", "north", "macro", "dragon"], default="realtime", help="Data type")
    parser.add_argument("--symbol", "-s", help="Stock symbol (for US stocks)")
    parser.add_argument("--output", "-o", default="./market_data", help="Output directory")
    
    args = parser.parse_args()
    
    os.makedirs(args.output, exist_ok=True)
    
    print("📊 市场数据获取工具")
    print("=" * 50)
    
    if args.market == "A" or args.market == "all":
        if args.type == "realtime" or args.type == "all":
            print("\n📈 获取A股实时行情...")
            df = get_a_stock_realtime()
            if df is not None:
                df.to_csv(f"{args.output}/a_stock_realtime.csv", index=False)
                print(f"✅ A股行情已保存: {args.output}/a_stock_realtime.csv")
        
        if args.type == "index" or args.type == "all":
            print("\n📊 获取指数数据...")
            df = get_index_realtime()
            if df is not None:
                df.to_csv(f"{args.output}/index_realtime.csv", index=False)
                print(f"✅ 指数数据已保存: {args.output}/index_realtime.csv")
        
        if args.type == "sector" or args.type == "all":
            print("\n💰 获取板块资金流向...")
            df = get_sector_funds()
            if df is not None:
                df.to_csv(f"{args.output}/sector_funds.csv", index=False)
                print(f"✅ 板块资金流向已保存: {args.output}/sector_funds.csv")
        
        if args.type == "north" or args.type == "all":
            print("\n🌐 获取北向资金...")
            df = get_north_funds()
            if df is not None:
                df.to_csv(f"{args.output}/north_funds.csv", index=False)
                print(f"✅ 北向资金数据已保存: {args.output}/north_funds.csv")
        
        if args.type == "macro" or args.type == "all":
            print("\n🏛️ 获取宏观经济数据...")
            data = get_macro_data()
            if data:
                for key, df in data.items():
                    if df is not None:
                        df.to_csv(f"{args.output}/macro_{key}.csv", index=False)
                        print(f"✅ {key.upper()} 数据已保存: {args.output}/macro_{key}.csv")
        
        if args.type == "dragon" or args.type == "all":
            print("\n🐉 获取龙虎榜数据...")
            df = get_dragon_tiger_list()
            if df is not None:
                df.to_csv(f"{args.output}/dragon_tiger.csv", index=False)
                print(f"✅ 龙虎榜数据已保存: {args.output}/dragon_tiger.csv")
    
    if args.market == "HK" or args.market == "all":
        print("\n🇭🇰 获取港股数据...")
        df = get_hk_stock_realtime()
        if df is not None:
            df.to_csv(f"{args.output}/hk_stock.csv", index=False)
            print(f"✅ 港股数据已保存: {args.output}/hk_stock.csv")
    
    if args.market == "US" and args.symbol:
        print(f"\n🇺🇸 获取美股 {args.symbol} 数据...")
        df = get_us_stock(args.symbol)
        if df is not None:
            df.to_csv(f"{args.output}/us_{args.symbol}.csv")
            print(f"✅ 美股数据已保存: {args.output}/us_{args.symbol}.csv")
    
    print("\n🎉 数据获取完成！")


if __name__ == "__main__":
    main()
