# Image Generator Examples

## SVG Templates

### Icon
```bash
python3 scripts/generate_svg.py -o icon.svg -t icon -d '{"shape":"circle","color":"#ff6b6b","size":100}'
```

### Diagram
```bash
python3 scripts/generate_svg.py -o diagram.svg -t diagram -d '{"title":"My Process","boxes":[{"text":"Start","color":"#4a90d9"},{"text":"Step 1","color":"#00cec9"},{"text":"End","color":"#ff6b6b"}]}'
```

### Portrait
```bash
python3 scripts/generate_svg.py -o portrait.svg -t portrait -d '{"name":"My Avatar","style":"friendly"}'
```

### Chart
```bash
python3 scripts/generate_svg.py -o chart.svg -t chart -d '{"title":"Sales","values":[30,70,50,90],"labels":["Q1","Q2","Q3","Q4"]}'
```

## ASCII Art

### Banner Style
```bash
python3 scripts/generate_ascii.py -t "HELLO" -s banner
```

### Simple Block Letters
```bash
python3 scripts/generate_ascii.py -t "ABC" -s simple
```

## Charts (with matplotlib)

### Bar Chart
```bash
python3 scripts/generate_chart.py -t bar -o bar.png -d '{"values":[30,70,50,90],"labels":["A","B","C","D"]}'
```

### Line Chart
```bash
python3 scripts/generate_chart.py -t line -o line.png -d '{"values":[10,25,15,40],"labels":["Mon","Tue","Wed","Thu"]}'
```

### Pie Chart
```bash
python3 scripts/generate_chart.py -t pie -o pie.png -d '{"values":[30,25,20],"labels":["A","B","C"]}'
```
