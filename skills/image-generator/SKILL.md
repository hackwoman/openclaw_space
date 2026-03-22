---
name: image-generator
description: Generate images, graphics, and visual content using Python. Create SVG graphics, ASCII art, charts, diagrams, simple illustrations, icons, and data visualizations. Use when user asks to draw, create images, generate graphics, make charts/diagrams, or produce visual content. Supports PNG (via PIL/Pillow), SVG, and ASCII art outputs.
---

# Image Generator

Generate images and graphics using Python scripts.

## Capabilities

- **SVG Graphics**: Scalable vector graphics for icons, diagrams, illustrations
- **Charts & Graphs**: Bar charts, line graphs, pie charts, data visualization
- **ASCII Art**: Text-based art and diagrams
- **Simple Illustrations**: Basic shapes, icons, logos
- **Image Manipulation**: Resize, crop, add text/watermark to existing images

## Quick Start

### Generate an SVG Image

```bash
python3 {skill_dir}/scripts/generate_svg.py --output <output_path> --template <template_name> --data '{json_data}'
```

Available templates: `icon`, `diagram`, `chart`, `portrait`, `logo`

### Generate ASCII Art

```bash
python3 {skill_dir}/scripts/generate_ascii.py --text "<text>" --style <style>
```

Styles: `block`, `shadow`, `bold`, `thin`

### Generate Chart (requires matplotlib)

```bash
python3 {skill_dir}/scripts/generate_chart.py --type <bar|line|pie> --data '<json_data>' --output <output_path>
```

## Workflows

### 1. User Asks for an Image

1. Determine the type of image needed (icon, chart, diagram, illustration)
2. Choose appropriate template/script
3. Generate the image
4. Provide the file path to the user

### 2. Custom Graphics

1. Create a custom SVG or Python script
2. Execute to generate the output
3. Save to workspace and share

## Notes

- SVG is preferred for scalability and small file size
- For complex photo-realistic images, inform user that code-based generation has limitations
- PIL/Pillow needed for PNG output (install with `pip3 install Pillow`)
- matplotlib needed for charts (install with `pip3 install matplotlib`)
