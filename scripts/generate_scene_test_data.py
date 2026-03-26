"""
生成场景测试数据脚本 - 扩充场景标注到520条
"""
import json
import random
from datetime import datetime, timedelta

# 场景定义
SCENES = ["看球", "加班", "聚会", "独饮", "零食", "追剧", "游戏"]

# 商品库
PRODUCTS_BY_CATEGORY = {
    "看球": [
        ("青岛啤酒500ml", "啤酒"), ("百威啤酒330ml", "啤酒"), ("乐事薯片原味104g", "薯片"),
        ("可比克薯片", "薯片"), ("绝味卤味拼盘", "卤味"), ("周黑鸭鸭脖", "卤味"),
        ("洽洽瓜子", "坚果"), ("可口可乐330ml", "碳酸饮料"), ("百事可乐330ml", "碳酸饮料")
    ],
    "加班": [
        ("康师傅红烧牛肉面", "泡面"), ("统一老坛酸菜面", "泡面"), ("红牛功能饮料250ml", "能量饮料"),
        ("东鹏特饮", "能量饮料"), ("雀巢咖啡拿铁", "咖啡"), ("星巴克美式", "咖啡"),
        ("三顿半咖啡", "咖啡"), ("良品铺子坚果礼盒", "坚果")
    ],
    "聚会": [
        ("青岛啤酒500ml", "啤酒"), ("百威啤酒330ml", "啤酒"), ("绝对伏特加", "洋酒"),
        ("RIO微醺系列", "洋酒"), ("绝味卤味拼盘", "卤味"), ("小龙虾", "卤味"),
        ("乐事薯片混合装", "薯片"), ("奥利奥饼干", "饼干"), ("可口可乐1.5L", "碳酸饮料")
    ],
    "独饮": [
        ("百威啤酒330ml", "啤酒"), ("科罗娜啤酒330ml", "啤酒"), ("RIO强爽", "洋酒"),
        ("江小白白酒100ml", "白酒"), ("青岛原浆啤酒1L", "啤酒"), ("泰山原浆啤酒1L", "啤酒")
    ],
    "零食": [
        ("乐事薯片原味104g", "薯片"), ("可比克薯片", "薯片"), ("卫龙辣条大礼包", "辣条"),
        ("良品铺子坚果", "坚果"), ("奥利奥饼干", "饼干"), ("德芙巧克力", "巧克力"),
        ("旺旺果冻", "果冻"), ("养乐多", "乳制品")
    ],
    "追剧": [
        ("乐事薯片原味104g", "薯片"), ("可比克薯片", "薯片"), ("良品铺子坚果", "坚果"),
        ("百事可乐330ml", "碳酸饮料"), ("元气森林气泡水", "气泡水"), ("奥利奥饼干", "饼干"),
        ("周黑鸭鸭锁骨", "卤味")
    ],
    "游戏": [
        ("红牛功能饮料250ml", "能量饮料"), ("东鹏特饮", "能量饮料"), ("可口可乐330ml", "碳酸饮料"),
        ("乐事薯片原味104g", "薯片"), ("卫龙辣条", "辣条"), ("雀巢咖啡", "咖啡"),
        ("统一冰红茶", "饮料")
    ]
}

CONTEXTS = [
    {"has_sports_event": True, "event_name": "欧洲杯半决赛", "weather": "晴", "is_weekend": False, "location_type": "公寓", "user_occupation": "互联网工程师", "user_age": 28},
    {"has_sports_event": True, "event_name": "欧冠决赛", "weather": "阴", "is_weekend": True, "location_type": "酒吧", "user_occupation": "自由职业", "user_age": 32},
    {"has_sports_event": False, "event_name": None, "weather": "小雨", "is_weekend": False, "location_type": "写字楼", "user_occupation": "金融分析师", "user_age": 26},
    {"has_sports_event": False, "event_name": None, "weather": "晴", "is_weekend": True, "location_type": "商场", "user_occupation": "学生", "user_age": 22},
    {"has_sports_event": False, "event_name": None, "weather": "多云", "is_weekend": False, "location_type": "公寓", "user_occupation": "设计师", "user_age": 30},
    {"has_sports_event": True, "event_name": "NBA总决赛", "weather": "晴", "is_weekend": False, "location_type": "网吧", "user_occupation": "游戏主播", "user_age": 25},
    {"has_sports_event": False, "event_name": None, "weather": "暴雨", "is_weekend": True, "location_type": "公寓", "user_occupation": "作家", "user_age": 35},
    {"has_sports_event": False, "event_name": None, "weather": "晴", "is_weekend": False, "location_type": "学校", "user_occupation": "研究生", "user_age": 24},
]

WORK_LOCATIONS = ["写字楼", "公寓", "网吧", "学校"]
WEEKEND_LOCATIONS = ["公寓", "酒吧", "商场", "朋友家"]


def generate_scene_annotation(idx, scene):
    """生成一条场景标注"""
    # 选择商品（根据场景选择）
    available_products = PRODUCTS_BY_CATEGORY.get(scene, PRODUCTS_BY_CATEGORY["零食"])

    # 随机选择2-5个商品
    num_products = random.randint(2, 5)
    selected_products = random.sample(available_products, min(num_products, len(available_products)))
    product_ids = [f"P{100+i:03d}" for i in range(len(selected_products))]

    # 选择上下文
    ctx = random.choice(CONTEXTS).copy()

    # 根据场景调整上下文
    if scene == "看球":
        ctx["has_sports_event"] = True
        ctx["is_weekend"] = random.choice([True, False])
    elif scene == "加班":
        ctx["location_type"] = random.choice(["写字楼", "公寓", "学校"])
        ctx["has_sports_event"] = False
    elif scene == "聚会":
        ctx["location_type"] = random.choice(["酒吧", "朋友家", "公寓"])
        ctx["is_weekend"] = True

    # 生成订单时间
    if ctx["is_weekend"]:
        hour = random.randint(20, 23)
    else:
        hour = random.randint(21, 23) if random.random() > 0.3 else random.randint(0, 2)
    order_time = (datetime.now() - timedelta(days=random.randint(1, 30))).replace(hour=hour, minute=30)
    order_time_str = order_time.isoformat() + "Z"

    # 计算订单金额
    total_amount = sum(random.randint(15, 80) for _ in selected_products)

    # 生成潜在需求
    potential_needs = []
    if scene == "看球":
        potential_needs = [f"P{155:03d}", f"P{156:03d}"]  # 冰块、更多零食
    elif scene == "加班":
        potential_needs = [f"P{160:03d}", f"P{161:03d}"]  # 咖啡、泡面
    elif scene == "聚会":
        potential_needs = [f"P{170:03d}", f"P{171:03d}"]  # 更多酒水、小龙虾

    # 生成原因
    reasons = {
        "看球": "订单包含啤酒+零食+卤味，且处于欧洲杯赛事期间，符合看球场景特征",
        "加班": "订单包含泡面/咖啡，且在深夜工作时段，符合加班场景特征",
        "聚会": "订单包含多种酒水和大份量食物，符合聚会场景特征",
        "独饮": "订单仅包含小份酒水，时段较晚，符合独饮场景特征",
        "零食": "订单以零食为主，无特定场景，符合解馋型消费特征",
        "追剧": "订单包含薯片、饮料等，且在晚间时段，符合追剧场景特征",
        "游戏": "订单包含能量饮料+零食，且在网吧或深夜时段，符合游戏场景特征"
    }

    return {
        "annotation_id": f"SCENE{idx:04d}",
        "user_id": f"U{random.randint(1, 500):03d}",
        "order_id": f"O{random.randint(1, 10000):05d}",
        "order_time": order_time_str,
        "order_products": product_ids,
        "product_names": [p[0] for p in selected_products],
        "context": ctx,
        "standard_scene": scene,
        "scene_confidence": round(random.uniform(0.85, 0.98), 2),
        "reason": reasons.get(scene, "综合判断为该场景"),
        "standard_potential_needs": potential_needs,
        "potential_need_reasons": [
            f"{scene}时通常需要更多相关商品",
            "可能需要搭配购买提升体验"
        ] if potential_needs else []
    }


def generate_scene_annotations(count=520):
    """生成场景标注数据集"""
    random.seed(42)  # 保证可复现

    # 预定义真实样本
    real_samples = [
        {
            "annotation_id": "SCENE001",
            "user_id": "U001",
            "order_id": "O001",
            "order_time": "2024-04-05T22:30:00Z",
            "order_products": ["P001", "P002", "P003"],
            "product_names": ["青岛啤酒500ml", "乐事薯片原味", "卤味拼盘"],
            "context": {
                "has_sports_event": True,
                "event_name": "欧洲杯半决赛-法国vs德国",
                "weather": "晴",
                "is_weekend": False,
                "location_type": "写字楼",
                "user_occupation": "互联网工程师",
                "user_age": 28
            },
            "standard_scene": "看球",
            "scene_confidence": 0.95,
            "reason": "订单包含啤酒+零食+卤味，且处于欧洲杯赛事期间，符合看球场景特征",
            "standard_potential_needs": ["P055", "P056"],
            "potential_need_reasons": ["看球时通常需要更多零食储备", "可能需要冰块提升啤酒口感"]
        },
        {
            "annotation_id": "SCENE002",
            "user_id": "U002",
            "order_id": "O002",
            "order_time": "2024-04-05T21:45:00Z",
            "order_products": ["P004", "P005", "P006"],
            "product_names": ["喜茶多肉葡萄", "元气森林气泡水", "每日坚果礼盒"],
            "context": {
                "has_sports_event": False,
                "event_name": None,
                "weather": "小雨",
                "is_weekend": False,
                "location_type": "商业区",
                "user_occupation": "学生",
                "user_age": 22
            },
            "standard_scene": "零食",
            "scene_confidence": 0.88,
            "reason": "订单以饮品和坚果为主，符合休闲零食场景",
            "standard_potential_needs": ["P060", "P061"],
            "potential_need_reasons": ["搭配饮品的小零食", "提升口感的搭配商品"]
        }
    ]

    annotations = real_samples.copy()

    # 计算每种场景需要生成的条数
    scene_counts = {}
    base_count = (count - len(real_samples)) // len(SCENES)
    remainder = (count - len(real_samples)) % len(SCENES)

    for i, scene in enumerate(SCENES):
        scene_counts[scene] = base_count + (1 if i < remainder else 0)

    # 生成各场景数据
    idx = len(real_samples) + 1
    for scene, num in scene_counts.items():
        for _ in range(num):
            annotations.append(generate_scene_annotation(idx, scene))
            idx += 1

    # 打乱顺序
    random.shuffle(annotations)

    # 重新编号
    for i, ann in enumerate(annotations):
        ann["annotation_id"] = f"SCENE{i+1:04d}"

    return {
        "数据集说明": "用户行为测试集 - 用户场景标注数据",
        "数据量": len(annotations),
        "生成日期": datetime.now().strftime("%Y-%m-%d"),
        "数据用途": "评估用户情绪/场景分析Agent的场景判断准确率和潜在需求命中率",
        "场景分类定义": {
            "看球": "用户在看体育比赛时进行的消费行为，通常伴随啤酒、零食等",
            "加班": "用户因工作需要熬夜，消费以泡面、能量饮料、咖啡等提神产品为主",
            "聚会": "多人社交场景，消费包含多种酒水、大份量食物",
            "独饮": "单人夜间饮酒消费，通常量小、时段晚",
            "零食": "以零食、饮料为主的解馋型消费，无特定场景",
            "追剧": "用户观看电视剧/综艺时的伴随消费",
            "游戏": "用户玩游戏时的伴随消费，常搭配能量饮料、零食"
        },
        "scene_annotations": annotations
    }


if __name__ == "__main__":
    # 生成520条场景标注
    print("生成520条场景标注数据...")
    data = generate_scene_annotations(520)

    output_path = "test_data/users/scene_annotations.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已生成 {len(data['scene_annotations'])} 条场景标注")
    print(f"保存至: {output_path}")

    # 统计场景分布
    scenes = {}
    for ann in data['scene_annotations']:
        scene = ann['standard_scene']
        scenes[scene] = scenes.get(scene, 0) + 1
    print(f"场景分布: {scenes}")
