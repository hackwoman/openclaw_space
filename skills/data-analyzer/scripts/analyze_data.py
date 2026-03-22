#!/usr/bin/env python3
"""Data Analysis Toolkit - Excel, CSV, JSON analysis with visualizations."""

import argparse
import os
import sys
import json
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']


def load_data(input_file):
    """Load data from various formats."""
    ext = Path(input_file).suffix.lower()
    
    if ext == '.csv':
        return pd.read_csv(input_file)
    elif ext == '.xlsx':
        return pd.read_excel(input_file)
    elif ext == '.xls':
        return pd.read_excel(input_file, engine='xlrd')
    elif ext == '.json':
        return pd.read_json(input_file)
    elif ext == '.tsv':
        return pd.read_csv(input_file, sep='\t')
    else:
        raise ValueError(f"Unsupported format: {ext}")


def basic_info(df, output_dir):
    """Generate basic data information."""
    info = {
        "shape": list(df.shape),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "missing_percent": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
    }
    
    # Numerical summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        info["numerical_summary"] = df[numeric_cols].describe().to_dict()
    
    # Categorical summary
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        info["categorical_summary"] = {}
        for col in cat_cols:
            info["categorical_summary"][col] = {
                "unique": int(df[col].nunique()),
                "top_values": df[col].value_counts().head(5).to_dict()
            }
    
    # Save info
    with open(f'{output_dir}/data_info.json', 'w') as f:
        json.dump(info, f, indent=2, default=str)
    
    print(f"✅ 数据基本信息已保存: data_info.json")
    return info


def plot_distributions(df, output_dir):
    """Plot distributions for numerical columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        print("⚠️ 无数值列，跳过分布图")
        return
    
    n_cols = min(3, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
    if n_rows * n_cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    for idx, col in enumerate(numeric_cols):
        if idx < len(axes):
            sns.histplot(df[col].dropna(), kde=True, ax=axes[idx], color='#4a90d9')
            axes[idx].set_title(f'{col} 分布', fontsize=12)
            axes[idx].set_xlabel('')
    
    # Hide empty subplots
    for idx in range(len(numeric_cols), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/distributions.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 分布图已保存: distributions.png")


def plot_correlation_heatmap(df, output_dir):
    """Plot correlation heatmap."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        print("⚠️ 数值列不足，跳过相关性热力图")
        return
    
    corr = df[numeric_cols].corr()
    
    plt.figure(figsize=(max(10, len(numeric_cols)*0.8), max(8, len(numeric_cols)*0.6)))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', 
                cmap='RdBu_r', center=0, square=True,
                linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('相关性热力图', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/correlation_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 相关性热力图已保存: correlation_heatmap.png")


def plot_boxplots(df, output_dir):
    """Plot box plots for outlier detection."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        return
    
    n_cols = min(3, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
    if n_rows * n_cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    for idx, col in enumerate(numeric_cols):
        if idx < len(axes):
            sns.boxplot(y=df[col].dropna(), ax=axes[idx], color='#00cec9')
            axes[idx].set_title(f'{col} 箱线图', fontsize=12)
    
    for idx in range(len(numeric_cols), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/boxplots.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 箱线图已保存: boxplots.png")


def plot_categorical(df, output_dir):
    """Plot categorical columns."""
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    
    if len(cat_cols) == 0:
        return
    
    for col in cat_cols[:5]:  # Max 5 categorical columns
        value_counts = df[col].value_counts().head(10)
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(range(len(value_counts)), value_counts.values, color='#a29bfe')
        plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
        plt.title(f'{col} 分布', fontsize=14, fontweight='bold')
        plt.ylabel('数量')
        
        # Add value labels
        for bar, val in zip(bars, value_counts.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(val), ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        safe_col_name = col.replace(' ', '_').replace('/', '_')
        plt.savefig(f'{output_dir}/categorical_{safe_col_name}.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✅ 分类图已保存: categorical_{safe_col_name}.png")


def plot_scatter_matrix(df, output_dir):
    """Plot scatter matrix for numeric columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        return
    
    # Use max 5 columns for readability
    cols_to_plot = numeric_cols[:5]
    
    fig = plt.figure(figsize=(12, 10))
    pd.plotting.scatter_matrix(df[cols_to_plot], alpha=0.5, 
                               figsize=(12, 10), diagonal='hist')
    plt.suptitle('散点矩阵图', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/scatter_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 散点矩阵图已保存: scatter_matrix.png")


def generate_html_report(df, info, output_dir):
    """Generate HTML report."""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 数据分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #333; margin-bottom: 10px; }}
        h2 {{ color: #4a90d9; margin: 30px 0 15px; border-bottom: 2px solid #4a90d9; padding-bottom: 10px; }}
        .summary {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .stat-value {{ font-size: 2em; font-weight: bold; }}
        .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #4a90d9; color: white; font-weight: 600; }}
        tr:hover {{ background: #f8f9fa; }}
        .chart {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .chart img {{ max-width: 100%; height: auto; }}
        .chart-title {{ font-size: 1.2em; font-weight: bold; color: #333; margin-bottom: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 数据分析报告</h1>
        <p style="color: #666; margin-bottom: 20px;">生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <h2>📋 数据概览</h2>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-value">{info['shape'][0]}</div>
                    <div class="stat-label">行数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{info['shape'][1]}</div>
                    <div class="stat-label">列数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{sum(info['missing_values'].values())}</div>
                    <div class="stat-label">缺失值</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(df.select_dtypes(include=[np.number]).columns)}</div>
                    <div class="stat-label">数值列</div>
                </div>
            </div>
        </div>
        
        <div class="summary">
            <h2>📝 列信息</h2>
            <table>
                <tr><th>列名</th><th>类型</th><th>非空数</th><th>缺失数</th><th>缺失率</th></tr>
"""
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        missing = df[col].isna().sum()
        missing_pct = f"{missing/len(df)*100:.1f}%"
        html += f"                <tr><td>{col}</td><td>{dtype}</td><td>{non_null}</td><td>{missing}</td><td>{missing_pct}</td></tr>\n"
    
    html += """            </table>
        </div>
        
"""
    
    # Add charts if they exist
    charts = [
        ('distributions.png', '📈 数值分布图'),
        ('correlation_heatmap.png', '🔥 相关性热力图'),
        ('boxplots.png', '📦 箱线图（异常值检测）'),
        ('scatter_matrix.png', '🔵 散点矩阵图'),
    ]
    
    for filename, title in charts:
        filepath = f'{output_dir}/{filename}'
        if os.path.exists(filepath):
            html += f"""        <div class="chart">
            <div class="chart-title">{title}</div>
            <img src="{filename}" alt="{title}">
        </div>
"""
    
    # Add data preview
    html += f"""
        <div class="summary">
            <h2>👀 数据预览（前10行）</h2>
            {df.head(10).to_html(classes='', index=False)}
        </div>
        
        <div class="summary">
            <h2>📊 统计摘要</h2>
            {df.describe().to_html(classes='', index=True)}
        </div>
    </div>
</body>
</html>"""
    
    with open(f'{output_dir}/report.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML报告已保存: report.html")


def main():
    parser = argparse.ArgumentParser(description="Data Analysis Toolkit")
    parser.add_argument("--input", "-i", required=True, help="Input file (CSV, Excel, JSON)")
    parser.add_argument("--output", "-o", default="./analysis_output", help="Output directory")
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    print(f"📊 开始分析: {args.input}")
    print(f"📁 输出目录: {args.output}")
    print()
    
    # Load data
    df = load_data(args.input)
    print(f"✅ 数据加载成功: {df.shape[0]} 行, {df.shape[1]} 列")
    print()
    
    # Basic info
    info = basic_info(df, args.output)
    
    # Generate visualizations
    print("\n📈 生成可视化图表...")
    plot_distributions(df, args.output)
    plot_correlation_heatmap(df, args.output)
    plot_boxplots(df, args.output)
    plot_categorical(df, args.output)
    plot_scatter_matrix(df, args.output)
    
    # Generate report
    print("\n📄 生成HTML报告...")
    generate_html_report(df, info, args.output)
    
    # Save cleaned data
    df.to_csv(f'{args.output}/cleaned_data.csv', index=False)
    print(f"✅ 清洗后数据已保存: cleaned_data.csv")
    
    print(f"\n🎉 分析完成！所有文件保存在: {args.output}")


if __name__ == "__main__":
    main()
