"""
场景推理服务 - 基于LLM的场景推理
"""
import json

SCENE_INFERENCE_PROMPT = """
你是一个用户行为分析专家。根据以下用户信息，判断用户当前最可能的消费场景。

用户订单信息：
- 订单商品：{order_products}
- 订单时间：{order_time}
- 订单金额：{order_amount}

当前环境上下文：
- 天气：{weather}
- 正在发生的事件：{active_events}

候选场景：{candidate_scenes}

请分析以上信息，确定最终场景标签，并输出JSON格式：
{{
    "final_scene": "最终确定的场景",
    "confidence": 0.0-1.0,
    "reasoning": "推理理由"
}}
"""


class SceneInference:
    """场景推理引擎"""

    def __init__(self, llm_client=None):
        self.llm = llm_client

    async def infer(
        self,
        user_order: dict,
        candidate_scenes: list[dict],
        event_context: dict
    ) -> dict:
        """
        推理用户场景

        Args:
            user_order: 用户订单信息
            candidate_scenes: 规则引擎匹配的候选场景
            event_context: 事件上下文

        Returns:
            最终场景判断结果
        """
        # 规范化event_context
        normalized_ctx = self._normalize_context(event_context)

        if not candidate_scenes:
            # 无候选场景时，基于上下文推断
            return self._rule_based_inference(user_order, [], normalized_ctx)

        prompt = self._build_prompt(user_order, candidate_scenes, normalized_ctx)

        try:
            response = await self.llm.agenerate([prompt], agent_type="scene_inference")
            result = self._parse_response(response)
        except Exception as e:
            print(f"LLM inference error: {e}")
            result = self._rule_based_inference(user_order, candidate_scenes, normalized_ctx)

        return result

    def _rule_based_inference(
        self,
        user_order: dict,
        candidate_scenes: list[dict],
        event_context: dict
    ) -> dict:
        """基于规则的场景推理 - 精准版"""
        # 获取商品名称列表
        product_names = user_order.get("product_names", [])
        if not product_names:
            # 兼容products格式
            products = user_order.get("products", [])
            product_names = [p.get("name", p.get("product_name", "")) for p in products]

        # 合并为字符串用于关键词匹配
        product_text = " ".join(product_names)

        # 看球场景 - 有赛事或世界杯关键词
        if event_context.get("has_sports_event", False):
            return {
                "final_scene": "看球",
                "confidence": 0.95,
                "reasoning": f"检测到赛事事件: {event_context.get('event_name', '世界杯决赛')}"
            }

        # 计算特征变量
        has_泡面 = any(kw in product_text for kw in ["康师傅", "泡面", "农心", "辛拉面"])
        has_能量饮料 = any(kw in product_text for kw in ["红牛", "东鹏特饮", "魔爪", "脉动"])
        has_凤爪 = "凤爪" in product_text
        has_周黑鸭 = "周黑鸭" in product_text
        has_薯片 = "薯片" in product_text
        has_辣条 = "辣条" in product_text
        has_威士忌 = "威士忌" in product_text
        beer_count = 0
        for name in product_names:
            name_lower = name.lower()
            if any(kw in name_lower for kw in ["啤酒", "百威", "青岛", "雪花", "哈尔滨"]):
                beer_count += 1
        has_瓜子 = "瓜子" in product_text
        product_count = len(product_names)

        # 加班场景 - 红牛/泡面/东鹏/农心（无凤爪）
        if has_能量饮料 and has_泡面 and not has_凤爪:
            return {
                "final_scene": "加班",
                "confidence": 0.90,
                "reasoning": f"检测到加班商品: {[p for p in product_names if '泡面' in p or '东鹏' in p or '脉动' in p][:2]}"
            }

        # 游戏场景 - 能量饮料 + (薯片 或 辣条)，优先级高
        if has_能量饮料 and (has_薯片 or has_辣条):
            return {
                "final_scene": "游戏",
                "confidence": 0.89,
                "reasoning": f"检测到游戏商品: 能量饮料+零食"
            }

        # 独饮场景 - 小瓶酒/RIO/江小白 或 少量商品(1-3个)+单一酒类
        has_独饮酒 = any(kw in product_text for kw in ["江小白", "RIO", "小瓶", "50ml", "100ml"])
        if has_独饮酒:
            return {
                "final_scene": "独饮",
                "confidence": 0.92,
                "reasoning": f"检测到独饮酒类"
            }

        # 独饮场景 - 少量商品(<=3个) + 单一啤酒(无瓜子)
        if beer_count == 1 and product_count <= 3 and not has_瓜子:
            return {
                "final_scene": "独饮",
                "confidence": 0.88,
                "reasoning": f"检测到少量酒类独饮"
            }

        # 聚会场景 - 威士忌(非小瓶) 或 多种酒水(>=2) 或 多种酒水(>=2)+坚果
        if (has_威士忌 and "50ml" not in product_text and "100ml" not in product_text) or beer_count >= 2:
            return {
                "final_scene": "聚会",
                "confidence": 0.92,
                "reasoning": f"检测到聚会商品: 酒水{beer_count}种"
            }

        # 夜宵场景 - 周黑鸭/凤爪/自热火锅/梦龙冰淇淋
        if any(kw in product_text for kw in ["周黑鸭", "凤爪", "泡椒", "自热", "火锅", "梦龙", "冰淇淋"]):
            return {
                "final_scene": "夜宵",
                "confidence": 0.93,
                "reasoning": f"检测到夜宵商品: {[p for p in product_names if '周黑鸭' in p or '凤爪' in p or '自热' in p][:2]}"
            }

        # 追剧场景 - 薯片+奥利奥/可乐（无酒水）
        if "薯片" in product_text and ("奥利奥" in product_text or "可乐" in product_text) and "啤酒" not in product_text:
            return {
                "final_scene": "追剧",
                "confidence": 0.88,
                "reasoning": f"检测到追剧商品: {[p for p in product_names if '薯片' in p or '奥利奥' in p][:2]}"
            }

        # 游戏场景 - 红牛+凤爪（无威士忌）
        if "红牛" in product_text and "凤爪" in product_text:
            return {
                "final_scene": "游戏",
                "confidence": 0.89,
                "reasoning": f"检测到游戏商品: 红牛+凤爪"
            }

        # 默认场景 - 基于商品数量和时间
        hour = self._parse_hour(user_order.get("order_time", ""))
        if hour and hour >= 23:
            return {
                "final_scene": "夜宵",
                "confidence": 0.6,
                "reasoning": "深夜时段，默认夜宵场景"
            }

        return {
            "final_scene": "零食",
            "confidence": 0.5,
            "reasoning": "无特定场景特征"
        }

    def _infer_from_context(self, event_context: dict) -> dict:
        """无候选场景时，基于上下文推断"""
        has_sports = event_context.get("has_sports_event", False)
        if has_sports:
            return {
                "final_scene": "看球",
                "confidence": 0.7,
                "reasoning": "有赛事发生"
            }
        return {
            "final_scene": "零食",
            "confidence": 0.4,
            "reasoning": "无特定上下文"
        }

    def _parse_hour(self, order_time: str) -> int:
        """从订单时间提取小时"""
        if not order_time:
            return None
        try:
            if "T" in order_time:
                return int(order_time.split("T")[1].split(":")[0])
            elif ":" in order_time:
                return int(order_time.split(":")[0])
        except:
            pass
        return None

    def _build_prompt(
        self,
        user_order: dict,
        candidate_scenes: list[dict],
        event_context: dict
    ) -> str:
        """构建推理Prompt"""
        # 规范化event_context字段访问
        normalized_ctx = self._normalize_context(event_context)

        return SCENE_INFERENCE_PROMPT.format(
            order_products=self._format_products(user_order.get("products", [])),
            order_time=user_order.get("order_time", ""),
            order_amount=user_order.get("total_amount", 0),
            weather=normalized_ctx.get("weather", "未知"),
            active_events=normalized_ctx.get("events", "无"),
            candidate_scenes=", ".join([s["scene"] for s in candidate_scenes])
        )

    def _normalize_context(self, event_context: dict) -> dict:
        """规范化事件上下文字段，支持多种数据格式"""
        # 嵌套格式: context.weather, context.event_name
        if "context" in event_context:
            ctx = event_context["context"]
            has_sports = ctx.get("has_sports_event", False)
            event_name = ctx.get("event_name")
            events_str = event_name if (has_sports and event_name) else "无"
            return {
                "weather": ctx.get("weather", "未知"),
                "events": events_str,
                "has_sports_event": has_sports,
                "event_name": event_name
            }

        # 标准格式: event_context.weather, event_context.active_events
        has_sports = event_context.get("has_sports_event", False)
        active_events = event_context.get("active_events", [])
        if isinstance(active_events, list) and active_events:
            events_str = ", ".join([e.get("name", "") for e in active_events if e])
        else:
            events_str = "无"

        return {
            "weather": event_context.get("weather", "未知"),
            "events": events_str,
            "has_sports_event": has_sports,
            "event_name": event_context.get("event_name")
        }

    def _format_products(self, products: list) -> str:
        """格式化商品列表"""
        if not products:
            return "无"
        return ", ".join([
            f"{p.get('name', p.get('product_name', '未知'))}({p.get('category', p.get('category_name', '未知'))})"
            for p in products
        ])

    def _parse_response(self, response) -> dict:
        """解析LLM响应"""
        try:
            # 处理字典格式响应 (我们的LLMClient返回格式)
            if isinstance(response, dict):
                text = response.get("content", "").strip()
            else:
                # 处理LangChain格式响应
                text = response.generations[0].text.strip()
            
            # 尝试提取JSON
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            # 尝试直接解析JSON
            try:
                return json.loads(text.strip())
            except json.JSONDecodeError:
                # 如果不是JSON格式，使用规则推理作为后备
                return self._rule_based_inference({}, [], {})
        except json.JSONDecodeError:
            return {
                "final_scene": "其他",
                "confidence": 0.5,
                "reasoning": "解析失败"
            }
        except Exception as e:
            print(f"Parse error: {e}")
            return {
                "final_scene": "其他",
                "confidence": 0.5,
                "reasoning": "解析异常"
            }
