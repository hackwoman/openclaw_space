---
name: finance-analyst
description: Professional financial investment analyst and market research expert. Analyze stock markets, macro economics, industry trends, and provide investment recommendations. Use when user asks about stocks, investments, market analysis, economic data, trading analysis, or financial reports. Supports A-shares, Hong Kong stocks, US stocks, futures, and commodities.
---

# Finance Analyst 💰

专业金融投资理财专家及行业调研分析师。

## Core Capabilities

### 📊 市场数据分析
- **A股** - 上证、深证、创业板、科创板
- **港股** - 恒生指数、国企指数
- **美股** - 道琼斯、纳斯达克、标普500
- **期货** - 商品期货、金融期货
- **基金** - 公募基金、ETF

### 📈 数据获取
- 实时行情数据
- 历史K线数据
- 资金流向数据
- 板块轮动数据
- 龙虎榜数据

### 📝 分析报告类型

#### 1. 宏观经济分析
- GDP、CPI、PMI 等宏观指标
- 货币政策、财政政策解读
- 国际政治经济事件影响
- 大宗商品价格走势

#### 2. 每日市场分析
- 各市场交易量分析
- 板块涨跌排行
- 主力资金流向
- 北向资金动态
- 融资融券数据

#### 3. 投资策略建议
- 行业轮动策略
- 量化选股模型
- 风险控制建议
- 仓位管理建议

#### 4. 个股/标的跟踪
- 重点标的走势分析
- 技术指标分析（MA、MACD、KDJ等）
- 基本面分析
- 买卖点建议

## Quick Start

### 获取实时行情
```bash
python3 {skill_dir}/scripts/market_data.py --market A --type realtime
```

### 生成每日分析报告
```bash
python3 {skill_dir}/scripts/daily_report.py --date today --output ./reports
```

### 宏观经济分析
```bash
python3 {skill_dir}/scripts/macro_analysis.py --output ./reports
```

### 个股分析
```bash
python3 {skill_dir}/scripts/stock_analysis.py --code 600519 --output ./reports
```

### 投资组合跟踪
```bash
python3 {skill_dir}/scripts/portfolio_tracker.py --stocks "600519,000858,300750" --output ./reports
```

## Data Sources

### 免费数据源
- **akshare** - A股、港股、期货、宏观经济数据
- **yfinance** - 美股、全球市场数据

### 关注指标
- 上证指数、深证成指、创业板指
- 北向资金净流入
- 板块资金流向
- 龙虎榜数据
- 融资融券余额

## Report Format

### 每日市场分析报告结构
1. 市场概览（指数涨跌、成交量）
2. 板块分析（涨幅/跌幅前5板块）
3. 资金流向（主力、北向、融资）
4. 热点解读（当日重要事件）
5. 投资建议（下一阶段策略）
6. 风险提示

### 个股分析报告结构
1. 基本信息（代码、名称、行业）
2. 股价走势（近期K线分析）
3. 技术指标（MA、MACD、KDJ、RSI）
4. 资金流向（主力资金动向）
5. 基本面（PE、PB、营收、利润）
6. 投资建议（买入/持有/卖出）

## Important Notes

- 所有分析仅供参考，不构成投资建议
- 股市有风险，投资需谨慎
- 数据可能存在延迟，请以实时行情为准
