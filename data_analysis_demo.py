#!/usr/bin/env python3
"""数据分析能力演示 - 生成示例数据并分析"""

import pandas as pd
import numpy as np
import sqlite3
import os

output_dir = '/home/kui/.openclaw/workspace/data_analysis'
os.makedirs(output_dir, exist_ok=True)

print("📊 数据分析能力演示")
print("=" * 50)

# ============ 1. 创建示例 Excel 数据 ============
print("\n1️⃣ 创建示例销售数据...")

np.random.seed(42)
n = 500

# 生成销售数据
sales_data = {
    '订单ID': [f'ORD{i:05d}' for i in range(1, n+1)],
    '日期': pd.date_range('2025-01-01', periods=n, freq='D'),
    '产品类别': np.random.choice(['电子产品', '服装', '食品', '家居', '图书'], n),
    '产品名称': np.random.choice(['笔记本电脑', '手机', 'T恤', '牛仔裤', '咖啡', '面包', '台灯', '书籍'], n),
    '单价': np.random.uniform(10, 5000, n).round(2),
    '数量': np.random.randint(1, 10, n),
    '客户年龄': np.random.randint(18, 70, n),
    '客户性别': np.random.choice(['男', '女'], n),
    '地区': np.random.choice(['北京', '上海', '广州', '深圳', '杭州', '成都'], n),
    '支付方式': np.random.choice(['支付宝', '微信', '银行卡', '现金'], n),
}

df_sales = pd.DataFrame(sales_data)
df_sales['销售额'] = (df_sales['单价'] * df_sales['数量']).round(2)

# 添加一些缺失值（模拟真实数据）
missing_idx = np.random.choice(n, 20, replace=False)
df_sales.loc[missing_idx, '客户年龄'] = np.nan

# 保存为 Excel
excel_path = f'{output_dir}/销售数据_2025.xlsx'
df_sales.to_excel(excel_path, index=False, sheet_name='销售明细')
print(f"✅ Excel 文件已创建: {excel_path}")

# ============ 2. 创建 SQLite 数据库 ============
print("\n2️⃣ 创建示例数据库...")

db_path = f'{output_dir}/company.db'
conn = sqlite3.connect(db_path)

# 员工表
employees = pd.DataFrame({
    '员工ID': range(1, 101),
    '姓名': [f'员工{i:03d}' for i in range(1, 101)],
    '部门': np.random.choice(['技术部', '销售部', '市场部', '财务部', '人事部'], 100),
    '职位': np.random.choice(['工程师', '经理', '主管', '专员', '总监'], 100),
    '薪资': np.random.uniform(8000, 50000, 100).round(0),
    '入职日期': pd.date_range('2020-01-01', periods=100, freq='10D'),
    '绩效评分': np.random.uniform(60, 100, 100).round(1),
})
employees.to_sql('employees', conn, if_exists='replace', index=False)

# 部门表
departments = pd.DataFrame({
    '部门ID': range(1, 6),
    '部门名称': ['技术部', '销售部', '市场部', '财务部', '人事部'],
    '负责人': ['张三', '李四', '王五', '赵六', '钱七'],
    '预算': [500000, 300000, 200000, 150000, 100000],
})
departments.to_sql('departments', conn, if_exists='replace', index=False)

# 项目表
projects = pd.DataFrame({
    '项目ID': range(1, 21),
    '项目名称': [f'项目{i:02d}' for i in range(1, 21)],
    '负责人ID': np.random.randint(1, 101, 20),
    '状态': np.random.choice(['进行中', '已完成', '暂停', '计划中'], 20),
    '开始日期': pd.date_range('2025-01-01', periods=20, freq='15D'),
    '预算': np.random.uniform(50000, 500000, 20).round(0),
})
projects.to_sql('projects', conn, if_exists='replace', index=False)

conn.close()
print(f"✅ SQLite 数据库已创建: {db_path}")
print(f"   - employees 表: {len(employees)} 条记录")
print(f"   - departments 表: {len(departments)} 条记录")
print(f"   - projects 表: {len(projects)} 条记录")

# ============ 3. 运行数据分析 ============
print("\n3️⃣ 运行数据分析...")

# 分析销售数据
print("\n📈 销售数据分析:")
print("-" * 40)

# 按类别统计
category_stats = df_sales.groupby('产品类别').agg({
    '销售额': ['sum', 'mean', 'count'],
    '数量': 'sum'
}).round(2)
category_stats.columns = ['总销售额', '平均销售额', '订单数', '总数量']
print("\n按产品类别:")
print(category_stats)

# 按地区统计
region_stats = df_sales.groupby('地区')['销售额'].agg(['sum', 'mean', 'count']).round(2)
region_stats.columns = ['总销售额', '平均销售额', '订单数']
print("\n按地区:")
print(region_stats)

# 月度趋势
df_sales['月份'] = df_sales['日期'].dt.month
monthly_sales = df_sales.groupby('月份')['销售额'].sum().round(2)
print("\n月度销售额:")
print(monthly_sales)

# ============ 4. 分析数据库 ============
print("\n4️⃣ 数据库分析:")
print("-" * 40)

conn = sqlite3.connect(db_path)

# 部门薪资统计
print("\n部门薪资统计:")
dept_salary = pd.read_sql_query("""
    SELECT 部门, 
           COUNT(*) as 人数,
           ROUND(AVG(薪资), 2) as 平均薪资,
           ROUND(MIN(薪资), 2) as 最低薪资,
           ROUND(MAX(薪资), 2) as 最高薪资,
           ROUND(SUM(薪资), 2) as 薪资总额
    FROM employees
    GROUP BY 部门
    ORDER BY 平均薪资 DESC
""", conn)
print(dept_salary)

# 绩效分析
print("\n绩效评分分析:")
perf_stats = pd.read_sql_query("""
    SELECT 部门,
           ROUND(AVG(绩效评分), 2) as 平均绩效,
           COUNT(CASE WHEN 绩效评分 >= 80 THEN 1 END) as 优秀人数,
           COUNT(CASE WHEN 绩效评分 < 60 THEN 1 END) as 待改进人数
    FROM employees
    GROUP BY 部门
    ORDER BY 平均绩效 DESC
""", conn)
print(perf_stats)

# 项目状态
print("\n项目状态统计:")
project_status = pd.read_sql_query("""
    SELECT 状态, COUNT(*) as 数量,
           ROUND(SUM(预算), 0) as 总预算
    FROM projects
    GROUP BY 状态
""", conn)
print(project_status)

conn.close()

# ============ 5. 保存分析结果 ============
print("\n5️⃣ 保存分析结果...")

# 保存统计结果到 Excel
with pd.ExcelWriter(f'{output_dir}/分析报告.xlsx', engine='openpyxl') as writer:
    category_stats.to_excel(writer, sheet_name='类别分析')
    region_stats.to_excel(writer, sheet_name='地区分析')
    monthly_sales.to_excel(writer, sheet_name='月度趋势')
    dept_salary.to_excel(writer, sheet_name='部门薪资')
    perf_stats.to_excel(writer, sheet_name='绩效分析')
    project_status.to_excel(writer, sheet_name='项目状态')

print(f"✅ 分析报告已保存: {output_dir}/分析报告.xlsx")

print("\n" + "=" * 50)
print("🎉 数据分析演示完成！")
print(f"\n📁 所有文件保存在: {output_dir}")
print("\n生成的文件:")
for f in os.listdir(output_dir):
    print(f"  • {f}")
