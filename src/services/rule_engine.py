"""
规则引擎模块 - 场景匹配规则
"""

SCENE_RULES = {
    "看球": {
        "conditions": [
            {"type": "order_contains", "category": "啤酒"},
            {"type": "order_contains", "category": "零食"},
            {"type": "event_active", "event_type": "赛事"},
            {"type": "time_range", "start": "20:00", "end": "06:00"}
        ],
        "condition_logic": "AND",
        "weight": 0.8
    },
    "加班": {
        "conditions": [
            {"type": "order_contains", "category": "泡面"},
            {"type": "order_contains", "category": "能量饮料"},
            {"type": "location_type", "value": "写字楼"},
            {"type": "is_workday"},
            {"type": "time_range", "start": "20:00", "end": "23:00"}
        ],
        "condition_logic": "AND",
        "weight": 0.75
    },
    "聚会": {
        "conditions": [
            {"type": "order_count", "operator": ">=", "value": 3},
            {"type": "order_contains", "category": "酒水", "count": 2, "count_operator": ">="},
            {"type": "is_weekend_or_holiday"},
            {"type": "order_total_amount", "operator": ">=", "value": 150}
        ],
        "condition_logic": "AND",
        "weight": 0.85
    },
    "独饮": {
        "conditions": [
            {"type": "order_contains", "category": "酒水"},
            {"type": "order_count", "operator": "<=", "value": 2},
            {"type": "time_range", "start": "22:00", "end": "04:00"}
        ],
        "condition_logic": "AND",
        "weight": 0.7
    },
    "零食": {
        "conditions": [
            {"type": "order_contains", "category": "膨化食品"},
            {"type": "order_contains", "category": "饮料"},
            {"type": "no_specific_time"}
        ],
        "condition_logic": "AND",
        "weight": 0.6
    }
}


class RuleEngine:
    """规则引擎"""

    def __init__(self):
        self.rules = SCENE_RULES

    async def match(
        self,
        user_order: dict,
        user_profile: dict,
        event_context: dict
    ) -> list[dict]:
        """
        匹配用户场景

        Args:
            user_order: 用户订单信息
            user_profile: 用户画像
            event_context: 事件上下文

        Returns:
            匹配的场景列表，按置信度排序
        """
        candidates = []

        for scene_name, rule in self.rules.items():
            match_result = await self._evaluate_rule(
                rule, user_order, user_profile, event_context
            )
            if match_result["matched"]:
                candidates.append({
                    "scene": scene_name,
                    "confidence": match_result["confidence"],
                    "matched_conditions": match_result["matched_conditions"],
                    "weight": rule["weight"]
                })

        # 按置信度×权重排序
        candidates.sort(
            key=lambda x: x["confidence"] * x["weight"],
            reverse=True
        )
        return candidates[:3]  # 返回Top 3候选场景

    async def _evaluate_rule(
        self,
        rule: dict,
        user_order: dict,
        user_profile: dict,
        event_context: dict
    ) -> dict:
        """评估单条规则"""
        matched_conditions = []
        total_confidence = 0

        for condition in rule["conditions"]:
            result = await self._check_condition(
                condition, user_order, user_profile, event_context
            )
            if result["matched"]:
                matched_conditions.append(condition)
                total_confidence += result.get("confidence", 0.8)

        if rule["condition_logic"] == "AND":
            matched = len(matched_conditions) == len(rule["conditions"])
        else:
            matched = len(matched_conditions) > 0

        confidence = (
            total_confidence / len(rule["conditions"])
            if matched and matched_conditions else 0
        )

        return {
            "matched": matched,
            "confidence": confidence,
            "matched_conditions": matched_conditions
        }

    async def _check_condition(
        self,
        condition: dict,
        user_order: dict,
        user_profile: dict,
        event_context: dict
    ) -> dict:
        """检查单个条件"""
        cond_type = condition["type"]

        if cond_type == "order_contains":
            categories = user_order.get("categories", [])
            count = condition.get("count", 1)
            # 优先使用count_operator，没有则用operator
            op = condition.get("count_operator", condition.get("operator", ">="))

            category_count = sum(1 for c in categories if condition["category"] in c)

            if op == ">=":
                matched = category_count >= count
            elif op == "<=":
                matched = category_count <= count
            else:
                matched = category_count >= 1

            return {"matched": matched, "confidence": 0.9}

        elif cond_type == "order_count":
            order_count = len(user_order.get("products", []))
            operator = condition.get("operator", ">=")
            value = condition.get("value", 1)

            if operator == ">=":
                matched = order_count >= value
            elif operator == "<=":
                matched = order_count <= value
            else:
                matched = order_count == value

            return {"matched": matched, "confidence": 0.7}

        elif cond_type == "order_total_amount":
            total = user_order.get("total_amount", 0)
            operator = condition.get("operator", ">=")
            value = condition.get("value", 0)

            if operator == ">=":
                matched = total >= value
            elif operator == "<=":
                matched = total <= value
            else:
                matched = total == value

            return {"matched": matched, "confidence": 0.7}

        elif cond_type == "time_range":
            from datetime import datetime
            current_hour = datetime.now().hour
            start_hour = int(condition["start"].split(":")[0])
            end_hour = int(condition["end"].split(":")[0])

            if start_hour <= end_hour:
                matched = start_hour <= current_hour <= end_hour
            else:
                matched = current_hour >= start_hour or current_hour <= end_hour

            return {"matched": matched, "confidence": 0.7}

        elif cond_type == "is_workday":
            from datetime import datetime
            is_workday = datetime.now().weekday() < 5
            return {"matched": is_workday, "confidence": 0.8}

        elif cond_type == "is_weekend_or_holiday":
            from datetime import datetime
            is_weekend = datetime.now().weekday() >= 5
            return {"matched": is_weekend, "confidence": 0.8}

        elif cond_type == "event_active":
            active_events = event_context.get("active_events", [])
            event_types = [e.get("type") for e in active_events]
            matched = condition["event_type"] in event_types
            return {"matched": matched, "confidence": 0.85}

        elif cond_type == "location_type":
            location = user_profile.get("location_type", "")
            matched = location == condition.get("value", "")
            return {"matched": matched, "confidence": 0.75}

        elif cond_type == "no_specific_time":
            # 没有特定时间要求
            return {"matched": True, "confidence": 0.5}

        return {"matched": False, "confidence": 0}
