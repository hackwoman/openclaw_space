#!/usr/bin/env python3
"""Generate charts and graphs using matplotlib."""

import argparse
import json
import sys

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def generate_bar_chart(data, output, title="Bar Chart"):
    """Generate a bar chart."""
    values = data.get("values", [30, 70, 50, 90, 40])
    labels = data.get("labels", ["A", "B", "C", "D", "E"])
    colors = data.get("colors", ["#4a90d9", "#ff6b6b", "#ffd700", "#00cec9", "#a29bfe"])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color=colors[:len(values)], edgecolor='white', linewidth=2)
    
    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                str(val), ha='center', va='bottom', fontweight='bold')
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Value', fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✅ Bar chart saved to: {output}")


def generate_line_chart(data, output, title="Line Chart"):
    """Generate a line chart."""
    values = data.get("values", [10, 25, 15, 40, 30, 55, 45])
    labels = data.get("labels", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    color = data.get("color", "#4a90d9")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(labels, values, marker='o', linewidth=3, markersize=10, color=color)
    ax.fill_between(labels, values, alpha=0.3, color=color)
    
    # Add value labels
    for i, (x, y) in enumerate(zip(labels, values)):
        ax.text(x, y + 2, str(y), ha='center', va='bottom', fontweight='bold')
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Value', fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✅ Line chart saved to: {output}")


def generate_pie_chart(data, output, title="Pie Chart"):
    """Generate a pie chart."""
    values = data.get("values", [30, 25, 20, 15, 10])
    labels = data.get("labels", ["A", "B", "C", "D", "E"])
    colors = data.get("colors", ["#4a90d9", "#ff6b6b", "#ffd700", "#00cec9", "#a29bfe"])
    
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors[:len(values)],
                                      autopct='%1.1f%%', startangle=90,
                                      textprops={'fontsize': 12})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✅ Pie chart saved to: {output}")


def generate_svg_chart(data, output, title="Chart"):
    """Fallback: Generate a simple SVG chart without matplotlib."""
    values = data.get("values", [30, 70, 50, 90, 40])
    labels = data.get("labels", ["A", "B", "C", "D", "E"])
    colors = data.get("colors", ["#4a90d9", "#ff6b6b", "#ffd700", "#00cec9", "#a29bfe"])
    
    width = 500
    height = 350
    bar_width = 50
    gap = (width - len(values) * bar_width) // (len(values) + 1)
    max_val = max(values) if values else 1
    
    bars = ""
    for i, (val, label) in enumerate(zip(values, labels)):
        x = gap + i * (bar_width + gap)
        bar_height = int((val / max_val) * 200)
        y = 280 - bar_height
        color = colors[i % len(colors)]
        bars += f'''
  <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="5"/>
  <text x="{x + bar_width//2}" y="300" text-anchor="middle" font-size="12" fill="#333">{label}</text>
  <text x="{x + bar_width//2}" y="{y - 5}" text-anchor="middle" font-size="11" fill="#333">{val}</text>'''
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" fill="#f8f9fa" rx="15"/>
  <text x="{width//2}" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">{title}</text>
  <line x1="30" y1="280" x2="{width-20}" y2="280" stroke="#999" stroke-width="2"/>
  {bars}
</svg>'''
    
    with open(output, 'w') as f:
        f.write(svg)
    print(f"✅ SVG chart saved to: {output}")


def main():
    parser = argparse.ArgumentParser(description="Generate charts")
    parser.add_argument("--type", "-t", required=True,
                       choices=["bar", "line", "pie"],
                       help="Chart type")
    parser.add_argument("--data", "-d", required=True, help="JSON data")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--title", default="Chart", help="Chart title")
    
    args = parser.parse_args()
    
    data = json.loads(args.data) if isinstance(args.data, str) else args.data
    
    if not HAS_MATPLOTLIB:
        print("⚠️  matplotlib not available, generating SVG chart instead")
        generate_svg_chart(data, args.output, args.title)
        return
    
    generators = {
        "bar": generate_bar_chart,
        "line": generate_line_chart,
        "pie": generate_pie_chart,
    }
    
    generator = generators.get(args.type)
    if generator:
        generator(data, args.output, args.title)
    else:
        print(f"❌ Unknown chart type: {args.type}")
        sys.exit(1)


if __name__ == "__main__":
    main()
