# AI Night Owl Prediction - 外卖夜间爆品预测助手

基于 AI Agent 工作流的即时零售夜间场景智能决策系统，精准预测爆品需求，助力商家精准备货、降低损耗。

[English](./README_en.md) | 中文

---

## 一句话描述

通过事件理解、场景推理、多维度销量预测的 AI Agent 工作流，为夜间便利店、闪电仓等即时零售商家提供爆品预测与补货建议，解决夜间备货难、缺货多、损耗高的核心痛点。

---

## 简介

### 背景与问题

即时零售夜间时段（20:00-06:00）订单量持续增长，但在夜间经营中，商家普遍面临三大挑战：

- **缺货损失**：因缺货导致的销售损失平均达 8%-12%，单店月均损失 4000-6000 元
- **滞销损耗**：夜间备货不当导致的食品过期损耗率是日间的 2 倍
- **预测困难**：商家依赖经验备货，无法精准预判夜间消费趋势和热点事件影响

### 解决方案

本项目通过 AI Agent 工作流，对外部事件（天气、赛事、社交热点）和用户行为进行深度理解，生成多维度爆品预测和补货建议：

- **事件理解 Agent**：实时采集并分类天气、赛事、社交媒体热点事件
- **场景推理 Agent**：基于事件和用户订单，推理"看球"、"加班"、"聚会"等消费场景
- **决策 Agent**：整合事件热度、用户偏好、地域特性，预测爆品并生成补货清单

### 核心价值

- 预测准确率达 80%+，助力商家精准备货
- 缺货率下降 30%+，滞销损耗下降 20%+
- 全流程自动化，端到端响应 < 2 分钟

---

## 快速开始

### 环境要求

- Python 3.11+
- MySQL 8.0+（可选，用于数据持久化）
- Redis 7.0+（可选，用于缓存加速）

### 安装

```bash
# 克隆项目
git clone https://github.com/HYFLLLo/ProDuctYF.git
cd ProDuctYF

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 填写配置
# 主要配置项：
# - MINIMAX_API_KEY: MiniMax API 密钥（用于 LLM 调用）
# - DB_HOST/DB_PORT: MySQL 数据库连接信息
# - REDIS_HOST/REDIS_PORT: Redis 连接信息
```

### 运行

```bash
# 离线测试（验证核心功能）
python final_test.py

# API 服务
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# 单元测试
pytest tests/ -v
```

---

## 功能特性

### 核心功能

| 功能 | 说明 |
|------|------|
| **事件理解** | 实时采集天气、赛事、社交媒体热点，自动分类与热度计算 |
| **场景推理** | 基于订单和事件上下文，识别"看球"、"加班"、"游戏"、"聚会"等消费场景 |
| **爆品预测** | 多维度评分（事件驱动40% + 用户偏好25% + 地域特性20% + 顶流热点10% + 趋势增长5%） |
| **补货建议** | 根据预测销量和库存情况，生成精准补货清单 |
| **置信度评估** | 全链路置信度传递，支持低置信度场景的人工复核 |

### 技术特性

- **AI Agent 架构**：事件理解 → 场景推理 → 决策生成的三层 Agent 工作流
- **静态动态分离**：静态映射数据月/季度更新，动态事件每日拉取，节省 80%+ Token
- **多平台支持**：兼容即时零售（美团24小时）与电商平台（淘宝5天）的差异化需求
- **降级策略**：LLM 不可用时自动切换规则引擎，保证系统可用性

---

## 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| **Web 框架** | FastAPI + Uvicorn | 高性能异步 API 服务 |
| **AI/LLM** | LangChain + MiniMax | Agent 推理与语义理解 |
| **时序预测** | Prophet | 销量趋势预测模型 |
| **数据处理** | Pandas + NumPy | 数据清洗与特征工程 |
| **数据库** | MySQL 8.0 | 业务数据持久化 |
| **缓存** | Redis 7.0 | 热度缓存与 LLM 结果缓存 |
| **异步任务** | Celery | 定时任务与异步处理 |

---

## 项目结构

```
ProDuctYF/
├── src/                          # 核心源代码
│   ├── api/                       # API 层
│   │   ├── main.py               # FastAPI 应用入口
│   │   ├── routes/               # 路由定义
│   │   └── schemas/              # 数据模型
│   ├── services/                  # 服务层（核心业务逻辑）
│   │   ├── collectors/          # 数据采集器
│   │   │   ├── weather.py       # 天气数据采集
│   │   │   ├── sports.py        # 赛事数据采集
│   │   │   └── social_media.py  # 社交媒体数据采集
│   │   ├── event_classifier.py  # 事件理解 Agent
│   │   ├── scene_inference.py    # 场景推理 Agent
│   │   ├── hot_product_engine.py # 爆品预测引擎
│   │   ├── restock_calculator.py # 补货计算
│   │   └── decision_service.py  # 决策服务（流程编排）
│   ├── ml/                        # 机器学习模块
│   │   └── llm/                  # LLM 封装与降级策略
│   └── config/                    # 配置文件
│       └── llm_config.yaml       # LLM 模型配置
├── tests/                         # 测试代码
│   ├── unit/                     # 单元测试
│   └── agent_pipeline_test.py    # 端到端测试
├── test_data/                     # 测试数据集
├── Truth_data/                    # 基准真值数据
├── scripts/                       # 脚本工具
│   └── init_database.sql        # 数据库初始化
├── PRD.md                         # 产品需求文档
├── TRD.md                         # 技术需求文档
└── requirements.txt               # Python 依赖
```

---

## 开发指南

### 添加新的事件类型

在 `src/services/collectors/` 下创建新的采集器，继承 `BaseCollector`：

```python
from .base import BaseCollector

class MyEventCollector(BaseCollector):
    async def collect(self, time_range):
        # 实现采集逻辑
        return events
```

### 自定义场景类型

在 `src/services/scene_inference.py` 的 `_rule_based_inference` 方法中添加规则：

```python
if any(kw in product_text for kw in ["新商品关键词"]):
    return {
        "final_scene": "新场景",
        "confidence": 0.9,
        "reasoning": "匹配到新场景特征"
    }
```

### 调整爆品评分权重

在 `src/services/hot_product_engine.py` 中修改权重配置：

```python
WEIGHTS = {
    "hot_event": 0.40,      # 事件驱动权重
    "user_preference": 0.25, # 用户偏好权重
    # ...
}
```

---

## 部署

### Docker 部署（推荐）

```dockerfile
# 构建镜像
docker build -t night-owl-prediction .

# 运行容器
docker run -d -p 8000:8000 \
  --env-file .env \
  night-owl-prediction
```

### Docker Compose 完整部署

```bash
# 启动所有服务（API + MySQL + Redis）
docker-compose up -d
```

### 生产环境注意事项

1. 配置 MySQL 和 Redis 的持久化存储
2. 设置合理的 LLM API 调用限流
3. 配置日志轮转策略
4. 开启健康检查端点 `/health`

---

## 常见问题

### Q: 如何获取 MiniMax API Key？

A: 访问 [MiniMax 开放平台](https://platform.minimaxi.com/) 注册并创建 API Key。

### Q: 不使用 LLM 也能运行吗？

A: 可以。系统内置了规则引擎作为降级策略，LLM 不可用时会自动切换。建议用于验证功能，正式环境建议接入 LLM。

### Q: 如何处理新的热点事件类型？

A: 在 `Truth_data/event_annotations.json` 中添加新的事件标注，系统会学习事件与爆品的映射关系。

### Q: 支持哪些外部数据源？

A: 当前支持天气 API（和风/心知）、赛事 API（球探/雷速）、社交媒体（微博/知乎热搜）。可通过扩展采集器支持更多数据源。

---

## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 致谢

- [MiniMax](https://www.minimax.chat/) - 提供 LLM API 支持
- [LangChain](https://www.langchain.com/) - Agent 框架支持
- [Prophet](https://facebook.github.io/prophet/) - 时序预测模型

---

**注意**：请勿将包含敏感信息的 `.env` 文件提交到 Git。
