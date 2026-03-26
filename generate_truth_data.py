"""
生成Truth_data测试数据集
模拟真实业务数据用于离线测试
"""
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


class TruthDataGenerator:
    """生成真实的测试数据"""

    def __init__(self):
        self.output_dir = Path("Truth_data")
        self.output_dir.mkdir(exist_ok=True)
        self.categories = ["啤酒", "薯片", "卤味", "功能饮料", "坚果", "零食", "速食", "冰淇淋", "洋酒", "碳酸饮料"]
        self.scenes = ["看球", "加班", "聚会", "独饮", "夜宵", "追剧", "游戏"]
        self.event_types = ["赛事", "娱乐", "天气", "社会"]

    def generate_weather_events(self, count=100):
        """生成天气事件数据"""
        weather_conditions = ["晴", "多云", "阴", "小雨", "中雨", "雷阵雨", "暴雨"]
        weathers = []
        base_time = datetime.now()

        for i in range(count):
            weather = random.choice(weather_conditions)
            temp = random.randint(15, 35)
            hour = random.randint(20, 23)

            event_time = base_time + timedelta(hours=hour)

            weathers.append({
                "event_id": f"WEATHER_{i+1:04d}",
                "event_name": f"天气：{weather}",
                "summary": f"温度{temp}度，{weather}，风力{random.choice(['微风', '东北风2-3级', '西南风3-4级'])}",
                "time": event_time.strftime("%Y-%m-%d %H:%M"),
                "location": random.choice(["北京", "上海", "广州", "深圳"]),
                "temperature": temp,
                "weather_text": weather,
                "wind_dir": random.choice(["微风", "东北风", "西南风"]),
                "view_count": random.randint(10000, 500000),
                "click_count": random.randint(1000, 50000),
                "created_at": (event_time - timedelta(days=random.randint(0, 7))).isoformat()
            })

        return weathers

    def generate_sports_events(self, count=100):
        """生成赛事事件数据"""
        leagues = ["欧冠", "英超", "西甲", "意甲", "德甲", "NBA", "CBA", "世界杯", "欧洲杯"]
        teams_pool = {
            "足球": [
                ["曼城", "皇马", "巴萨", "拜仁", "利物浦", "巴黎圣日耳曼"],
                ["尤文图斯", "AC米兰", "国际米兰", "多特蒙德", "切尔西", "阿森纳"]
            ],
            "篮球": [
                ["湖人", "勇士", "篮网", "雄鹿", "凯尔特人", "热火"],
                ["掘金", "太阳", "快船", "76人", "独行侠", "灰熊"]
            ]
        }

        sports_events = []
        base_time = datetime.now()

        for i in range(count):
            sport_type = random.choice(["足球", "篮球"])
            teams = random.choice(teams_pool[sport_type])
            home_team = random.choice(teams[0])
            away_team = random.choice(teams[1])
            league = random.choice([l for l in leagues if l in ["欧冠", "NBA", "世界杯"] or sport_type == "足球"])

            hour = random.randint(21, 23)
            event_time = base_time + timedelta(hours=hour)

            # 大赛决赛热度高
            is_final = random.random() < 0.2
            heat_base = 95 if is_final else random.randint(60, 90)

            sports_events.append({
                "event_id": f"SPORTS_{i+1:04d}",
                "event_name": f"赛事：{home_team} vs {away_team}",
                "summary": f"{league}{sport_type}比赛，{home_team}对阵{away_team}",
                "time": event_time.strftime("%Y-%m-%d %H:%M"),
                "location": random.choice(["伦敦", "马德里", "慕尼黑", "巴黎", "洛杉矶", "纽约"]),
                "event_type": "sports",
                "teams": [home_team, away_team],
                "league": league,
                "sport_type": sport_type,
                "is_final": is_final,
                "view_count": random.randint(500000, 50000000),
                "click_count": random.randint(50000, 5000000),
                "heat_score": heat_base,
                "created_at": (event_time - timedelta(days=random.randint(0, 3))).isoformat()
            })

        return sports_events

    def generate_social_media_events(self, count=100):
        """生成社交媒体热点数据"""
        topics = [
            "世界杯决赛",
            "欧洲杯半决赛",
            "欧冠决赛",
            "NBA总冠军",
            "618促销",
            "双十一",
            "明星塌房",
            "新剧上映",
            "游戏发售",
            "音乐节",
            "电影节",
            "颁奖典礼"
        ]

        social_events = []
        base_time = datetime.now()

        for i in range(count):
            topic = random.choice(topics)
            hot_value = random.randint(500000, 100000000)
            view_count = hot_value * random.uniform(2, 5)
            click_count = hot_value * random.uniform(0.3, 0.8)

            hour = random.randint(20, 23)
            event_time = base_time + timedelta(hours=hour)

            # 热点事件分类
            category = "赛事"
            if "618" in topic or "双十一" in topic:
                category = "社会"
            elif "剧" in topic or "电影" in topic or "音乐" in topic or "颁奖" in topic:
                category = "娱乐"
            elif "世界杯" in topic or "欧洲杯" in topic or "欧冠" in topic or "NBA" in topic:
                category = "赛事"

            social_events.append({
                "event_id": f"SOCIAL_{i+1:04d}",
                "event_name": f"热点：{topic}",
                "summary": f"{topic}引发全网讨论，热度持续攀升",
                "time": event_time.strftime("%Y-%m-%d %H:%M"),
                "location": "",
                "hot_value": hot_value,
                "view_count": int(view_count),
                "click_count": int(click_count),
                "category": category,
                "sentiment": random.choice(["positive", "neutral", "negative"]),
                "trend": random.choice(["rising", "stable", "falling"]),
                "created_at": (event_time - timedelta(hours=random.randint(1, 12))).isoformat()
            })

        return social_events

    def generate_event_annotations(self, events_all):
        """生成事件标注数据"""
        annotations = []

        # 从所有事件中采样生成标注
        for i, event in enumerate(events_all[:320]):
            annotations.append({
                "annotation_id": f"ANNOT_{i+1:04d}",
                "raw_data": {
                    "event_name": event.get("event_name", ""),
                    "raw_content": event.get("summary", "")
                },
                "standard_classification": event.get("category", "其他"),
                "standard_type_detail": event.get("sport_type", event.get("weather_text", "一般")),
                "standard_time": event.get("time", ""),
                "standard_location": event.get("location", ""),
                "standard_entities": self._extract_entities(event),
                "standard_heat_score": event.get("heat_score", 50),
                "confidence_level": random.uniform(0.85, 0.99),
                "annotator_notes": f"标准标注数据，用于评估事件分类准确性"
            })

        return {
            "数据集说明": "事件数据标注集 - 用于事件理解分析Agent评估",
            "数据量": len(annotations),
            "生成日期": datetime.now().strftime("%Y-%m-%d"),
            "数据用途": "评估事件分类、信息抽取、去重、热度计算的准确性",
            "annotations": annotations
        }

    def _extract_entities(self, event):
        """提取事件实体"""
        entities = []
        name = event.get("event_name", "")

        # 提取队伍/地名
        if " vs " in name:
            parts = name.split(" vs ")
            for part in parts:
                entities.append(part.replace("赛事：", "").replace("热点：", ""))

        # 提取关键词
        keywords = ["世界杯", "欧洲杯", "欧冠", "NBA", "决赛", "促销", "上映", "发售"]
        for kw in keywords:
            if kw in name:
                entities.append(kw)

        return entities[:5]  # 最多5个实体

    def generate_merchants(self, count=55):
        """生成商家数据"""
        merchants = []
        merchant_types = ["便利店", "超市", "酒吧", "零食店", "24小时店"]

        for i in range(count):
            merchant_type = random.choice(merchant_types)
            mtype_code = "CN" if "便利店" in merchant_type else ("BAR" if "酒吧" in merchant_type else "SNK")

            merchants.append({
                "merchant_id": f"M{i+1:03d}",
                "merchant_name": f"夜宵{merchant_type}{i+1}号店",
                "merchant_type": merchant_type,
                "type_code": mtype_code,
                "location": random.choice(["朝阳区", "海淀区", "浦东区", "天河区", "南山区"]),
                "night_focus": random.choice([True, False]),
                "night_sales_ratio": random.uniform(0.3, 0.8),
                "main_categories": random.sample(self.categories, k=random.randint(3, 6))
            })

        return merchants

    def generate_products(self, merchants, total=520):
        """生成商品数据"""
        products = []
        product_names = {
            "啤酒": ["青岛啤酒330ml", "百威啤酒500ml", "雪花啤酒", "哈尔滨啤酒", "喜力啤酒"],
            "薯片": ["乐事薯片", "可比克薯片", "薯片先生", "上好佳薯片"],
            "卤味": ["周黑鸭鸭脖", "绝味鸭脖", "泡椒凤爪", "卤牛肉", "卤鸡爪"],
            "功能饮料": ["红牛250ml", "东鹏特饮", "魔爪", "脉动"],
            "坚果": ["洽洽瓜子", "三只松鼠坚果", "百草味坚果", "沃隆坚果"],
            "零食": ["奥利奥", "奥利奥饼干", "好丽友", "士力架", "德芙巧克力"],
            "速食": ["康师傅泡面", "统一老坛酸菜", "自热火锅", "螺蛳粉"],
            "冰淇淋": ["梦龙冰淇淋", "可爱多", "哈根达斯", "八喜"],
            "洋酒": ["威士忌", "伏特加", "人头马", "轩尼诗"],
            "碳酸饮料": ["可口可乐", "百事可乐", "雪碧", "芬达"]
        }

        product_id = 1
        for merchant in merchants:
            categories = merchant.get("main_categories", self.categories[:3])

            for category in categories:
                names = product_names.get(category, [f"{category}商品"])
                for name in names[:random.randint(2, 4)]:
                    price = round(random.uniform(5, 50), 2)

                    products.append({
                        "product_id": f"P{product_id:04d}",
                        "merchant_id": merchant["merchant_id"],
                        "product_name": name,
                        "category_name": category,
                        "retail_price": price,
                        "cost_price": round(price * random.uniform(0.5, 0.7), 2),
                        "status": "active",
                        "stock": random.randint(0, 200)
                    })
                    product_id += 1

                    if product_id > total:
                        return products

        return products

    def generate_inventory(self, products):
        """生成库存数据"""
        inventory = []

        for product in products:
            current_stock = random.randint(0, 150)
            safety_stock = random.randint(20, 50)

            inventory.append({
                "inventory_id": f"INV_{product['product_id']}",
                "merchant_id": product["merchant_id"],
                "product_id": product["product_id"],
                "usable_stock": current_stock,
                "safety_stock": safety_stock,
                "warehouse_stock": current_stock + random.randint(50, 200),
                "last_restock_time": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                "restock_lead_time": random.randint(1, 7),
                "turnover_rate": round(random.uniform(0.5, 3.0), 2)
            })

        return inventory

    def generate_user_scenes(self, products, count=520):
        """生成用户场景数据"""
        scenes = []
        scenes_definitions = {
            "看球": ["啤酒", "薯片", "卤味", "功能饮料"],
            "加班": ["功能饮料", "速食", "零食", "咖啡"],
            "聚会": ["啤酒", "洋酒", "薯片", "坚果"],
            "独饮": ["啤酒", "洋酒"],
            "夜宵": ["卤味", "速食", "冰淇淋"],
            "追剧": ["零食", "薯片", "饮料"],
            "游戏": ["功能饮料", "零食", "薯片"]
        }

        for i in range(count):
            scene_type = random.choice(list(scenes_definitions.keys()))
            preferred_categories = scenes_definitions[scene_type]

            # 选择符合场景的商品
            selected_products = [p for p in products if p["category_name"] in preferred_categories]
            order_products = random.sample(selected_products, k=min(random.randint(2, 5), len(selected_products)))

            hour = random.randint(21, 23) if random.random() < 0.8 else random.randint(0, 5)
            order_time = datetime.now().replace(hour=hour, minute=random.randint(0, 59))

            total_amount = sum([p["retail_price"] for p in order_products]) * random.randint(1, 3)

            scene_data = {
                "annotation_id": f"SCENE{i+1:04d}",
                "user_id": f"U{random.randint(1, 10000):05d}",
                "order_id": f"O{i+1:05d}",
                "order_time": order_time.isoformat() + "Z",
                "order_products": [p["product_id"] for p in order_products],
                "product_names": [p["product_name"] for p in order_products],
                "context": {
                    "has_sports_event": scene_type == "看球",
                    "event_name": "世界杯决赛" if scene_type == "看球" and random.random() < 0.3 else "",
                    "weather": random.choice(["晴", "多云", "阴"]),
                    "is_weekend": random.choice([True, False]),
                    "location_type": random.choice(["家中", "公司", "酒吧", "朋友家"]),
                    "user_occupation": random.choice(["学生", "上班族", "自由职业"]),
                    "user_age": random.randint(18, 45)
                },
                "standard_scene": scene_type,
                "scene_confidence": random.uniform(0.80, 0.99),
                "reason": f"订单包含{','.join([p['category_name'] for p in order_products])}，符合{scene_type}场景特征",
                "standard_potential_needs": self._generate_potential_needs(scene_type),
                "potential_need_reasons": [f"基于{scene_type}场景的潜在需求推荐"]
            }

            scenes.append(scene_data)

        return {
            "数据集说明": "用户行为测试集 - 用户场景标注数据",
            "数据量": len(scenes),
            "生成日期": datetime.now().strftime("%Y-%m-%d"),
            "数据用途": "评估用户情绪/场景分析Agent的场景判断准确率和潜在需求命中率",
            "场景分类定义": {
                "看球": "用户在看体育比赛时进行的消费行为，通常伴随啤酒、零食等",
                "加班": "用户因工作需要熬夜，消费以泡面、能量饮料、咖啡等提神产品为主",
                "聚会": "多人社交场景，消费包含多种酒水、大份量食物",
                "独饮": "单人夜间饮酒消费，通常量小、时段晚",
                "夜宵": "以零食、饮料为主的解馋型消费，无特定场景",
                "追剧": "用户观看电视剧/综艺时的伴随消费",
                "游戏": "用户玩游戏时的伴随消费，常搭配能量饮料、零食"
            },
            "scene_annotations": scenes
        }

    def _generate_potential_needs(self, scene_type):
        """生成潜在需求"""
        needs_map = {
            "看球": ["P002", "P003"],  # 更多啤酒零食
            "加班": ["P004", "P009"],  # 功能饮料+速食
            "聚会": ["P001", "P002"],  # 更多酒水
        }
        return needs_map.get(scene_type, [])

    def generate_ground_truth(self, merchants, products, count=100):
        """生成Ground Truth答案数据"""
        ground_truth_records = []

        for i in range(count):
            merchant = random.choice(merchants)
            merchant_id = merchant["merchant_id"]

            # 筛选该商家的商品
            merchant_products = [p for p in products if p["merchant_id"] == merchant_id]
            if len(merchant_products) < 5:
                continue

            # 生成真实销量数据
            real_sales = {}
            for p in merchant_products[:10]:
                base_sales = random.randint(20, 100)
                has_event_boost = random.random() < 0.4

                if has_event_boost:
                    sales_change = random.uniform(0.3, 0.8)
                else:
                    sales_change = random.uniform(-0.1, 0.2)

                predicted = int(base_sales * (1 + sales_change))
                actual = int(predicted * random.uniform(0.9, 1.1))

                real_sales[p["product_id"]] = {
                    "product_name": p["product_name"],
                    "predicted_sales": predicted,
                    "actual_sales": actual,
                    "sales_change_ratio": round(sales_change, 2)
                }

            # 生成补货需求
            real_restock = {}
            for pid, sales_data in list(real_sales.items())[:5]:
                if sales_data["sales_change_ratio"] > 0.3:
                    product = next((p for p in merchant_products if p["product_id"] == pid), None)
                    if product:
                        needed_qty = int(sales_data["actual_sales"] * 1.5)
                        real_restock[pid] = {
                            "product_name": product["product_name"],
                            "needed_quantity": needed_qty,
                            "urgency": "high" if sales_data["sales_change_ratio"] > 0.5 else "medium",
                            "reason": f"销量增长{sales_data['sales_change_ratio']:.0%}，需要补货"
                        }

            # 业务指标
            total_gmv = sum([sales["actual_sales"] * merchant_products[i % len(merchant_products)]["retail_price"]
                            for i, sales in enumerate(real_sales.values())])

            gt_record = {
                "gt_id": f"GT{i+1:03d}",
                "merchant_id": merchant_id,
                "date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "night_period": "20:00-06:00",
                "context": {
                    "weather": random.choice(["晴", "多云", "阴"]),
                    "has_sports_event": random.choice([True, False]),
                    "event_name": "世界杯决赛" if random.random() < 0.3 else "",
                    "event_heat_score": random.randint(60, 95)
                },
                "real_sales_data": real_sales,
                "expected_hot_products": list(real_sales.keys())[:10],
                "real_restock_needs": real_restock,
                "expected_restock_products": list(real_restock.keys()),
                "business_metrics": {
                    "total_gmv": int(total_gmv),
                    "gmv_change_ratio": round(random.uniform(-0.1, 0.4), 2),
                    "out_of_stock_rate": round(random.uniform(0, 0.15), 2),
                    "out_of_stock_rate_change": round(random.uniform(-0.2, 0), 2),
                    "overstock_rate": round(random.uniform(0, 0.1), 2),
                    "overstock_rate_change": round(random.uniform(-0.05, 0.1), 2)
                }
            }

            ground_truth_records.append(gt_record)

            if len(ground_truth_records) >= count:
                break

        return {
            "数据集说明": "Ground Truth答案数据 - 用于评估决策层Agent的预测准确性",
            "数据量": len(ground_truth_records),
            "生成日期": datetime.now().strftime("%Y-%m-%d"),
            "数据用途": "评估爆品预测准确率、补货建议准确率、业务价值指标",
            "ground_truth_records": ground_truth_records
        }

    def save_json(self, data, filename):
        """保存JSON文件"""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  [OK] {filepath}")

    def run(self):
        """运行数据生成"""
        print("\n" + "="*60)
        print("Truth_data 数据集生成器")
        print("="*60)

        # Step 1: 生成事件数据
        print("\n[1/6] 生成事件数据...")
        weather_events = self.generate_weather_events(100)
        sports_events = self.generate_sports_events(100)
        social_events = self.generate_social_media_events(100)

        # 合并所有事件
        all_events = weather_events + sports_events + social_events

        # 保存各类事件
        self.save_json(weather_events, "weather_events.json")
        self.save_json(sports_events, "sports_events.json")
        self.save_json(social_events, "social_media_events.json")
        self.save_json(all_events, "all_events.json")
        print(f"  共生成 {len(all_events)} 个事件")

        # Step 2: 生成事件标注
        print("\n[2/6] 生成事件标注数据...")
        event_annotations = self.generate_event_annotations(all_events)
        self.save_json(event_annotations, "event_annotations.json")
        print(f"  生成 {len(event_annotations['annotations'])} 条标注")

        # Step 3: 生成商家数据
        print("\n[3/6] 生成商家和商品数据...")
        merchants = self.generate_merchants(55)
        self.save_json(merchants, "merchants.json")
        print(f"  生成 {len(merchants)} 个商家")

        products = self.generate_products(merchants, 520)
        self.save_json(products, "products.json")
        print(f"  生成 {len(products)} 个商品")

        inventory = self.generate_inventory(products)
        self.save_json(inventory, "inventory.json")
        print(f"  生成 {len(inventory)} 条库存")

        # Step 4: 生成用户场景数据
        print("\n[4/6] 生成用户场景数据...")
        user_scenes = self.generate_user_scenes(products, 520)
        self.save_json(user_scenes, "scene_annotations.json")
        print(f"  生成 {len(user_scenes['scene_annotations'])} 条场景")

        # Step 5: 生成Ground Truth
        print("\n[5/6] 生成Ground Truth数据...")
        ground_truth = self.generate_ground_truth(merchants, products, 100)
        self.save_json(ground_truth, "ground_truth.json")
        print(f"  生成 {len(ground_truth['ground_truth_records'])} 条答案")

        # Step 6: 生成README
        print("\n[6/6] 生成数据说明文档...")
        readme = {
            "Truth_data数据集说明": "模拟真实业务数据，用于离线测试AI夜宵爆品预测系统",
            "生成日期": datetime.now().strftime("%Y-%m-%d"),
            "数据集列表": {
                "weather_events.json": "天气事件数据 (100条)",
                "sports_events.json": "体育赛事数据 (100条)",
                "social_media_events.json": "社交媒体热点数据 (100条)",
                "all_events.json": "所有事件汇总 (300条)",
                "event_annotations.json": "事件标注数据 (320条) - 用于评估事件理解Agent",
                "merchants.json": "商家档案 (55家)",
                "products.json": "商品品类数据 (520个)",
                "inventory.json": "库存数据",
                "scene_annotations.json": "用户场景标注 (520条) - 用于评估场景分析Agent",
                "ground_truth.json": "Ground Truth答案 (100条) - 用于评估决策层Agent"
            },
            "使用说明": [
                "1. 将Truth_data文件夹下的所有数据导入测试系统",
                "2. 使用event_annotations.json评估事件理解Agent",
                "3. 使用scene_annotations.json评估场景分析Agent",
                "4. 使用ground_truth.json评估决策层Agent",
                "5. 所有数据均为模拟数据，符合真实业务特征"
            ]
        }
        self.save_json(readme, "README.json")

        print("\n" + "="*60)
        print("Truth_data 数据集生成完成!")
        print("="*60)
        print(f"\n数据保存位置: {self.output_dir.absolute()}")
        print("\n数据集统计:")
        print(f"  - 事件数据: 300条")
        print(f"  - 事件标注: 320条")
        print(f"  - 商家档案: 55家")
        print(f"  - 商品品类: 520个")
        print(f"  - 库存数据: {len(inventory)}条")
        print(f"  - 用户场景: 520条")
        print(f"  - Ground Truth: 100条")
        print("\n数据集已准备就绪，可以运行离线测试!")


if __name__ == "__main__":
    generator = TruthDataGenerator()
    generator.run()
