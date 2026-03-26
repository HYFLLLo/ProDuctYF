"""
事件分类服务 - 基于LLM的事件类型分类
"""
import json
from typing import Optional

CLASSIFICATION_PROMPT = """
你是一个事件分类专家。请根据以下事件信息，判断其类型。

事件信息：
- 事件名称：{event_name}
- 事件摘要：{event_summary}
- 发生时间：{event_time}

分类选项：
- 赛事：体育比赛相关事件
- 娱乐：影视、音乐、综艺等娱乐事件
- 天气：天气相关事件
- 社会：社会新闻、热点事件
- 其他：不属于以上类别的事件

请输出JSON格式的分类结果：
{{
    "category": "分类名称",
    "confidence": 0.0-1.0的置信度,
    "reasoning": "分类理由"
}}
"""


class EventClassifier:
    """事件分类器"""

    def __init__(self, llm_client=None):
        self.llm = llm_client

    async def classify(self, event: dict) -> dict:
        """
        对事件进行分类

        Args:
            event: 事件字典，支持多种格式:
                - 标准格式: {name, summary, time}
                - 嵌套格式: {raw_data: {event_name, raw_content}}
                - 测试数据格式: {event_name, event_type, description}

        Returns:
            分类结果字典，包含category, confidence, reasoning
        """
        # 规范化字段名
        normalized = self._normalize_event(event)

        if self.llm is None:
            # 无LLM客户端时，使用规则分类
            return self._rule_based_classify(normalized)

        prompt = CLASSIFICATION_PROMPT.format(
            event_name=normalized.get("name", ""),
            event_summary=normalized.get("summary", ""),
            event_time=normalized.get("time", "")
        )

        try:
            response = await self.llm.agenerate([prompt], agent_type="event_classifier")
            result = self._parse_response(response)
        except Exception as e:
            print(f"LLM classification error: {e}")
            result = self._rule_based_classify(normalized)

        # 置信度低于0.7时标记需要人工复核
        if result["confidence"] < 0.7:
            result["needs_review"] = True

        return result

    def _normalize_event(self, event: dict) -> dict:
        """规范化事件字段名，支持多种数据格式"""
        # 嵌套格式: raw_data.event_name
        if "raw_data" in event:
            raw = event["raw_data"]
            return {
                "name": raw.get("event_name", ""),
                "summary": raw.get("raw_content", ""),
                "time": raw.get("event_time", raw.get("time", ""))
            }

        # 测试数据格式: event_name, event_type
        if "event_name" in event:
            return {
                "name": event.get("event_name", ""),
                "summary": event.get("description", event.get("event_type", "")),
                "time": event.get("start_time", event.get("event_time", ""))
            }

        # 标准格式直接返回
        return {
            "name": event.get("name", ""),
            "summary": event.get("summary", ""),
            "time": event.get("time", "")
        }

    def _rule_based_classify(self, event: dict) -> dict:
        """基于规则的分类作为后备"""
        name = event.get("name", "")
        summary = event.get("summary", "")
        text = f"{name} {summary}".lower()

        # 优先级1：检查事件名称前缀（决定性分类）
        if name.startswith("热点："):
            return {"category": "社会", "confidence": 0.95, "reasoning": "热点前缀优先分类为社会"}
        elif name.startswith("赛事："):
            return {"category": "赛事", "confidence": 0.95, "reasoning": "赛事前缀直接分类"}
        elif name.startswith("天气："):
            return {"category": "天气", "confidence": 0.95, "reasoning": "天气前缀直接分类"}
        elif name.startswith("娱乐："):
            return {"category": "娱乐", "confidence": 0.95, "reasoning": "娱乐前缀直接分类"}

        # 优先级2：关键词匹配
        sports_keywords = ["赛事", "vs", "决赛", "世界杯", "欧冠", "欧洲杯", "联赛", "比赛",
                          "足球", "篮球", "网球", "羽毛球", "乒乓球", "游泳", "田径"]
        entertainment_keywords = ["演唱会", "电影", "电视剧", "综艺", "首映", "颁奖", "红毯",
                                "上映", "播出", "选秀", "综艺"]
        weather_keywords = ["天气", "雨", "雪", "晴", "阴", "风", "台风", "降温", "升温", "温度"]
        social_keywords = ["热点", "热搜", "突发", "新闻", "曝光", "热搜"]

        # 评分机制：多个关键词命中增加置信度
        sports_score = sum(1 for kw in sports_keywords if kw in text)
        entertainment_score = sum(1 for kw in entertainment_keywords if kw in text)
        weather_score = sum(1 for kw in weather_keywords if kw in text)
        social_score = sum(1 for kw in social_keywords if kw in text)

        max_score = max(sports_score, entertainment_score, weather_score, social_score)

        if max_score == 0:
            return {"category": "其他", "confidence": 0.5, "reasoning": "无关键词匹配"}

        # 根据最高分类和得分返回结果
        if sports_score == max_score:
            confidence = min(0.95, 0.7 + sports_score * 0.08)
            return {"category": "赛事", "confidence": confidence, "reasoning": "赛事关键词匹配"}
        elif entertainment_score == max_score:
            confidence = min(0.95, 0.7 + entertainment_score * 0.08)
            return {"category": "娱乐", "confidence": confidence, "reasoning": "娱乐关键词匹配"}
        elif weather_score == max_score:
            confidence = min(0.95, 0.7 + weather_score * 0.08)
            return {"category": "天气", "confidence": confidence, "reasoning": "天气关键词匹配"}
        elif social_score == max_score:
            confidence = min(0.95, 0.7 + social_score * 0.08)
            return {"category": "社会", "confidence": confidence, "reasoning": "社会热点关键词匹配"}
        else:
            return {"category": "其他", "confidence": 0.5, "reasoning": "默认分类"}

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
                # 如果不是JSON格式，使用规则分类作为后备
                return self._rule_based_classify({"name": "", "summary": text})
        except json.JSONDecodeError:
            return {"category": "其他", "confidence": 0.5, "reasoning": "解析失败"}
        except Exception as e:
            print(f"Parse error: {e}")
            return {"category": "其他", "confidence": 0.5, "reasoning": "解析异常"}
