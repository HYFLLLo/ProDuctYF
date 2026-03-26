"""
商品匹配服务 - 基于LLM的潜在需求推荐
"""
import json

PRODUCT_MATCHING_PROMPT = """
你是一个商品推荐专家。基于用户场景，为用户推荐可能感兴趣的商品。

用户场景：{scene_type}
场景理由：{scene_reason}
用户历史偏好：{user_preferences}
当前订单：{current_products}

请根据以上信息，推荐3-5个用户可能感兴趣的商品（不在当前订单中）：
请输出JSON格式：
{{
    "recommended_products": [
        {{"product_id": "xxx", "product_name": "xxx", "priority": "高/中/低", "reason": "推荐理由"}}
    ]
}}
"""


class ProductMatcher:
    """商品匹配器"""

    def __init__(self, llm_client=None):
        self.llm = llm_client

    # 场景-商品关联规则（无LLM时的后备）
    SCENE_PRODUCT_RULES = {
        "看球": {
            "啤酒类": ["啤酒", "进口啤酒"],
            "零食类": ["薯片", "花生", "瓜子", "鸡爪"],
            "饮料类": ["可乐", "雪碧"]
        },
        "加班": {
            "泡面类": ["泡面", "自热锅", "螺蛳粉"],
            "能量类": ["红牛", "咖啡", "奶茶"],
            "零食类": ["巧克力", "饼干"]
        },
        "聚会": {
            "酒水类": ["啤酒", "洋酒", "葡萄酒", "饮料"],
            "零食类": ["薯片", "坚果", "糖果"],
            "小吃类": ["鸡翅", "鸭脖"]
        },
        "独饮": {
            "酒水类": ["啤酒", "白酒", "洋酒"],
            "下酒类": ["花生", "卤味", "薯片"]
        },
        "零食": {
            "膨化类": ["薯片", "虾条", "爆米花"],
            "饮料类": ["可乐", "雪碧", "果汁"],
            "糖果类": ["糖果", "巧克力"]
        }
    }

    async def match(
        self,
        scene_type: str,
        scene_reason: str,
        user_preferences: list,
        current_products: list
    ) -> list[dict]:
        """
        匹配商品推荐

        Args:
            scene_type: 场景类型
            scene_reason: 场景判断理由
            user_preferences: 用户历史偏好
            current_products: 当前订单商品

        Returns:
            推荐商品列表
        """
        if self.llm is None:
            return self._rule_based_match(
                scene_type, user_preferences, current_products
            )

        prompt = PRODUCT_MATCHING_PROMPT.format(
            scene_type=scene_type,
            scene_reason=scene_reason,
            user_preferences=", ".join(user_preferences) if user_preferences else "无",
            current_products=", ".join([
                p.get("name", "") for p in current_products
            ])
        )

        try:
            response = await self.llm.agenerate([prompt])
            result = self._parse_response(response)
            return result.get("recommended_products", [])
        except Exception as e:
            print(f"LLM match error: {e}")
            return self._rule_based_match(
                scene_type, user_preferences, current_products
            )

    def _rule_based_match(
        self,
        scene_type: str,
        user_preferences: list,
        current_products: list
    ) -> list[dict]:
        """基于规则的商品匹配"""
        current_names = [p.get("name", "") for p in current_products]
        recommendations = []

        scene_rules = self.SCENE_PRODUCT_RULES.get(scene_type, {})

        for category, products in scene_rules.items():
            for product in products:
                if product not in current_names:
                    # 检查用户偏好
                    priority = "中"
                    if any(pref in product for pref in user_preferences):
                        priority = "高"

                    recommendations.append({
                        "product_id": f"P_{product}",
                        "product_name": product,
                        "priority": priority,
                        "reason": f"基于{scene_type}场景推荐"
                    })

        # 按优先级排序
        priority_order = {"高": 0, "中": 1, "低": 2}
        recommendations.sort(
            key=lambda x: priority_order.get(x["priority"], 1)
        )

        return recommendations[:5]

    def _parse_response(self, response) -> dict:
        """解析LLM响应"""
        try:
            text = response.generations[0].text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except json.JSONDecodeError:
            return {"recommended_products": []}
        except Exception as e:
            print(f"Parse error: {e}")
            return {"recommended_products": []}
