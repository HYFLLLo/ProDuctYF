# 离线测试数据集说明

## 1. 数据集概述

本测试数据集用于评估"AI夜宵爆品预测助手"项目各模块的性能和准确性。数据集按照PRD文档第7章"离线验证方案"的要求构建，包含事件数据、用户行为数据、商家数据和Ground Truth答案数据四个部分。

## 2. 目录结构

```
test_data/
├── events/                          # 事件数据
│   ├── weather_test_data.json       # 天气预报数据 (520条)
│   ├── sports_events_test_data.json # 赛事日历数据 (220条)
│   ├── social_media_test_data.json  # 社交媒体热搜数据 (1050条)
│   └── event_annotations.json       # 事件标注数据 (320条)
├── users/                            # 用户行为数据
│   ├── user_profiles.json           # 用户画像数据 (10500个用户)
│   ├── order_history_sample.json    # 历史订单数据 (105000条)
│   └── scene_annotations.json       # 用户场景标注数据 (520条)
├── merchants/                        # 商家数据
│   ├── merchant_profiles.json       # 商家档案数据 (55家)
│   ├── products_catalog.json        # 商品品类数据 (5200个SKU)
│   └── inventory_data.json          # 库存数据 (11000条)
├── ground_truth/                     # Ground Truth答案数据
│   └── ground_truth.json            # 决策层评估答案 (100条)
└── README.md                        # 本说明文档
```

## 3. 数据文件详细说明

### 3.1 事件数据（events/）

| 文件名 | 数据量 | 用途 | 关键字段 |
|--------|-------|------|---------|
| weather_test_data.json | 520条 | 评估事件理解分析Agent | 城市、天气类型、温度、湿度、AQI |
| sports_events_test_data.json | 220条 | 评估事件理解分析Agent | 赛事名称、类型、时间、地点、参赛队伍 |
| social_media_test_data.json | 1050条 | 评估事件理解分析Agent | 平台、话题、话题类型、浏览量、点击量 |
| event_annotations.json | 320条 | **评估专用**：含标准答案 | 标准分类、标准时间、标准热度值 |

### 3.2 用户行为数据（users/）

| 文件名 | 数据量 | 用途 | 关键字段 |
|--------|-------|------|---------|
| user_profiles.json | 10500个 | 评估用户场景分析Agent | 用户ID、职业、偏好、行为模式 |
| order_history_sample.json | 105000条 | 评估用户场景分析Agent | 订单ID、用户ID、订单时间、商品列表 |
| scene_annotations.json | 520条 | **评估专用**：含标准场景 | 标准场景标签、潜在需求商品 |

### 3.3 商家数据（merchants/）

| 文件名 | 数据量 | 用途 | 关键字段 |
|--------|-------|------|---------|
| merchant_profiles.json | 55家 | 评估决策层Agent | 商家ID、位置、GMV、夜间销售占比 |
| products_catalog.json | 5200个SKU | 评估决策层Agent | 商品ID、分类、品牌、成本、零售价 |
| inventory_data.json | 11000条 | 评估决策层Agent | 库存数量、周转率、缺货风险 |

### 3.4 Ground Truth数据（ground_truth/）

| 文件名 | 数据量 | 用途 | 关键字段 |
|--------|-------|------|---------|
| ground_truth.json | 100条 | **评估专用**：决策层标准答案 | 真实销量、真实补货需求、业务指标 |

## 4. 评估指标与数据集对应关系

| Agent | 评估指标 | 使用数据集 |
|-------|---------|-----------|
| 事件理解分析Agent | 分类准确率≥90% | event_annotations.json |
| 事件理解分析Agent | 信息抽取完整率≥95% | event_annotations.json |
| 事件理解分析Agent | 去重准确率≥98% | events/*.json |
| 事件理解分析Agent | 热度计算误差≤15% | event_annotations.json |
| 用户场景分析Agent | 场景判断准确率≥85% | scene_annotations.json |
| 用户场景分析Agent | 潜在需求命中率≥30% | scene_annotations.json |
| 决策层Agent | 爆品预测准确率≥75% | ground_truth.json |
| 决策层Agent | 补货建议准确率≥80% | ground_truth.json |
| 决策层Agent | 缺货率降低≥20% | ground_truth.json |
| 决策层Agent | 滞销率降低≥15% | ground_truth.json |

## 5. 数据使用示例

### 5.1 加载事件标注数据

```python
import json

with open('test_data/events/event_annotations.json', 'r', encoding='utf-8') as f:
    event_annotations = json.load(f)

for annot in event_annotations['annotations'][:5]:
    print(f"标注ID: {annot['annotation_id']}")
    print(f"标准分类: {annot['standard_classification']}")
    print(f"标准热度: {annot['standard_heat_score']}")
    print("---")
```

### 5.2 加载用户场景标注数据

```python
with open('test_data/users/scene_annotations.json', 'r', encoding='utf-8') as f:
    scene_annotations = json.load(f)

for annot in scene_annotations['scene_annotations'][:5]:
    print(f"标注ID: {annot['annotation_id']}")
    print(f"标准场景: {annot['standard_scene']}")
    print(f"潜在需求: {annot['standard_potential_needs']}")
    print("---")
```

### 5.3 加载Ground Truth数据

```python
with open('test_data/ground_truth/ground_truth.json', 'r', encoding='utf-8') as f:
    ground_truth = json.load(f)

for gt in ground_truth['ground_truth_records'][:3]:
    print(f"GT ID: {gt['gt_id']}")
    print(f"商家: {gt['merchant_id']}, 日期: {gt['date']}")
    print(f"实际销量: {gt['real_sales_data']}")
    print("---")
```

## 6. 数据格式规范

所有JSON文件均遵循以下格式规范：

```json
{
  "数据集说明": "数据集用途描述",
  "数据量": 数字,
  "生成日期": "YYYY-MM-DD",
  "数据来源": "模拟生成",
  "records/annotations/ground_truth_records": [实际数据数组]
}
```

## 7. 数据质量保证

- 所有数据均通过模拟生成，符合真实业务场景
- 标注数据由人工标注，标注准确率≥95%
- 数据覆盖PRD定义的多种场景和条件
- 数据时间跨度为2024年4月1日至6月30日（90天）

## 8. 注意事项

1. **数据脱敏**：所有用户ID、商家ID、商品ID均为模拟生成，不代表真实实体
2. **数据规模**：实际测试时可根据需要选择全部或部分数据
3. **Ground Truth**：仅用于评估，不可用于模型训练（避免数据泄露）
4. **更新周期**：测试数据集应定期更新以反映最新的业务场景

## 9. 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| V1.0 | 2024-07-01 | 初始版本，包含基础测试数据集 |
