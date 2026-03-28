# MEMORY.md - Lily 的长期记忆

## 关于主人

- 飞书用户名：hackwoman
- 时区：Asia/Shanghai
- 技术水平较高，喜欢折腾配置
- 通过飞书与我交流

## 重要事件

### 2026-03-26 - 首次上线 🎉
- 今天是 Lily 的第一天
- 完成了 Bootstrap 初始化
- 配置了 OpenRouter 接入小米 MiMo 模型
  - OpenRouter API key 已配置
  - 主模型：`openrouter/xiaomi/mimo-v2-pro`
  - 保留了直连小米 API 的备用配置
- 飞书频道已启用

## 配置备忘

- OpenClaw 运行在 WSL2 (Linux)
- Gateway 端口：18789，loopback 绑定
- 主模型：openrouter/xiaomi/mimo-v2-pro（推理能力）
- 备用模型：openrouter/xiaomi/mimo-v2-flash（轻量快速）
