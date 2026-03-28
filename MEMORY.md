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

## 监控 ETL 平台项目

- GitHub 仓库：hackwoman/monitoring-etl（HTTPS 克隆）
- 云服务器：阿里云 ECS 47.93.61.196 (2C 4G 40GB)
- 登录：lily / Temp2026!（SSH 密码登录已开启）
- 镜像加速：docker.1ms.run（阿里云默认镜像源不可用）
- CMDB 数据库：docker compose down -v 会丢失，需手动重建
- 前端：React 构建有 Vite tree-shaking 问题，临时用静态 HTML 兜底
- 模拟器：python3 demo/simulator/main.py --rps 2 --log-dir logs
- 项目运行状态：http://47.93.61.196:3000（前端）、:8000（API）

## 主人偏好

- 重视架构设计的完整性和前瞻性
- 不急于交付速度，重质量
- 告警理念：业务风险度驱动，不以 IT 严重度为准
- CMDB 实例应从数据自动生成（非预置）
- 数据要走完整管道（采集→ETL→存储），不直接写库
