---
name: data-analyzer
description: Professional data analysis for Excel, CSV, and databases. Perform statistical analysis, data cleaning, visualization, and generate reports. Use when user needs to analyze data, create charts, process Excel/CSV files, query databases, or generate data insights. Supports pandas, numpy, matplotlib, seaborn.
---

# Data Analyzer

Professional data analysis and visualization toolkit.

## Capabilities

### Data Sources
- **Excel** (.xlsx, .xls) - Multiple sheets, formulas
- **CSV/TSV** - Delimited text files
- **JSON** - Nested data structures
- **SQLite** - Direct database queries
- **MySQL/PostgreSQL** - With connection string

### Analysis Features
- **Statistical Summary** - Mean, median, std, correlations
- **Data Cleaning** - Missing values, duplicates, types
- **Grouping & Aggregation** - Group by, pivot tables
- **Time Series** - Date parsing, resampling, trends
- **Correlation Analysis** - Heatmaps, relationships

### Visualization
- **Distribution** - Histograms, box plots, violin plots
- **Comparison** - Bar charts, grouped bars
- **Trends** - Line charts, area charts
- **Relationships** - Scatter plots, heatmaps
- **Composition** - Pie charts, stacked bars

## Quick Start

### Analyze Excel/CSV
```bash
python3 {skill_dir}/scripts/analyze_data.py --input <file> --output <dir>
```

### Generate Report
```bash
python3 {skill_dir}/scripts/generate_report.py --input <file> --format html
```

### Query Database
```bash
python3 {skill_dir}/scripts/query_db.py --db <db_file> --query "<sql>"
```

## Workflows

### 1. Quick Data Overview
1. Load data with pandas
2. Show head(), info(), describe()
3. Check missing values
4. Generate summary statistics

### 2. Full Analysis
1. Data cleaning
2. Statistical analysis
3. Correlation analysis
4. Generate visualizations
5. Create HTML report

### 3. Database Analysis
1. Connect to database
2. Explore tables
3. Run queries
4. Analyze results
5. Export findings

## Output Formats
- CSV - Cleaned data
- PNG/SVG - Charts
- HTML - Interactive report
- Excel - Formatted output
