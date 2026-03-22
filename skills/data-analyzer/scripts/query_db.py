#!/usr/bin/env python3
"""Database Query Toolkit - SQLite, MySQL, PostgreSQL support."""

import argparse
import os
import sys
import json
import pandas as pd
from pathlib import Path

try:
    import sqlite3
    HAS_SQLITE = True
except ImportError:
    HAS_SQLITE = False

try:
    from sqlalchemy import create_engine, text
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False


def connect_sqlite(db_path):
    """Connect to SQLite database."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")
    return sqlite3.connect(db_path)


def connect_sqlalchemy(conn_string):
    """Connect using SQLAlchemy."""
    if not HAS_SQLALCHEMY:
        raise ImportError("sqlalchemy not installed")
    return create_engine(conn_string)


def explore_database(conn, db_type='sqlite'):
    """Explore database structure."""
    tables = []
    
    if db_type == 'sqlite':
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
    
    structure = {}
    for table in tables:
        if db_type == 'sqlite':
            cursor = conn.execute(f"PRAGMA table_info({table})")
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    'name': row[1],
                    'type': row[2],
                    'not_null': bool(row[3]),
                    'primary_key': bool(row[5])
                })
            structure[table] = columns
    
    return tables, structure


def get_table_stats(conn, table, db_type='sqlite'):
    """Get table statistics."""
    stats = {}
    
    # Row count
    result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    stats['row_count'] = result[0]
    
    # Column count
    if db_type == 'sqlite':
        cursor = conn.execute(f"PRAGMA table_info({table})")
        stats['column_count'] = len(cursor.fetchall())
    
    return stats


def query_to_dataframe(conn, query):
    """Execute query and return DataFrame."""
    return pd.read_sql_query(query, conn)


def analyze_table(df, table_name, output_dir):
    """Analyze a table and save results."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Basic info
    info = {
        'table': table_name,
        'shape': list(df.shape),
        'columns': list(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'missing': df.isnull().sum().to_dict(),
    }
    
    # Numerical stats
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        info['numerical_stats'] = df[numeric_cols].describe().to_dict()
    
    with open(f'{output_dir}/{table_name}_info.json', 'w') as f:
        json.dump(info, f, indent=2, default=str)
    
    print(f"✅ 表 {table_name} 分析完成: {df.shape[0]} 行, {df.shape[1]} 列")
    return info


def main():
    parser = argparse.ArgumentParser(description="Database Query Toolkit")
    parser.add_argument("--db", required=True, help="Database file (SQLite) or connection string")
    parser.add_argument("--query", "-q", help="SQL query to execute")
    parser.add_argument("--table", "-t", help="Table to analyze")
    parser.add_argument("--explore", action="store_true", help="Explore database structure")
    parser.add_argument("--output", "-o", default="./db_output", help="Output directory")
    
    args = parser.parse_args()
    
    os.makedirs(args.output, exist_ok=True)
    
    # Determine connection type
    if args.db.endswith('.db') or args.db.endswith('.sqlite'):
        print(f"📦 连接 SQLite 数据库: {args.db}")
        conn = connect_sqlite(args.db)
        db_type = 'sqlite'
    else:
        print(f"🔗 连接数据库: {args.db}")
        engine = connect_sqlalchemy(args.db)
        conn = engine.connect()
        db_type = 'sqlalchemy'
    
    # Explore mode
    if args.explore:
        print("\n🔍 探索数据库结构...")
        tables, structure = explore_database(conn, db_type)
        
        print(f"\n📋 发现 {len(tables)} 张表:")
        for table in tables:
            stats = get_table_stats(conn, table, db_type)
            print(f"  • {table}: {stats['row_count']} 行, {stats['column_count']} 列")
        
        # Save structure
        with open(f'{args.output}/database_structure.json', 'w') as f:
            json.dump({'tables': tables, 'structure': structure}, f, indent=2)
        print(f"\n✅ 结构信息已保存: database_structure.json")
        
    # Query mode
    elif args.query:
        print(f"\n📝 执行查询: {args.query[:100]}...")
        df = query_to_dataframe(conn, args.query)
        print(f"✅ 查询结果: {len(df)} 行")
        
        # Save results
        df.to_csv(f'{args.output}/query_result.csv', index=False)
        df.to_excel(f'{args.output}/query_result.xlsx', index=False)
        print(f"✅ 结果已保存: query_result.csv, query_result.xlsx")
        
    # Table analysis mode
    elif args.table:
        print(f"\n📊 分析表: {args.table}")
        df = query_to_dataframe(conn, f"SELECT * FROM {args.table}")
        analyze_table(df, args.table, args.output)
        
        # Save data
        df.to_csv(f'{args.output}/{args.table}.csv', index=False)
        print(f"✅ 数据已保存: {args.table}.csv")
    
    conn.close()
    print("\n🎉 完成！")


if __name__ == "__main__":
    main()
