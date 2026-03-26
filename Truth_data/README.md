# Truth_data 数据集说明

## 📋 数据集概览

**Truth_data** 是一个完整的模拟真实业务数据集，用于离线测试AI夜宵爆品预测系统。

### 数据统计

| 数据类型 | 文件名 | 数量 | 用途 |
|---------|--------|------|------|
| 天气事件 | weather_events.json | 100条 | 模拟天气API数据 |
| 体育赛事 | sports_events.json | 100条 | 模拟赛事API数据 |
| 社交媒体 | social_media_events.json | 100条 | 模拟热点API数据 |
| 事件汇总 | all_events.json | 300条 | 所有事件数据 |
| 事件标注 | event_annotations.json | 300条 | 评估事件理解Agent |
| 商家档案 | merchants.json | 55家 | 商家信息 |
| 商品品类 | products.json | 520个 | 商品数据 |
| 库存数据 | inventory.json | 520条 | 库存记录 |
| 场景标注 | scene_annotations.json | 520条 | 评估场景分析Agent |
| Ground Truth | ground_truth.json | 75条 | 评估决策层Agent |

**总计**: 2590条数据

---

## 🎯 数据集特点

### 1. 真实业务场景模拟

- **事件数据**: 模拟世界杯、欧冠、NBA、618促销等真实热点
- **商家画像**: 便利店、超市、酒吧等不同类型商家
- **商品结构**: 啤酒、零食、卤味等夜宵商品
- **用户行为**: 看球、加班、聚会等真实消费场景

### 2. 完整标注体系

每条数据都包含：
- **标准答案**: 正确的分类、场景、预测结果
- **上下文信息**: 时间、地点、天气、事件等
- **置信度评分**: 用于评估模型可靠性

### 3. 多层次评估数据

| 评估对象 | 数据集 | 评估指标 |
|---------|--------|---------|
| 事件理解Agent | event_annotations.json | 分类准确率≥90% |
| 场景分析Agent | scene_annotations.json | 场景判断准确率≥85% |
| 决策层Agent | ground_truth.json | 爆品预测≥75%，补货≥80% |

---

## 📁 文件结构

```
Truth_data/
├── 事件数据/
│   ├── weather_events.json          # 天气事件 (100条)
│   ├── sports_events.json           # 体育赛事 (100条)
│   ├── social_media_events.json     # 社交媒体热点 (100条)
│   └── all_events.json             # 所有事件汇总 (300条)
│
├── 事件标注/
│   └── event_annotations.json      # 事件分类标注 (300条)
│       ├── raw_data                 # 原始事件数据
│       ├── standard_classification  # 标准分类
│       ├── standard_heat_score     # 标准热度
│       └── standard_entities        # 标准实体
│
├── 商家商品/
│   ├── merchants.json              # 商家档案 (55家)
│   ├── products.json               # 商品数据 (520个)
│   └── inventory.json              # 库存数据 (520条)
│
├── 用户场景/
│   └── scene_annotations.json      # 场景标注 (520条)
│       ├── order_products          # 订单商品
│       ├── context                 # 上下文信息
│       ├── standard_scene          # 标准场景
│       └── standard_potential_needs # 潜在需求
│
├── 答案数据/
│   └── ground_truth.json           # Ground Truth (75条)
│       ├── merchant_id             # 商家ID
│       ├── real_sales_data         # 真实销量
│       ├── expected_hot_products   # 预期爆品
│       ├── real_restock_needs      # 实际补货需求
│       └── business_metrics        # 业务指标
│
└── README.md                       # 本说明文档
```

---

## 🔧 使用方法

### 方法1: 使用专用测试脚本

```bash
# 运行Truth_data专用测试
python test_with_truth_data.py
```

这个脚本会：
1. 自动加载Truth_data数据集
2. 依次测试所有Agent
3. 生成测试报告

### 方法2: 使用通用测试脚本

修改 `run_offline_test.py` 或 `quick_test.py` 中的数据路径：

```python
# 在测试脚本中添加
data_dir = Path("Truth_data")
```

### 方法3: 手动加载数据

```python
import json
from pathlib import Path

# 加载事件标注
with open("Truth_data/event_annotations.json", 'r', encoding='utf-8') as f:
    events = json.load(f)

# 加载Ground Truth
with open("Truth_data/ground_truth.json", 'r', encoding='utf-8') as f:
    ground_truth = json.load(f)

# 加载商家数据
with open("Truth_data/merchants.json", 'r', encoding='utf-8') as f:
    merchants = json.load(f)
```

---

## 📊 数据格式

### 事件标注格式

```json
{
  "annotation_id": "ANNOT_0001",
  "raw_data": {
    "event_name": "赛事：阿根廷 vs 法国",
    "raw_content": "世界杯决赛，阿根廷对阵法国"
  },
  "standard_classification": "赛事",
  "standard_type_detail": "足球",
  "standard_time": "2026-03-20 21:00",
  "standard_entities": ["阿根廷", "法国", "世界杯", "决赛"],
  "standard_heat_score": 95,
  "confidence_level": 0.95
}
```

### 场景标注格式

```json
{
  "annotation_id": "SCENE0001",
  "user_id": "U00001",
  "order_id": "O00001",
  "order_time": "2026-03-20T21:30:05Z",
  "order_products": ["P001", "P002", "P003"],
  "product_names": ["青岛啤酒330ml", "周黑鸭鸭脖", "乐事薯片"],
  "context": {
    "has_sports_event": true,
    "event_name": "世界杯决赛",
    "weather": "晴",
    "is_weekend": true,
    "location_type": "家中",
    "user_occupation": "上班族",
    "user_age": 28
  },
  "standard_scene": "看球",
  "scene_confidence": 0.94,
  "standard_potential_needs": ["P004", "P005"]
}
```

### Ground Truth格式

```json
{
  "gt_id": "GT001",
  "merchant_id": "M001",
  "date": "2026-03-20",
  "context": {
    "weather": "晴",
    "has_sports_event": true,
    "event_name": "世界杯决赛",
    "event_heat_score": 95
  },
  "real_sales_data": {
    "P001": {
      "product_name": "青岛啤酒330ml",
      "predicted_sales": 150,
      "actual_sales": 158,
      "sales_change_ratio": 0.45
    }
  },
  "expected_hot_products": ["P001", "P002", "P003", ...],
  "real_restock_needs": {
    "P001": {
      "product_name": "青岛啤酒330ml",
      "needed_quantity": 200,
      "urgency": "high",
      "reason": "销量增长45%，需要补货"
    }
  },
  "business_metrics": {
    "total_gmv": 15000,
    "gmv_change_ratio": 0.25,
    "out_of_stock_rate": 0.05,
    "overstock_rate": 0.03
  }
}
```

---

## 🎓 测试评估标准

### 事件理解Agent

| 指标 | 达标要求 | 说明 |
|------|---------|------|
| 分类准确率 | ≥90% | 事件分类正确率 |
| 信息抽取完整率 | ≥95% | 实体、关键词抽取完整度 |
| 去重准确率 | ≥98% | 重复事件检测准确率 |
| 热度计算误差 | ≤15% | 预测热度与实际热度误差 |

### 场景分析Agent

| 指标 | 达标要求 | 说明 |
|------|---------|------|
| 场景判断准确率 | ≥85% | 场景识别正确率 |
| 潜在需求命中率 | ≥30% | 推荐的潜在需求命中用户真实需求 |
| 召回率 | ≥80% | 场景相关商品召回率 |
| 处理延迟 | ≤5秒/用户 | 单用户场景分析延迟 |

### 决策层Agent

| 指标 | 达标要求 | 说明 |
|------|---------|------|
| 爆品预测准确率 | ≥75% | 预测爆品与实际爆品重合度 |
| 补货建议准确率 | ≥80% | 补货建议的准确率 |
| 缺货率降低率 | ≥20% | 相比基线降低的缺货率 |
| 滞销率降低率 | ≥15% | 相比基线降低的滞销率 |

---

## 🔄 数据更新

如需生成新的测试数据：

```bash
# 运行数据生成器
python generate_truth_data.py
```

这会重新生成所有数据集，覆盖现有文件。

---

## 📝 数据质量保证

### 数据一致性

- 所有事件、商家、商品ID保持全局唯一
- 场景数据与Ground Truth商家ID匹配
- 时间戳格式统一为ISO 8601

### 数据合理性

- 销量数据符合真实业务规律
- 场景分布符合实际消费场景比例
- 事件热度与类型匹配

### 数据完整性

- 所有必要字段都有值
- 标注数据包含完整上下文
- Ground Truth包含业务指标

---

## 🎯 使用建议

### 开发阶段

1. 使用Truth_data进行离线开发
2. 验证算法逻辑正确性
3. 调整模型参数优化性能

### 测试阶段

1. 使用完整数据集进行压力测试
2. 评估各Agent达标情况
3. 生成详细测试报告

### 生产阶段

1. 用Truth_data做冒烟测试
2. 验证系统整体流程
3. 确保与离线测试结果一致

---

## ⚠️ 注意事项

1. **数据保密**: Truth_data为模拟数据，可公开使用
2. **版本控制**: 每次运行 `generate_truth_data.py` 会重新生成数据
3. **数据量**: 可根据需要修改生成脚本中的 `count` 参数
4. **格式兼容**: 确保测试脚本的数据加载代码与Truth_data格式一致

---

## 📞 支持

如有问题，请检查：

1. JSON文件格式是否正确
2. 文件编码是否为UTF-8
3. 必填字段是否完整
4. 测试脚本路径是否正确

---

*数据集生成工具: generate_truth_data.py*
*测试脚本: test_with_truth_data.py, quick_verify_truth.py*
*生成时间: 2026-03-20*
