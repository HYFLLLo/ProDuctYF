"""
热度计算服务 - 事件热度计算与衰减（增强版）
详细实现了多平台热度融合、标准化处理、时间衰减
"""
import math
from datetime import datetime, timedelta
from typing import Optional, Dict, List


class HeatCalculator:
    """
    事件热度计算器（增强版）

    热度计算流程：
    1. 多平台热度数据获取
    2. 基础热度计算（浏览量40% + 点击量60%）
    3. 热度标准化处理（对数变换 + Min-Max标准化）
    4. 时间衰减（指数衰减模型）
    5. 最终热度输出
    """

    WEIGHTS = {
        "view_count": 0.4,
        "click_count": 0.6
    }

    PLATFORM_WEIGHTS = {
        "微博": 0.30,
        "抖音": 0.25,
        "新闻媒体": 0.25,
        "搜索引擎": 0.20
    }

    DECAY_CONFIG = {
        "half_life_hours": 6,
        "base_decay": 0.95
    }

    EVENT_TYPE_HALF_LIFE = {
        "突发新闻": 9,
        "体育赛事": 18,
        "娱乐热点": 36,
        "节日庆典": 60,
        "常规天气": 24
    }

    HEAT_THRESHOLDS = {
        "A": 90,
        "B": 80,
        "C": 70,
        "D": 60,
        "E": 50,
        "F": 0
    }

    def __init__(self, redis_client=None):
        self.redis = redis_client

    def calculate(self, event: dict) -> float:
        """
        计算事件热度值（基础版）

        Args:
            event: 事件字典，包含view_count, click_count, created_at等

        Returns:
            0-100标准化热度值
        """
        view_count = event.get("view_count", 0)
        click_count = event.get("click_count", 0)

        raw_heat = (
            view_count * self.WEIGHTS["view_count"] +
            click_count * self.WEIGHTS["click_count"]
        )

        normalized_heat = self._normalize(raw_heat)

        age_hours = self._get_event_age_hours(event)
        decayed_heat = self._apply_decay(normalized_heat, age_hours)

        return round(decayed_heat, 2)

    def calculate_enhanced(
        self,
        platform_data: Dict[str, Dict],
        event_created_at: datetime,
        event_type: Optional[str] = None,
        current_time: Optional[datetime] = None
    ) -> Dict:
        """
        增强版热度计算

        Args:
            platform_data: 多平台热度数据
                {
                    "微博": {"浏览量": 1200000, "点赞量": 85000, "转发量": 32000, "评论量": 15000},
                    "抖音": {"浏览量": 5600000, "点赞量": 230000, "转发量": 45000, "评论量": 67000},
                    "百度": {"搜索指数": 85000, "资讯指数": 120000}
                }
            event_created_at: 事件创建时间
            event_type: 事件类型
            current_time: 当前时间（默认now）

        Returns:
            包含完整热度信息的字典
        """
        if current_time is None:
            current_time = datetime.now()

        raw_heat = self._calculate_platform_heat(platform_data)

        normalized_heat = self._normalize(raw_heat)

        half_life = self.EVENT_TYPE_HALF_LIFE.get(event_type, 24) if event_type else 24
        age_hours = (current_time - event_created_at).total_seconds() / 3600
        decayed_heat = self._apply_decay(normalized_heat, age_hours, half_life)

        heat_level = self._get_heat_level(decayed_heat)

        return {
            "raw_heat": raw_heat,
            "normalized_heat": round(normalized_heat, 2),
            "decayed_heat": round(decayed_heat, 2),
            "heat_level": heat_level,
            "heat_level_desc": self._get_heat_level_desc(heat_level),
            "half_life_hours": half_life,
            "age_hours": round(age_hours, 2)
        }

    def _calculate_platform_heat(self, platform_data: Dict[str, Dict]) -> float:
        """
        计算多平台综合热度

        公式：综合热度 = Σ(平台热度 × 平台权重)
        """
        total_heat = 0.0

        for platform, data in platform_data.items():
            platform_heat = self._calculate_single_platform_heat(platform, data)
            platform_weight = self.PLATFORM_WEIGHTS.get(platform, 0.2)
            total_heat += platform_heat * platform_weight

        return total_heat

    def _calculate_single_platform_heat(self, platform: str, data: Dict) -> float:
        """
        计算单个平台热度

        公式：平台热度 = 浏览量×40% + 点击量×60%
        """
        browse_count = data.get("浏览量", data.get("浏览量", 0))
        click_metrics = data.get("点赞量", 0) + data.get("转发量", 0) * 2 + data.get("评论量", 0) * 3

        return browse_count * self.WEIGHTS["view_count"] + click_metrics * self.WEIGHTS["click_count"]

    def _normalize(self, raw_heat: float, reference_data: Optional[List[float]] = None) -> float:
        """
        对原始热度值进行标准化处理

        方法：对数变换 + Min-Max标准化
        """
        log_heat = math.log1p(raw_heat)

        if reference_data:
            log_reference = [math.log1p(h) for h in reference_data]
            log_max = max(log_reference)
            log_min = min(log_reference)

            if log_max == log_min:
                return 50

            normalized = ((log_heat - log_min) / (log_max - log_min)) * 100
        else:
            max_log = math.log1p(1000000)
            normalized = (log_heat / max_log) * 100

        return min(100, max(0, normalized))

    def _apply_decay(
        self,
        heat: float,
        age_hours: float,
        half_life_hours: Optional[float] = None
    ) -> float:
        """
        应用时间衰减

        公式：decay_factor = exp(-0.693 × age_hours / half_life_hours)
        """
        if half_life_hours is None:
            half_life_hours = self.DECAY_CONFIG["half_life_hours"]

        decay_factor = math.exp(-0.693 * age_hours / half_life_hours)
        return heat * decay_factor

    def _get_event_age_hours(self, event: dict) -> float:
        """计算事件年龄（小时）"""
        created_at = event.get("created_at", datetime.now())
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except:
                created_at = datetime.now()
        elif not isinstance(created_at, datetime):
            created_at = datetime.now()

        age = datetime.now() - created_at
        return age.total_seconds() / 3600

    def _get_heat_level(self, heat: float) -> str:
        """获取热度级别"""
        if heat > self.HEAT_THRESHOLDS["A"]:
            return "A"
        elif heat > self.HEAT_THRESHOLDS["B"]:
            return "B"
        elif heat > self.HEAT_THRESHOLDS["C"]:
            return "C"
        elif heat > self.HEAT_THRESHOLDS["D"]:
            return "D"
        elif heat > self.HEAT_THRESHOLDS["E"]:
            return "E"
        return "F"

    def _get_heat_level_desc(self, level: str) -> str:
        """获取热度级别描述"""
        desc_map = {
            "A": "🔥🔥🔥 极高热 - 自动触发爆品预警",
            "B": "🔥🔥 高热 - 强烈推荐进入爆品清单",
            "C": "🔥 中高热 - 建议纳入爆品清单",
            "D": "🔵 中热 - 观察是否上升",
            "E": "🔵 中低热 - 标记为观察对象",
            "F": "⚪ 低热 - 不进入爆品预测"
        }
        return desc_map.get(level, "")

    def calculate_with_event_type(
        self,
        event: dict,
        event_type: str
    ) -> dict:
        """
        计算带事件类型因子的热度
        """
        base_heat = self.calculate(event)

        type_factors = {
            "赛事": 1.2,
            "娱乐": 1.1,
            "天气": 1.0,
            "社会": 0.9,
            "其他": 0.8
        }

        factor = type_factors.get(event_type, 1.0)
        adjusted_heat = min(100, base_heat * factor)

        return {
            "raw_heat": base_heat,
            "adjusted_heat": round(adjusted_heat, 2),
            "type_factor": factor
        }

    def should_trigger_alert(self, heat: float) -> bool:
        """
        判断是否应该触发爆品预警

        Args:
            heat: 热度值

        Returns:
            True if should trigger alert
        """
        return heat > self.HEAT_THRESHOLDS["A"]
