# 监控数据 ETL 智能平台 - 开源框架调研报告

_调研日期：2026-03-27_

---

## 1. CMDB 与配置管理

### 1.1 NetBox
- **链接：** https://github.com/netbox-community/netbox
- **核心思想：** 网络基础设施的权威数据源，强类型模型（设备、机架、IP、VLAN 等），REST API 驱动
- **优点：** 模型设计严谨，API 完善，插件生态丰富
- **缺点：** 偏网络基础设施，通用 IT 资产建模需要扩展
- **借鉴度：** ⭐⭐⭐⭐ — 对象模型和关系设计值得借鉴

### 1.2 Apache Atlas
- **链接：** https://github.com/apache/atlas
- **核心思想：** 元数据治理框架，支持自定义实体类型（TypeDef），内置图数据库存储实体关系
- **优点：** 元数据模型灵活，支持血缘追踪，Type 系统强大
- **缺点：** 重量级（依赖 HBase/Solr），运维复杂，Java 生态
- **借鉴度：** ⭐⭐⭐⭐⭐ — TypeDef 系统和图关系模型是核心参考

### 1.3 DataHub (LinkedIn)
- **链接：** https://github.com/datahub-project/datahub
- **核心思想：** 现代元数据平台，图模型存储，支持流式元数据变更（MAE/MCE 消息）
- **优点：** 架构现代（Kafka + Elasticsearch + 图存储），流式变更通知，Aspect 模型灵活
- **缺点：** 主要面向数据治理，运维监控场景需要改造
- **借鉴度：** ⭐⭐⭐⭐⭐ — 流式元数据架构 + Aspect 模型设计是最佳参考

### 1.4 iTop
- **链接：** https://github.com/Combodo/iTop
- **核心思想：** ITIL 合规的 ITSM/CMDB，PHP 实现，面向运维管理
- **优点：** ITIL 流程完整，CMDB 关系模型成熟
- **缺点：** 架构老旧（PHP），扩展性差，API 弱
- **借鉴度：** ⭐⭐⭐ — ITIL 关系模型可参考，技术架构不借鉴

---

## 2. 监控数据采集与接入

### 2.1 统一接入层

#### OpenTelemetry (OTel)
- **链接：** https://github.com/open-telemetry
- **核心思想：** 统一的可观测性标准，一个 SDK 收集 Metrics/Traces/Logs
- **优点：** 厂商中立，标准化数据模型（Resource、Scope、Signal），Collector 可扩展
- **缺点：** Collector 配置复杂，某些 receiver 还在 maturing
- **借鉴度：** ⭐⭐⭐⭐⭐ — **接入层必须基于 OTel**，这是行业标准

#### Vector (Datadog)
- **链接：** https://github.com/vectordotdev/vector
- **核心思想：** 高性能数据路由管道（Rust），统一处理 logs/metrics/events
- **优点：** 性能极强，配置灵活（VRL 语言），Source/Sink 丰富
- **缺点：** 复杂变换需要学习 VRL
- **借鉴度：** ⭐⭐⭐⭐⭐ — **ETL 数据管道核心参考**，source/transform/sink 模型

### 2.2 时序指标

#### Prometheus + VictoriaMetrics
- Prometheus：Pull 模型，PromQL 查询，服务发现
- VictoriaMetrics：兼容 Prometheus，性能更好，支持集群
- **借鉴度：** ⭐⭐⭐⭐ — PromQL 作为指标查询标准，VM 作为存储后端候选

### 2.3 调用链追踪

#### SkyWalking
- **链接：** https://github.com/apache/skywalking
- **核心思想：** APM 平台，自动探针 + OAP 分析引擎 + UI
- **优点：** 拓扑自动发现，告警规则丰富，多语言探针
- **缺点：** 自成体系，与其他监控集成需要额外工作
- **借鉴度：** ⭐⭐⭐⭐ — 拓扑自动发现和实体关系推断是好参考

### 2.4 事件/告警

#### Alertmanager
- Prometheus 生态，支持分组、抑制、静默
- **借鉴度：** ⭐⭐⭐ — 告警路由和抑制逻辑可参考

---

## 3. ETL 与数据处理

### 3.1 流式 ETL

#### Apache Flink
- **核心思想：** 有状态流处理，Exactly-once 语义，SQL + DataStream API
- **优点：** 状态管理强大，窗口计算灵活，容错性好
- **缺点：** 运维复杂，学习曲线陡
- **借鉴度：** ⭐⭐⭐⭐ — 复杂流式 ETL 场景的首选

#### Benthos (现 Redpanda Connect)
- **链接：** https://github.com/redpanda-data/benthos
- **核心思想：** 声明式流处理引擎，YAML 配置管道
- **优点：** 配置即代码，内置丰富 connector，运维简单
- **缺点：** 复杂有状态处理能力弱于 Flink
- **借鉴度：** ⭐⭐⭐⭐⭐ — **轻量级 ETL 管道的最佳参考**，声明式配置

### 3.2 知识图谱与实体关系

#### Neo4j
- **核心思想：** 图数据库，Cypher 查询语言
- **优点：** 关系查询强大，适合 CMDB 实体关系存储
- **缺点：** 社区版功能有限，集群版收费
- **借鉴度：** ⭐⭐⭐⭐ — 图查询模式参考，但大规模场景考虑其他方案

#### Apache Atlas TypeDef 系统
- **核心思想：** 用户自定义实体类型（EntityDef）、关系类型（RelationshipDef）、分类（ClassificationDef）
- **优点：** Schema 灵活可扩展，运行时可新增类型
- **借鉴度：** ⭐⭐⭐⭐⭐ — **CMDB 模型设计的核心参考**

### 3.3 向量化 / Embedding

#### 模型方案
- 日志 Embedding：LogPAI 项目，或用 LLM（GPT/BERT）生成日志向量
- 指标 Embedding：时序数据特征提取 + 降维
- 告警 Embedding：文本向量化（用于告警聚合和根因分析）
- **存储：** Milvus / Qdrant / pgvector
- **借鉴度：** ⭐⭐⭐⭐ — 向量模型是智能运维的基础

---

## 4. 数据仓库与分析

### 4.1 Apache Doris / StarRocks
- **核心思想：** MPP 架构 OLAP 引擎，兼容 MySQL 协议，实时导入
- **优点：** 实时分析性能极强，支持多维分析（Rollup/物化视图），MySQL 兼容降低学习成本
- **缺点：** 集群运维有一定复杂度
- **借鉴度：** ⭐⭐⭐⭐⭐ — **OLAP 引擎首选**，多维分析能力强

### 4.2 ClickHouse
- **核心思想：** 列式存储 OLAP，极致压缩和查询性能
- **优点：** 查询速度极快，压缩率高
- **缺点：** 不支持标准 SQL 的 UPDATE/DELETE，Join 能力弱
- **借鉴度：** ⭐⭐⭐⭐ — 日志/指标明细存储好选择

### 4.3 时序 + OLAP 融合
- 思路：用 Doris/StarRocks 替代独立时序数据库，统一存储
- 支持：指标时序分析 + 多维聚合 + 明细查询
- **借鉴度：** ⭐⭐⭐⭐⭐ — 统一存储减少数据搬运

---

## 5. 智能运维（AIOps）

### 5.1 异常检测
- 开源方案：PyOD、Alibi-Detect、Merlion (Salesforce)
- 思路：对指标做时序异常检测，对日志做模式异常检测

### 5.2 根因分析
- 思路：基于拓扑图 + 告警关联 + 知识图谱推理
- LLM 结合：用 LLM 理解告警上下文，结合图谱推理根因

### 5.3 LLM + 运维
- **Grafana LLM plugin：** 用 LLM 解释指标和日志
- **思路：**
  - 自然语言查询监控数据（Text-to-SQL / Text-to-PromQL）
  - 告警智能摘要和建议
  - 自动化 Runbook 生成
- **借鉴度：** ⭐⭐⭐⭐⭐ — LLM 是平台智能化的关键

---

## 6. 前端场景搭建

### 6.1 Grafana
- **核心思想：** 数据源插件 + Panel 插件 + Dashboard JSON 模型
- **优点：** 生态最强，数据源丰富，可视化类型多
- **缺点：** Dashboard JSON 复杂，自定义开发门槛高
- **借鉴度：** ⭐⭐⭐⭐ — Panel/Dashboard 概念参考，但不直接用

### 6.2 Apache Superset
- **核心思想：** SQL-first 的 BI 平台，低代码构建图表
- **优点：** SQL Lab 强大，图表类型丰富，权限体系完整
- **缺点：** 面向 BI，运维监控场景定制不足
- **借鉴度：** ⭐⭐⭐ — SQL-first 思路可参考

### 6.3 API-first 前端架构
- 思路：前端不直接连数据源，通过统一 API 层获取数据
- API 层负责：权限、数据聚合、格式化
- 前端只做渲染和交互
- **借鉴度：** ⭐⭐⭐⭐⭐ — **必须采用 API-first 架构**

---

## 总结：核心借鉴方向

| 层次 | 首选参考 | 核心借鉴点 |
|------|---------|-----------|
| 接入层 | OpenTelemetry | 标准化数据模型 |
| ETL 管道 | Vector / Benthos | 声明式管道、Source/Transform/Sink |
| 对象模型 | Apache Atlas TypeDef + DataHub Aspect | 自定义实体类型、关系模型、流式元数据 |
| 存储层 | Doris/StarRocks | OLAP 多维分析 |
| 图存储 | Neo4j / AGE (PostgreSQL) | 实体关系图查询 |
| 向量存储 | Milvus / pgvector | 日志/告警语义向量 |
| 智能层 | LLM + 向量检索 | 自然语言查询、异常检测、根因分析 |
| 前端 | API-first + 可配置 Panel | 数据与展示分离 |
