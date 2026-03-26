"""
全面模拟数据生成器 - 生成最真实的业务场景数据
覆盖所有业务维度，确保测试完整性
"""
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


class ComprehensiveDataGenerator:
    """全面数据生成器"""

    def __init__(self):
        self.output_dir = Path("Truth_data_Comprehensive")
        self.output_dir.mkdir(exist_ok=True)

    def generate_comprehensive_events(self):
        """生成全面事件数据"""
        events = []

        # 1. 天气事件 - 各种天气类型
        weather_types = [
            ("晴", 50), ("多云", 30), ("阴", 20), ("小雨", 15),
            ("中雨", 10), ("雷阵雨", 8), ("暴雨", 5), ("大雪", 3)
        ]
        locations = ["北京", "上海", "广州", "深圳", "成都", "杭州", "武汉", "西安"]

        for i, (weather, count) in enumerate(weather_types):
            for j in range(count):
                temp = random.randint(15, 35) if "雨" not in weather and "雪" not in weather else random.randint(5, 20)
                events.append({
                    "annotation_id": f"ANNOT_E{i*10+j:04d}",
                    "raw_data": {
                        "event_name": f"天气：{weather}",
                        "raw_content": f"温度{temp}度，{weather}，风力{random.choice(['微风', '东北风2-3级', '西南风3-4级'])}"
                    },
                    "standard_classification": "天气",
                    "standard_type_detail": weather,
                    "standard_time": datetime.now().isoformat(),
                    "standard_location": random.choice(locations),
                    "standard_entities": [],
                    "standard_heat_score": random.randint(20, 60)
                })

        # 2. 赛事事件 - 各种类型比赛
        leagues = [
            ("欧冠", 30), ("英超", 25), ("西甲", 20), ("意甲", 15),
            ("德甲", 12), ("世界杯", 25), ("欧洲杯", 20), ("NBA", 30),
            ("CBA", 15), ("奥运会", 20), ("亚运会", 15)
        ]
        teams = {
            "足球": ["皇马", "巴萨", "拜仁", "曼城", "利物浦", "巴黎圣日耳曼", "尤文图斯", "AC米兰", "切尔西", "阿森纳"],
            "篮球": ["湖人", "勇士", "篮网", "雄鹿", "凯尔特人", "热火", "掘金", "太阳", "快船", "76人"],
            "综合": ["中国队", "美国队", "日本队", "韩国队", "德国队", "巴西队", "法国队", "英国队"]
        }

        for i, (league, count) in enumerate(leagues):
            for j in range(count):
                is_final = random.random() < 0.15
                sport_type = "篮球" if "NBA" in league else "足球"

                if sport_type == "篮球":
                    team1, team2 = random.sample(teams["篮球"], 2)
                else:
                    team1, team2 = random.sample(teams["足球"], 2)

                heat = 95 if is_final else random.randint(60, 90)
                event_name = f"赛事：{team1} vs {team2}"

                events.append({
                    "annotation_id": f"ANNOT_S{i*10+j:04d}",
                    "raw_data": {
                        "event_name": event_name,
                        "raw_content": f"{league}{sport_type}比赛，{team1}对阵{team2}，{'决赛' if is_final else '小组赛'}"
                    },
                    "standard_classification": "赛事",
                    "standard_type_detail": f"{league}_{sport_type}",
                    "standard_time": datetime.now().isoformat(),
                    "standard_location": random.choice(locations),
                    "standard_entities": [team1, team2, league],
                    "standard_heat_score": heat
                })

        # 3. 娱乐事件 - 各种娱乐类型
        entertainment_types = [
            ("电影上映", 25), ("电视剧热播", 20), ("演唱会", 15),
            ("颁奖典礼", 12), ("综艺节目", 18), ("游戏发售", 15),
            ("明星八卦", 20), ("电竞比赛", 18)
        ]

        for i, (ent_type, count) in enumerate(entertainment_types):
            for j in range(count):
                if "电影" in ent_type:
                    name = f"电影《{random.choice(['满江红', '流浪地球3', '热辣滚烫', '飞驰人生2', '熊出没·狂野大陆'])}》首映"
                elif "电视剧" in ent_type:
                    name = f"电视剧《{random.choice(['繁花', '漫长的季节', '长相思', '梦华录', '庆余年2'])}》热播"
                elif "演唱会" in ent_type:
                    name = f"演唱会：{random.choice(['周杰伦', '五月天', '林俊杰', '陈奕迅', '张学友'])}巡回演唱会"
                elif "颁奖" in ent_type:
                    name = f"颁奖典礼：{random.choice(['奥斯卡', '金鹰奖', '金马奖', '金像奖', 'MTV颁奖'])}"
                elif "综艺" in ent_type:
                    name = f"综艺：{random.choice(['奔跑吧', '极限挑战', '向往的生活', '创造营', '脱口秀大会'])}"
                elif "游戏" in ent_type:
                    name = f"游戏发售：{random.choice(['原神新版本', '王者荣耀新赛季', '塞尔达传说', '黑神话悟空'])}"
                elif "电竞" in ent_type:
                    name = f"电竞比赛：{random.choice(['LOL全球总决赛', 'DOTA2国际邀请赛', 'CSGOMajor'])}"
                else:
                    name = f"娱乐热点：{random.choice(['明星塌房', '热搜第一', '热搜话题', '热点事件'])}"

                events.append({
                    "annotation_id": f"ANNOT_ENT{i*10+j:04d}",
                    "raw_data": {
                        "event_name": name,
                        "raw_content": f"{name}引发全网关注"
                    },
                    "standard_classification": "娱乐",
                    "standard_type_detail": ent_type,
                    "standard_time": datetime.now().isoformat(),
                    "standard_location": random.choice(locations),
                    "standard_entities": [name],
                    "standard_heat_score": random.randint(50, 90)
                })

        # 4. 社会热点 - 各种社会事件
        social_topics = [
            ("618促销", 30), ("双十一", 25), ("春节", 20), ("五一", 15),
            ("国庆", 18), ("世界杯", 35), ("欧洲杯", 25), ("奥运会", 30),
            ("高考", 20), ("中考", 15), ("考研", 12), ("节假日出行", 18),
            ("天气预警", 25), ("交通管制", 15), ("突发新闻", 20), ("热搜话题", 25)
        ]

        for i, (topic, count) in enumerate(social_topics):
            for j in range(count):
                events.append({
                    "annotation_id": f"ANNOT_SOC{i*10+j:04d}",
                    "raw_data": {
                        "event_name": f"热点：{topic}",
                        "raw_content": f"{topic}引发全网讨论，热度持续攀升"
                    },
                    "standard_classification": "社会",
                    "standard_type_detail": topic,
                    "standard_time": datetime.now().isoformat(),
                    "standard_location": random.choice(locations),
                    "standard_entities": [topic],
                    "standard_heat_score": random.randint(60, 95)
                })

        return events

    def generate_comprehensive_scenes(self):
        """生成全面场景数据"""
        scenes = []

        # 定义各种场景的商品组合（多样化）
        scene_configs = {
            "看球": [
                {"products": ["青岛啤酒330ml", "百威啤酒500ml", "乐事薯片原味", "周黑鸭鸭脖"], "has_sports": True, "event": "世界杯决赛"},
                {"products": ["雪花啤酒", "乐事薯片烧烤味", "泡椒凤爪", "可口可乐"], "has_sports": True, "event": "欧冠决赛"},
                {"products": ["青岛啤酒330ml", "洽洽瓜子", "周黑鸭鸭锁骨", "薯片先生"], "has_sports": True, "event": "NBA总决赛"},
                {"products": ["百威啤酒500ml", "乐事薯片原味", "绝味鸭脖", "可口可乐330ml"], "has_sports": True, "event": "欧洲杯半决赛"},
                {"products": ["青岛啤酒330ml", "百威啤酒500ml", "乐事薯片", "周黑鸭鸭脖", "泡椒凤爪"], "has_sports": True, "event": "世界杯淘汰赛"},
            ],
            "加班": [
                {"products": ["红牛250ml", "康师傅泡面", "东鹏特饮", "农心辛拉面"], "has_sports": False, "event": ""},
                {"products": ["红牛250ml", "统一老坛酸菜", "雀巢咖啡", "奥利奥饼干"], "has_sports": False, "event": ""},
                {"products": ["东鹏特饮", "康师傅红烧牛肉面", "魔爪能量饮料", "好丽友派"], "has_sports": False, "event": ""},
                {"products": ["红牛250ml", "农心辛拉面", "脉动", "士力架"], "has_sports": False, "event": ""},
                {"products": ["红牛250ml", "康师傅泡面", "东鹏特饮", "可口可乐", "奥利奥"], "has_sports": False, "event": ""},
            ],
            "聚会": [
                {"products": ["青岛啤酒330ml", "百威啤酒500ml", "威士忌", "乐事薯片", "洽洽瓜子"], "has_sports": False, "event": ""},
                {"products": ["雪花啤酒", "青岛啤酒330ml", "可乐", "薯片", "坚果礼盒"], "has_sports": False, "event": ""},
                {"products": ["百威啤酒500ml", "百威啤酒330ml", "威士忌", "雪碧", "好丽友", "奥利奥"], "has_sports": False, "event": ""},
                {"products": ["青岛啤酒330ml", "哈尔滨啤酒", "可口可乐", "乐事薯片", "洽洽瓜子", "周黑鸭"], "has_sports": False, "event": ""},
                {"products": ["威士忌", "百利甜酒", "可乐", "薯片", "坚果", "巧克力"], "has_sports": False, "event": ""},
            ],
            "夜宵": [
                {"products": ["周黑鸭鸭脖", "泡椒凤爪", "自热火锅", "梦龙冰淇淋"], "has_sports": False, "event": ""},
                {"products": ["周黑鸭鸭锁骨", "绝味鸭脖", "小龙虾", "冰啤酒"], "has_sports": False, "event": ""},
                {"products": ["泡椒凤爪", "周黑鸭鸭翅", "小龙虾", "冰淇淋"], "has_sports": False, "event": ""},
                {"products": ["绝味鸭脖", "泡椒凤爪", "小龙虾", "百威啤酒330ml"], "has_sports": False, "event": ""},
                {"products": ["周黑鸭鸭脖", "绝味鸭锁骨", "自热米饭", "可口可乐"], "has_sports": False, "event": ""},
            ],
            "追剧": [
                {"products": ["乐事薯片原味", "奥利奥", "可口可乐330ml", "洽洽瓜子"], "has_sports": False, "event": ""},
                {"products": ["薯片先生", "好丽友派", "百事可乐", "奥利奥饼干"], "has_sports": False, "event": ""},
                {"products": ["乐事薯片", "奥利奥", "雪碧", "薯片零食大礼包"], "has_sports": False, "event": ""},
                {"products": ["可比克薯片", "好丽友蛋黄派", "可口可乐", "巧克力豆"], "has_sports": False, "event": ""},
                {"products": ["乐事薯片原味", "奥利奥", "百事可乐", "洽洽瓜子", "坚果"], "has_sports": False, "event": ""},
            ],
            "游戏": [
                {"products": ["红牛250ml", "东鹏特饮", "乐事薯片原味", "泡椒凤爪"], "has_sports": False, "event": ""},
                {"products": ["红牛250ml", "魔爪能量饮料", "薯片", "辣条大礼包"], "has_sports": False, "event": ""},
                {"products": ["东鹏特饮", "红牛250ml", "乐事薯片", "泡椒凤爪", "可口可乐"], "has_sports": False, "event": ""},
                {"products": ["红牛250ml", "脉动", "薯片", "周黑鸭鸭脖"], "has_sports": False, "event": ""},
                {"products": ["魔爪", "红牛250ml", "东鹏特饮", "乐事薯片", "辣条"], "has_sports": False, "event": ""},
            ],
            "独饮": [
                {"products": ["江小白白酒100ml", "RIO强爽"], "has_sports": False, "event": ""},
                {"products": ["威士忌50ml", "可口可乐"], "has_sports": False, "event": ""},
                {"products": ["百威啤酒330ml"], "has_sports": False, "event": ""},
                {"products": ["青岛啤酒330ml", "周黑鸭鸭脖"], "has_sports": False, "event": ""},
                {"products": ["RIO强爽", "泡椒凤爪"], "has_sports": False, "event": ""},
            ]
        }

        # 生成每个场景的多种变体
        scene_index = 0
        for scene_name, variants in scene_configs.items():
            for variant in variants:
                for time_offset in range(3):  # 每个变体3个时段
                    hour = [21, 22, 23][time_offset]
                    scene_index += 1

                    scenes.append({
                        "annotation_id": f"SCENE{scene_index:05d}",
                        "user_id": f"U{scene_index:05d}",
                        "order_id": f"O{scene_index:05d}",
                        "order_time": f"2026-03-20T{hour}:{random.randint(0,59):02d}:00Z",
                        "order_products": [f"P{scene_index:04d}"],
                        "product_names": variant["products"],
                        "context": {
                            "has_sports_event": variant["has_sports"],
                            "event_name": variant["event"],
                            "weather": random.choice(["晴", "多云", "阴"]),
                            "is_weekend": random.choice([True, False]),
                            "location_type": random.choice(["家中", "公司", "朋友家"]),
                            "user_occupation": random.choice(["上班族", "学生", "自由职业"])
                        },
                        "standard_scene": scene_name,
                        "scene_confidence": random.uniform(0.85, 0.99)
                    })

        return scenes

    def generate_comprehensive_ground_truth(self):
        """生成全面Ground Truth数据"""
        gt_records = []

        # 商品库
        products_lib = [
            ("P0001", "青岛啤酒330ml", "啤酒", 120, 8.5),
            ("P0002", "百威啤酒500ml", "啤酒", 95, 12.0),
            ("P0003", "乐事薯片原味", "薯片", 85, 6.5),
            ("P0004", "洽洽瓜子", "坚果", 65, 15.0),
            ("P0005", "周黑鸭鸭脖", "卤味", 110, 25.0),
            ("P0006", "可口可乐330ml", "碳酸饮料", 70, 3.5),
            ("P0007", "红牛250ml", "功能饮料", 88, 8.0),
            ("P0008", "泡椒凤爪", "卤味", 75, 12.0),
            ("P0009", "农心辛拉面", "速食", 45, 5.5),
            ("P0010", "梦龙冰淇淋", "冰品", 55, 18.0),
            ("P0011", "威士忌", "洋酒", 35, 45.0),
            ("P0012", "奥利奥", "零食", 62, 8.0),
            ("P0013", "东鹏特饮", "功能饮料", 72, 6.0),
            ("P0014", "康师傅泡面", "速食", 58, 4.5),
            ("P0015", "绝味鸭脖", "卤味", 68, 22.0),
        ]

        # 为不同商家生成不同场景的答案（每个商家只有一个场景）
        scene_types = ["看球", "加班", "聚会", "夜宵", "追剧", "游戏", "独饮"]

        for i in range(100):
            # 每个商家ID只生成一条记录
            merchant_id = f"M{i+1:03d}"
            scene_type = scene_types[i % len(scene_types)]

            # 根据场景确定热销商品
            if scene_type == "看球":
                top_products = ["P0001", "P0002", "P0005", "P0003", "P0008"]
            elif scene_type == "加班":
                top_products = ["P0007", "P0013", "P0009", "P0014", "P0006"]
            elif scene_type == "聚会":
                top_products = ["P0001", "P0002", "P0011", "P0004", "P0003"]
            elif scene_type == "夜宵":
                top_products = ["P0005", "P0008", "P0010", "P0015", "P0006"]
            elif scene_type == "追剧":
                top_products = ["P0003", "P0012", "P0006", "P0004", "P0007"]
            elif scene_type == "游戏":
                top_products = ["P0007", "P0013", "P0003", "P0008", "P0006"]
            else:  # 独饮
                top_products = ["P0001", "P0011", "P0005", "P0008", "P0002"]

            # 生成销量数据
            real_sales = {}
            for idx, pid in enumerate(top_products):
                product_info = next((p for p in products_lib if p[0] == pid), products_lib[0])
                name, cat, base, price = product_info[1], product_info[2], product_info[3], product_info[4]

                # 排名靠前的销量高
                actual = base - idx * random.randint(5, 15) + random.randint(-10, 10)
                actual = max(20, actual)  # 最低20

                real_sales[pid] = {
                    "product_name": name,
                    "actual_sales": actual,
                    "sales_change_ratio": random.uniform(0.2, 0.8) if idx < 3 else random.uniform(-0.1, 0.3)
                }

            gt_records.append({
                "gt_id": f"GT{i+1:03d}",
                "merchant_id": merchant_id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "context": {
                    "weather": random.choice(["晴", "多云", "阴"]),
                    "has_sports_event": scene_type == "看球",
                    "event_heat_score": random.randint(60, 95)
                },
                "real_sales_data": real_sales,
                "expected_hot_products": top_products,
                "real_restock_needs": {
                    pid: {
                        "product_name": real_sales[pid]["product_name"],
                        "needed_quantity": int(real_sales[pid]["actual_sales"] * 1.5),
                        "urgency": "high" if idx < 3 else "medium"
                    }
                    for idx, pid in enumerate(top_products[:3])
                }
            })

        return gt_records

    def generate_merchants(self):
        """生成商家数据"""
        merchants = []
        types = ["便利店", "超市", "酒吧", "零食店", "24小时店"]

        for i in range(20):
            merchants.append({
                "merchant_id": f"M{i+1:03d}",
                "merchant_name": f"夜宵便利店{i+1}号店",
                "merchant_type": types[i % len(types)],
                "location": random.choice(["朝阳区", "海淀区", "浦东区", "天河区", "南山区"])
            })

        return merchants

    def save_json(self, data, filename):
        """保存JSON文件"""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  [OK] {filename}")

    def run(self):
        """运行全面数据生成"""
        print("\n" + "="*70)
        print("全面模拟数据生成器")
        print("="*70)
        print("\n目标：生成覆盖所有业务维度的真实数据")

        # 生成商家
        print("\n[1/4] 生成商家数据...")
        merchants = self.generate_merchants()
        self.save_json(merchants, "merchants.json")

        # 生成事件数据
        print("\n[2/4] 生成事件数据...")
        events = self.generate_comprehensive_events()

        # 统计各类型事件
        event_stats = {}
        for e in events:
            cat = e.get("standard_classification", "其他")
            event_stats[cat] = event_stats.get(cat, 0) + 1

        self.save_json({
            "数据集说明": "全面事件标注数据",
            "统计": event_stats,
            "annotations": events
        }, "event_annotations.json")

        print(f"  事件统计: {event_stats}")

        # 生成场景数据
        print("\n[3/4] 生成场景数据...")
        scenes = self.generate_comprehensive_scenes()

        # 统计各场景数量
        scene_stats = {}
        for s in scenes:
            scene = s.get("standard_scene", "其他")
            scene_stats[scene] = scene_stats.get(scene, 0) + 1

        self.save_json({
            "数据集说明": "全面场景标注数据",
            "统计": scene_stats,
            "scene_annotations": scenes
        }, "scene_annotations.json")

        print(f"  场景统计: {scene_stats}")

        # 生成Ground Truth
        print("\n[4/4] 生成Ground Truth数据...")
        gt_records = self.generate_comprehensive_ground_truth()
        self.save_json({
            "数据集说明": "全面Ground Truth数据",
            "ground_truth_records": gt_records
        }, "ground_truth.json")

        print(f"  共 {len(gt_records)} 条答案数据")

        print("\n" + "="*70)
        print("全面数据生成完成!")
        print("="*70)
        print(f"\n数据保存位置: {self.output_dir.absolute()}")
        print("\n数据覆盖:")
        print(f"  - 事件数据: {len(events)} 条 (天气/赛事/娱乐/社会)")
        print(f"  - 场景数据: {len(scenes)} 条 (7种场景全覆盖)")
        print(f"  - 商家数据: {len(merchants)} 家")
        print(f"  - Ground Truth: {len(gt_records)} 条")


if __name__ == "__main__":
    generator = ComprehensiveDataGenerator()
    generator.run()
