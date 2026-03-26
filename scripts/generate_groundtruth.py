"""
生成Ground Truth数据脚本 - 扩充到100条
"""
import json
import random
from datetime import datetime, timedelta

PRODUCTS = [
    ("P001", "青岛啤酒500ml", "啤酒", 8.5, 5.5),
    ("P002", "乐事薯片原味104g", "薯片", 12.0, 8.0),
    ("P003", "绝味卤味拼盘", "卤味", 35.0, 22.0),
    ("P004", "红牛功能饮料250ml", "能量饮料", 15.0, 10.0),
    ("P005", "康师傅红烧牛肉面", "泡面", 8.0, 5.0),
    ("P006", "可口可乐330ml", "碳酸饮料", 6.0, 4.0),
    ("P007", "百威啤酒330ml", "啤酒", 7.0, 4.5),
    ("P008", "周黑鸭鸭脖", "卤味", 28.0, 18.0),
    ("P009", "东鹏特饮", "能量饮料", 12.0, 8.0),
    ("P010", "统一老坛酸菜面", "泡面", 7.5, 4.8),
    ("P011", "元气森林气泡水", "气泡水", 10.0, 6.5),
    ("P012", "良品铺子坚果礼盒", "坚果", 45.0, 28.0),
    ("P013", "卫龙辣条大礼包", "辣条", 22.0, 14.0),
    ("P014", "奥利奥饼干", "饼干", 15.0, 10.0),
    ("P015", "RIO微醺系列", "洋酒", 25.0, 16.0),
    ("P016", "小龙虾", "卤味", 68.0, 45.0),
    ("P017", "泰山原浆啤酒1L", "啤酒", 35.0, 22.0),
    ("P018", "雀巢咖啡拿铁", "咖啡", 18.0, 12.0),
    ("P019", "百事可乐1.5L", "碳酸饮料", 12.0, 8.0),
    ("P020", "科罗娜啤酒330ml", "啤酒", 9.0, 5.8),
]

EVENTS = [
    {"name": "欧洲杯半决赛-法国vs德国", "heat": 88, "has_sports": True},
    {"name": "欧冠决赛-曼城vs皇马", "heat": 95, "has_sports": True},
    {"name": "世界杯预选赛", "heat": 82, "has_sports": True},
    {"name": "NBA总决赛G7", "heat": 92, "has_sports": True},
    {"name": "LOL全球总决赛", "heat": 90, "has_sports": True},
    {"name": "无重大赛事", "heat": 0, "has_sports": False},
]

WEATHERS = ["晴", "阴", "小雨", "暴雨", "多云", "降温"]


def generate_restock_needs(selected_products, context):
    """生成补货需求"""
    restock = {}
    has_sports = context.get("has_sports_event", False)
    for pid, pname, cat, price, cost in selected_products[:5]:
        # 根据品类和场景计算需求
        base_qty = random.randint(20, 80)

        if cat == "啤酒" and has_sports:
            needed_qty = int(base_qty * 1.5)
            urgency = "high"
        elif cat == "能量饮料" and not has_sports:
            needed_qty = int(base_qty * 1.2)
            urgency = "medium"
        elif cat == "卤味":
            needed_qty = int(base_qty * 1.3)
            urgency = "high"
        else:
            needed_qty = base_qty
            urgency = "medium" if base_qty > 50 else "low"

        restock[pid] = {
            "needed_quantity": needed_qty,
            "urgency": urgency,
            "reason": f"{cat}基于场景预测需要补货"
        }
    return restock


def generate_sales_data(selected_products, context, event):
    """生成销量数据"""
    sales_data = {}
    base_total = 0

    for pid, pname, cat, price, cost in selected_products:
        # 基础销量
        base_sales = random.randint(20, 100)

        # 根据场景调整
        has_sports = context.get("has_sports_event", False)
        if cat == "啤酒" and has_sports:
            actual_sales = int(base_sales * 1.4)
            change_ratio = 0.4
        elif cat == "能量饮料" and not has_sports:
            actual_sales = int(base_sales * 1.3)
            change_ratio = 0.3
        elif cat == "卤味" and has_sports:
            actual_sales = int(base_sales * 1.35)
            change_ratio = 0.35
        elif cat == "薯片" or cat == "零食":
            actual_sales = int(base_sales * 1.15)
            change_ratio = 0.15
        else:
            actual_sales = base_sales
            change_ratio = 0.0 if base_sales < 50 else 0.1

        predicted_sales = int(actual_sales * 0.9)  # 预测略低

        sales_data[pid] = {
            "product_name": pname,
            "predicted_sales": predicted_sales,
            "actual_sales": actual_sales,
            "sales_change_ratio": round(change_ratio, 2)
        }
        base_total += actual_sales * price

    return sales_data, base_total


def generate_ground_truth(idx):
    """生成一条ground truth"""
    # 选择商家
    merchant_id = f"M{random.randint(1, 55):03d}"

    # 选择事件
    event = random.choice(EVENTS)

    # 选择天气
    weather = random.choice(WEATHERS)

    # 选择商品（3-8个）
    num_products = random.randint(3, 8)
    selected_products = random.sample(PRODUCTS, min(num_products, len(PRODUCTS)))

    # 生成销量数据
    context = {"weather": weather, "has_sports_event": event["has_sports"]}
    sales_data, total_gmv = generate_sales_data(selected_products, context, event)

    # 生成补货需求
    restock_needs = generate_restock_needs(selected_products, context)

    # 计算业务指标
    has_hot = any(v["sales_change_ratio"] > 0.2 for v in sales_data.values())
    out_of_stock_rate = random.uniform(0.05, 0.15) if has_hot else random.uniform(0.02, 0.08)
    out_of_stock_change = -random.uniform(0.08, 0.18) if has_hot else -random.uniform(0.02, 0.05)
    overstock_rate = random.uniform(0.03, 0.10)
    overstock_change = random.uniform(0.01, 0.05)

    return {
        "gt_id": f"GT{idx:04d}",
        "merchant_id": merchant_id,
        "date": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d"),
        "night_period": "20:00-06:00",
        "context": {
            "weather": weather,
            "has_sports_event": event["has_sports"],
            "event_name": event["name"],
            "event_heat_score": event["heat"]
        },
        "real_sales_data": sales_data,
        "real_restock_needs": restock_needs,
        "business_metrics": {
            "total_gmv": int(total_gmv),
            "gmv_change_ratio": round(sum(v["sales_change_ratio"] for v in sales_data.values()) / len(sales_data), 2),
            "out_of_stock_rate": round(out_of_stock_rate, 2),
            "out_of_stock_rate_change": round(out_of_stock_change, 2),
            "overstock_rate": round(overstock_rate, 2),
            "overstock_rate_change": round(overstock_change, 2)
        }
    }


def generate_ground_truth_data(count=100):
    """生成ground truth数据集"""
    random.seed(42)

    records = []

    # 预定义真实样本
    real_samples = [
        {
            "gt_id": "GT001",
            "merchant_id": "M001",
            "date": "2024-04-05",
            "night_period": "20:00-06:00",
            "context": {
                "weather": "晴",
                "has_sports_event": True,
                "event_name": "欧洲杯半决赛-法国vs德国",
                "event_heat_score": 88
            },
            "real_sales_data": {
                "P001": {"product_name": "青岛啤酒500ml", "predicted_sales": 85, "actual_sales": 92, "sales_change_ratio": 0.45},
                "P002": {"product_name": "乐事薯片原味", "predicted_sales": 35, "actual_sales": 38, "sales_change_ratio": 0.30},
                "P003": {"product_name": "绝味卤味拼盘", "predicted_sales": 18, "actual_sales": 22, "sales_change_ratio": 0.55},
                "P004": {"product_name": "红牛功能饮料", "predicted_sales": 25, "actual_sales": 28, "sales_change_ratio": 0.20},
                "P005": {"product_name": "康师傅红烧牛肉面", "predicted_sales": 30, "actual_sales": 25, "sales_change_ratio": -0.10}
            },
            "real_restock_needs": {
                "P001": {"needed_quantity": 120, "urgency": "high", "reason": "赛事带动啤酒需求激增"},
                "P003": {"needed_quantity": 40, "urgency": "high", "reason": "卤味爆品需紧急补货"},
                "P004": {"needed_quantity": 50, "urgency": "medium", "reason": "需求稳定上升"}
            },
            "business_metrics": {
                "total_gmv": 15800,
                "gmv_change_ratio": 0.35,
                "out_of_stock_rate": 0.08,
                "out_of_stock_rate_change": -0.12,
                "overstock_rate": 0.05,
                "overstock_rate_change": 0.02
            }
        }
    ]

    records.extend(real_samples)

    # 生成剩余记录
    for i in range(len(real_samples), count):
        records.append(generate_ground_truth(i + 1))

    return {
        "数据集说明": "Ground Truth答案数据 - 用于评估决策层Agent的预测准确性",
        "数据量": len(records),
        "生成日期": datetime.now().strftime("%Y-%m-%d"),
        "数据用途": "评估爆品预测准确率、补货建议准确率、业务价值指标",
        "ground_truth_records": records
    }


if __name__ == "__main__":
    # 生成100条ground truth
    print("生成100条ground truth数据...")
    data = generate_ground_truth_data(100)

    output_path = "test_data/ground_truth/ground_truth.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已生成 {len(data['ground_truth_records'])} 条ground truth")
    print(f"保存至: {output_path}")

    # 统计
    merchants = set(r["merchant_id"] for r in data["ground_truth_records"])
    has_sports = sum(1 for r in data["ground_truth_records"] if r["context"]["has_sports_event"])
    print(f"商家数: {len(merchants)}, 有赛事: {has_sports}")
