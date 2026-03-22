#!/usr/bin/env python3
"""Report Analyzer - 投资报告分析与学习工具"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path


def extract_key_sections(content):
    """提取报告关键章节"""
    sections = {}
    
    # 常见章节标题模式
    patterns = {
        "摘要": r"(?:摘要|核心观点|主要结论|投资要点)[：:]*\s*\n(.*?)(?=\n#|\n##|\Z)",
        "投资逻辑": r"(?:投资逻辑|分析逻辑|研究逻辑)[：:]*\s*\n(.*?)(?=\n#|\n##|\Z)",
        "风险提示": r"(?:风险提示|风险因素|投资风险)[：:]*\s*\n(.*?)(?=\n#|\n##|\Z)",
        "盈利预测": r"(?:盈利预测|业绩预测|估值)[：:]*\s*\n(.*?)(?=\n#|\n##|\Z)",
        "投资建议": r"(?:投资建议|评级|目标价)[：:]*\s*\n(.*?)(?=\n#|\n##|\Z)",
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            sections[key] = match.group(1).strip()[:500]  # 限制长度
    
    return sections


def extract_metrics(content):
    """提取关键指标"""
    metrics = []
    
    # 匹配数字+指标的模式
    patterns = [
        r"(?:PE|P/E|市盈率)[：:]*\s*(\d+\.?\d*)",
        r"(?:PB|P/B|市净率)[：:]*\s*(\d+\.?\d*)",
        r"(?:ROE)[：:]*\s*(\d+\.?\d*)%",
        r"(?:营收|收入)[：:]*\s*(\d+\.?\d*)(?:亿|万元)?",
        r"(?:净利润)[：:]*\s*(\d+\.?\d*)(?:亿|万元)?",
        r"(?:目标价)[：:]*\s*(\d+\.?\d*)",
        r"(?:增长率|增速)[：:]*\s*(\d+\.?\d*)%",
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content)
        metrics.extend(matches)
    
    return metrics[:20]  # 最多返回20个


def extract_industries(content):
    """提取行业/板块关键词"""
    industries = []
    
    # 常见行业关键词
    industry_keywords = [
        "新能源", "半导体", "芯片", "医药", "医疗", "消费", "科技", "金融",
        "地产", "银行", "保险", "证券", "汽车", "军工", "环保", "农业",
        "互联网", "AI", "人工智能", "云计算", "大数据", "5G", "光伏",
        "锂电池", "储能", "风电", "核电", "化工", "钢铁", "有色金属",
    ]
    
    for keyword in industry_keywords:
        if keyword in content:
            industries.append(keyword)
    
    return list(set(industries))


def extract_logic_chain(content):
    """提取逻辑链条"""
    logic_indicators = [
        "因此", "所以", "意味着", "表明", "说明",
        "由于", "因为", "基于", "考虑到", "受益于",
        "导致", "推动", "促进", "影响", "冲击",
    ]
    
    sentences = content.split("\n")
    logic_sentences = []
    
    for sentence in sentences:
        for indicator in logic_indicators:
            if indicator in sentence and len(sentence) > 20:
                logic_sentences.append(sentence.strip())
                break
    
    return logic_sentences[:10]  # 最多返回10条


def analyze_report(file_path, output_dir):
    """分析单份报告"""
    print(f"📊 分析报告: {file_path}")
    print("=" * 50)
    
    # 读取文件
    path = Path(file_path)
    if not path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return
    
    content = path.read_text(encoding="utf-8")
    
    # 提取信息
    sections = extract_key_sections(content)
    metrics = extract_metrics(content)
    industries = extract_industries(content)
    logic_chain = extract_logic_chain(content)
    
    # 生成分析结果
    analysis = {
        "source_file": str(file_path),
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sections": sections,
        "metrics": metrics,
        "industries": industries,
        "logic_chain": logic_chain,
        "word_count": len(content),
    }
    
    # 保存分析结果
    os.makedirs(output_dir, exist_ok=True)
    
    report_name = path.stem
    output_file = f"{output_dir}/{report_name}_analysis.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 分析结果已保存: {output_file}")
    
    # 生成学习笔记
    generate_learning_notes(analysis, output_dir, report_name)
    
    return analysis


def generate_learning_notes(analysis, output_dir, report_name):
    """生成学习笔记"""
    lines = []
    lines.append(f"# 📚 学习笔记：{report_name}")
    lines.append(f"\n分析时间：{analysis['analyzed_at']}")
    lines.append(f"原文长度：{analysis['word_count']} 字")
    
    # 行业覆盖
    if analysis["industries"]:
        lines.append("\n## 🏭 涉及行业")
        lines.append(", ".join(analysis["industries"]))
    
    # 关键指标
    if analysis["metrics"]:
        lines.append("\n## 📊 关键指标")
        for m in analysis["metrics"][:10]:
            lines.append(f"- {m}")
    
    # 核心观点
    if "摘要" in analysis["sections"]:
        lines.append("\n## 💡 核心观点")
        lines.append(analysis["sections"]["摘要"][:300])
    
    # 逻辑链条
    if analysis["logic_chain"]:
        lines.append("\n## 🔗 逻辑链条")
        for i, logic in enumerate(analysis["logic_chain"][:5], 1):
            lines.append(f"{i}. {logic}")
    
    # 投资建议
    if "投资建议" in analysis["sections"]:
        lines.append("\n## 💰 投资建议")
        lines.append(analysis["sections"]["投资建议"][:300])
    
    # 学习要点
    lines.append("\n## ✅ 学习要点")
    lines.append("1. 分析框架：")
    lines.append("2. 数据来源：")
    lines.append("3. 可复用方法：")
    lines.append("4. 待深入研究：")
    
    notes_content = "\n".join(lines)
    
    notes_file = f"{output_dir}/learned/{report_name}_notes.md"
    os.makedirs(f"{output_dir}/learned", exist_ok=True)
    
    with open(notes_file, "w", encoding="utf-8") as f:
        f.write(notes_content)
    
    print(f"✅ 学习笔记已保存: {notes_file}")


def batch_analyze(reports_dir, output_dir):
    """批量分析目录下所有报告"""
    reports_path = Path(reports_dir)
    
    if not reports_path.exists():
        print(f"❌ 目录不存在: {reports_dir}")
        return
    
    files = list(reports_path.glob("*.md")) + list(reports_path.glob("*.txt"))
    
    if not files:
        print(f"⚠️ 目录下没有找到报告文件: {reports_dir}")
        return
    
    print(f"📚 找到 {len(files)} 份报告，开始分析...")
    
    for file_path in files:
        try:
            analyze_report(file_path, output_dir)
        except Exception as e:
            print(f"❌ 分析失败 {file_path}: {e}")
    
    print(f"\n🎉 批量分析完成！")


def main():
    parser = argparse.ArgumentParser(description="Investment Report Analyzer")
    parser.add_argument("--input", "-i", required=True, help="Report file or directory")
    parser.add_argument("--output", "-o", default="./finance_knowledge/analysis", help="Output directory")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        analyze_report(args.input, args.output)
    elif input_path.is_dir():
        batch_analyze(args.input, args.output)
    else:
        print(f"❌ 路径不存在: {args.input}")


if __name__ == "__main__":
    main()
