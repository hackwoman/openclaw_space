# Demo 场景规划 v3

_日期：2026-03-28_
_核心思路：模拟器模拟完整请求流，每条请求同时产生日志+Trace+指标，用 trace_id 串联_

---

## 1. 核心理念：请求流模拟

**不是独立生成日志和 Trace，而是模拟一个完整的用户请求流经所有服务的过程。**

```
用户请求 "创建订单"
    │
    │ trace_id=abc123
    ▼
┌──────────────────────────────────────────────────────────────────────┐
│  Gateway (15ms)                                                      │
│  ├─ log: [INFO] "POST /api/order from 10.0.1.1"                      │
│  └─ span: gateway → order-service (15ms)                             │
│                                                                      │
│  order-service (120ms)                                               │
│  ├─ log: [INFO] "Processing order for user_123"                      │
│  ├─ span: order-service → order-db SQL INSERT (35ms)                 │
│  ├─ span: order-service → payment-service (80ms)                     │
│  │                                                                   │
│  │   payment-service (75ms)                                          │
│  │   ├─ log: [INFO] "Processing payment for order_456"               │
│  │   ├─ span: payment-service → payment-db SQL INSERT (25ms)         │
│  │   └─ span: payment-service → alipay-gateway HTTP POST (45ms)      │
│  │                                                                   │
│  └─ span: order-service → inventory-service gRPC (15ms)              │
│      inventory-service (12ms)                                        │
│      ├─ log: [INFO] "Stock deducted for product_789"                 │
│      └─ span: inventory-service → inventory-db SQL UPDATE (8ms)      │
│                                                                      │
│  总耗时: 120ms                                                       │
│  产生: 4条日志 + 7个Span + 5个指标数据点                              │
│  全部用 trace_id=abc123 串联                                          │
└──────────────────────────────────────────────────────────────────────┘
```

**一条请求 = 多条日志 + 多个 Span + 多个指标，全部 trace_id 串联。**

---

## 2. 数据输出方式

| 数据 | 格式 | 走管道 | 生成时机 |
|------|------|--------|---------|
| 应用日志 | JSON → 写文件 | filelog → Vector → ClickHouse | 每个 Span 产生时 |
| Trace Span | OTLP → 推送 | otlp → Vector → ClickHouse | 每个服务调用时 |
| 指标 | OTLP → 推送 | otlp → Vector → Doris(未来) | 每分钟聚合 |
| 网络日志 | Syslog → UDP | syslog → Vector → ClickHouse | 防火墙事件时 |

---

## 1. 模拟器架构（请求流驱动）

```
┌──────────────────────────────────────────────────────────────┐
│                    请求流模拟器 (RequestFlowSimulator)         │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │               请求流引擎                               │   │
│  │                                                      │   │
│  │  每秒产生 N 个模拟请求                                 │   │
│  │  每个请求经过完整服务调用链                             │   │
│  │  每个服务节点同时产生:                                  │   │
│  │    ├─ 日志 (JSON → 写文件)                             │   │
│  │    ├─ Trace Span (OTLP → 推送)                        │   │
│  │    └─ 指标数据 (累计，定期推送)                         │   │
│  │                                                      │   │
│  │  trace_id 贯穿所有数据                                │   │
│  └──────────────────┬───────────────────────────────────┘   │
│                     │                                        │
│         ┌───────────┼───────────┐                           │
│         ▼           ▼           ▼                           │
│    日志文件     OTLP 推送    Syslog UDP                      │
│    /var/log/    :4318        :5140                           │
└────┼───────────┼─────────────┼───────────────────────────────┘
     │           │             │
     ▼           ▼             ▼
┌──────────────────────────────────────────────────────────────┐
│              OTel Collector (真实采集管道)                     │
│  filelog ← 日志文件    otlp ← Trace    syslog ← 网络日志     │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                  Vector ETL (真实管道)                         │
│  解析 → CMDB 关联 → 时效分类 → 写入存储                        │
└──────────┬────────────────────┬──────────────────────────────┘
           │                    │
           ▼                    ▼
     ClickHouse            PostgreSQL
     (日志+Trace)           (CMDB)
```
│                  Vector ETL (真实的管道)                   │
│  解析 → 关联CMDB → 时效分类 → 写入存储                      │
└──────────┬────────────────────┬──────────────────────────┘
           │                    │
           ▼                    ▼
    ┌─────────────┐    ┌──────────────┐
    │ ClickHouse  │    │ PostgreSQL   │
    │ (日志)      │    │ (CMDB)       │
    └──────┬──────┘    └──────┬───────┘
           │                  │
           └────────┬─────────┘
                    ▼
             ┌─────────────┐
             │  前端展示     │
             │  浏览器查看   │
             └─────────────┘
```

**关键区别：模拟器不直接写数据库，它产生的是"看起来像真实应用的数据"，让管道自己处理。**

---

## 2. 三种数据输出方式

| 方式 | 模拟什么 | Collector 接收 | 适用数据 |
|------|---------|---------------|---------|
| **写日志文件** | 应用写本地日志 | filelog receiver | 应用日志、系统日志 |
| **OTLP 推送** | 应用 SDK 直推 | otlp receiver | Trace、结构化指标 |
| **Syslog UDP** | 网络设备 syslog | syslog receiver | 防火墙、交换机日志 |

---

## 3. 模拟器设计（请求流引擎）

### 3.1 目录结构

```
demo/simulator/
├── main.py                  # 入口：启动引擎，控制场景
├── config.py                # 配置
│
├── engine/
│   ├── request_flow.py      # 核心：请求流引擎
│   ├── service_graph.py     # 服务调用图定义
│   └── scenario.py          # 场景控制器（故障注入/恢复）
│
├── outputs/
│   ├── log_writer.py        # 写日志文件（OTel filelog 采集）
│   ├── otlp_sender.py       # OTLP 推送（Trace/指标）
│   └── syslog_sender.py     # Syslog UDP（网络设备）
│
├── scenarios/
│   ├── normal.yaml          # 正常运营
│   ├── slow_query.yaml      # 慢查询
│   ├── cascade.yaml         # 级联故障
│   └── network.yaml         # 网络异常
│
└── seed_cmdb.py             # 初始化 CMDB 实体和关系
```

### 3.2 核心：请求流引擎

```python
class RequestFlowEngine:
    """
    模拟用户请求流经服务调用链。
    每个请求产生：日志 + Trace Span + 指标，全部用 trace_id 串联。
    """
    
    def __init__(self, service_graph: ServiceGraph):
        self.graph = service_graph        # 服务调用关系图
        self.log_writer = LogWriter()     # 写日志文件
        self.otlp_sender = OTLPSender()   # OTLP 推送
        self.scenario = None              # 当前场景
    
    def simulate_request(self, request_type: str = "create_order"):
        """模拟一个完整的请求"""
        trace_id = generate_trace_id()
        
        # 获取该请求类型的服务调用链
        flow = self.graph.get_flow(request_type)
        
        for step in flow.steps:
            span_id = generate_span_id()
            parent_span_id = step.parent_span_id or ""
            
            # 应用故障注入（场景控制）
            duration_ms = self.apply_faults(step.service, step.base_duration_ms)
            is_error = self.should_error(step.service)
            
            # 1. 写日志文件（OTel filelog 会采集）
            self.log_writer.emit(
                service=step.service,
                level="error" if is_error else "info",
                message=step.error_message if is_error else step.normal_message,
                trace_id=trace_id,
                span_id=span_id,
                extra={"duration_ms": duration_ms, "status": 500 if is_error else 200}
            )
            
            # 2. 发送 OTLP Trace Span（OTel otlp receiver 会接收）
            self.otlp_sender.send_span(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=parent_span_id,
                service=step.service,
                operation=step.operation,
                duration_ms=duration_ms,
                status="ERROR" if is_error else "OK",
                attributes=step.attributes
            )
        
        return trace_id
    
    def run(self, rps: float = 1.0):
        """持续运行，每秒产生 rps 个请求"""
        while True:
            request_type = random.choice(self.graph.request_types)
            self.simulate_request(request_type)
            time.sleep(1.0 / rps + random.uniform(-0.2, 0.2))
```

### 3.3 服务调用图定义

```python
class ServiceGraph:
    """
    定义服务之间的调用关系和每条链路的特征。
    """
    
    FLOWS = {
        "create_order": [
            Step("gateway", "POST /api/order", 15,
                 normal="Request received: POST /api/order",
                 error="Upstream timeout"),
            Step("order-service", "POST /order/create", 120, parent="gateway",
                 normal="Processing order for user_{user_id}",
                 error="Order creation failed"),
            Step("order-db", "INSERT orders", 35, parent="order-service",
                 normal="Order inserted: order_{order_id}",
                 error="Slow query: INSERT orders (2500ms)"),
            Step("payment-service", "POST /pay", 75, parent="order-service",
                 normal="Processing payment for order_{order_id}",
                 error="PaymentServiceException: connection refused"),
            Step("payment-db", "INSERT payments", 25, parent="payment-service",
                 normal="Payment recorded: payment_{pay_id}",
                 error="ConnectionTimeout: payment-db:3306"),
            Step("inventory-service", "DeductStock", 15, parent="order-service",
                 normal="Stock deducted for product_{product_id}",
                 error="InventoryServiceException: timeout"),
            Step("inventory-db", "UPDATE inventory", 8, parent="inventory-service",
                 normal="Inventory updated: product_{product_id}",
                 error="Deadlock found when trying to get lock"),
        ],
        
        "user_login": [
            Step("gateway", "POST /api/login", 10,
                 normal="Request received: POST /api/login"),
            Step("user-service", "POST /user/login", 45, parent="gateway",
                 normal="User login: user_{user_id}"),
            Step("user-db", "SELECT users", 12, parent="user-service",
                 normal="User found: user_{user_id}"),
        ],
        
        "query_inventory": [
            Step("gateway", "GET /api/inventory", 8,
                 normal="Request received: GET /api/inventory"),
            Step("inventory-service", "GET /stock/query", 35, parent="gateway",
                 normal="Querying inventory for product_{product_id}"),
            Step("inventory-db", "SELECT inventory", 15, parent="inventory-service",
                 normal="Inventory queried: {count} items"),
        ],
    }
```

---

## 4. 场景控制（故障注入）

```python
class ScenarioController:
    """
    场景控制器：管理生成器的生命周期，注入故障。
    """
    
    def __init__(self):
        self.generators = {
            "payment": AppLogGenerator("payment-service"),
            "order": AppLogGenerator("order-service"),
            "user": AppLogGenerator("user-service"),
            "inventory": AppLogGenerator("inventory-service"),
            "trace": TraceOTLPGenerator(),
            "firewall": NetworkSyslogGenerator(),
        }
    
    def run_scenario(self, name: str):
        """运行指定场景"""
        scenario = self.load_scenario(name)
        print(f"🎬 运行场景: {scenario.name}")
        
        for step in scenario.timeline:
            time.sleep(step.delay)
            print(f"  ⏱ +{step.time}: {step.event}")
            
            for action in step.actions:
                self.execute_action(action)
    
    def execute_action(self, action: dict):
        """执行一个动作"""
        gen = self.generators[action["generator"]]
        
        if action["type"] == "emit_log":
            gen.emit(action["level"], action["message"])
        
        elif action["type"] == "inject_fault":
            # 注入故障：改变生成器行为
            gen.set_fault(action["fault_type"], action["params"])
        
        elif action["type"] == "heal":
            # 恢复：移除故障
            gen.clear_fault()
```

### 场景文件

```yaml
# scenarios/cascade.yaml
name: "级联故障：支付 DB 故障"
description: "payment-db 磁盘 IO 饱和 → 支付服务超时 → 订单链路中断"

baseline:
  # 所有服务正常运行的基础流量
  generators:
    - target: payment
      rate: 50/min     # 每分钟 50 条正常日志
    - target: order
      rate: 80/min
    - target: user
      rate: 30/min
    - target: trace
      rate: 100/min    # 每分钟 100 个 Span

timeline:
  - time: "+0s"
    event: "payment-db 磁盘 IO 飙升"
    actions:
      - type: emit_log
        generator: payment
        level: warn
        message: "Slow query: SELECT * FROM payments WHERE status='pending' (1200ms)"
        repeat: 3

  - time: "+30s"
    event: "payment-service 开始连接超时"
    actions:
      - type: inject_fault
        generator: payment
        fault_type: error_rate
        params: { rate: 0.3 }  # 30% 的日志变为 error
      - type: emit_log
        generator: payment
        level: error
        message: "ConnectionTimeout: Cannot connect to payment-db:3306 after 5000ms"
        repeat: 5

  - time: "+60s"
    event: "order-service 调用 payment 失败"
    actions:
      - type: emit_log
        generator: order
        level: error
        message: "PaymentServiceException: payment failed after 3 retries, order_id=12345"
        repeat: 8

  - time: "+120s"
    event: "故障恢复"
    actions:
      - type: heal
        generator: payment
      - type: emit_log
        generator: payment
        level: info
        message: "Database connection restored, resuming normal operations"
```

---

## 5. 启动方式

```bash
# 启动模拟器（默认正常场景，持续生成数据）
cd monitoring-etl/demo/simulator
python main.py

# 切换到故障场景
python main.py --scenario cascade

# 控制速率
python main.py --rate 10x    # 10 倍速快速演示

# 停止
Ctrl+C
```

---

## 6. 前端验证

模拟器运行后，打开前端 `http://47.93.61.196:3000`：
- 日志查询页能看到实时流入的日志
- 搜索 "error" 能看到故障日志
- 搜索 "payment" 能看到支付相关日志
- 切换场景后，日志内容和级别会相应变化

---

## 7. 实施顺序

1. **基础生成器** — AppLogGenerator（写文件，最核心）
2. **场景框架** — ScenarioController + 场景 YAML
3. **场景 1** — 正常运营（持续 INFO 日志）
4. **场景 2** — 慢查询（注入 WARN/ERROR）
5. **场景 3** — 级联故障（多服务联动）
6. **场景 4** — 网络设备（SyslogGenerator）
7. **Trace 生成器** — OTLP 推送（可选，Phase 2 再加）
8. **CMDB 种子数据** — 预置实体和关系

---

_Demo v2 计划，待主人确认_
