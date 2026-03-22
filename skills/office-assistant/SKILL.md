---
name: office-assistant
description: Professional office assistant for document creation, report writing, data analysis, and visual content generation. Create business documents (Word, Excel, PPT), write professional copy (reports, proposals, notifications), generate charts and infographics, analyze data, and prepare presentations. Use when user needs office work support, document writing, business analysis, report generation, or professional content creation.
---

# Office Assistant 🏢

Professional office assistant with dedicated sub-agent for all business documentation needs.

## Quick Start

### Spawn Office Specialist Sub-agent

When user requests office work, spawn a dedicated sub-agent:

```python
sessions_spawn(
    task="Office task description with all details",
    label="office-specialist",
    mode="run",  # or "session" for persistent
    cleanup="keep"
)
```

### Task Types

1. **Document Creation** - Reports, proposals, memos, meeting minutes
2. **Data Analysis** - Excel processing, statistics, visualization
3. **Presentation** - PPT creation, slides design
4. **Writing** - Business copy, emails, announcements

## Workflows

### 1. Work Report Request
```
User: "帮我写一份季度工作汇报"
→ Spawn sub-agent with report task
→ Sub-agent creates Word document
→ Returns file path to user
```

### 2. Data Analysis Request
```
User: "分析这个Excel数据"
→ Spawn sub-agent with data file
→ Sub-agent performs analysis
→ Returns charts and report
```

### 3. Presentation Request
```
User: "做一个项目介绍PPT"
→ Spawn sub-agent with content
→ Sub-agent creates presentation
→ Returns PPT file
```

## Sub-agent Configuration

```python
{
    "task": "Detailed task description",
    "label": "office-specialist",
    "mode": "run",
    "model": "xiaomi/mimo-v2-omni",  # or default
    "cleanup": "keep"
}
```

## Available Scripts

- `scripts/create_document.py` - Word/Excel/PPT generation
- `scripts/create_chart.py` - Chart generation
- `scripts/create_presentation.py` - PPT creation

## Best Practices

1. **Clear Task Description** - Include all requirements in spawn task
2. **Specify Output Format** - Word, Excel, PPT, or image
3. **Provide Data** - Attach or reference source data
4. **Set Expectations** - Mention deadline if urgent
