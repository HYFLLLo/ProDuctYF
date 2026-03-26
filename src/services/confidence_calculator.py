"""
置信度计算服务 - 大模型分类置信度计算与校准
详细实现了综合置信度计算、来源可靠性系数、数据完整性系数
"""
import math
from typing import Optional, Dict
from dataclasses import dataclass
from enum import Enum


class ConfidenceLevel(Enum):
    """置信度级别"""
    A_HIGH = "A"  # ≥90% 高可信
    B_MEDIUM = "B"  # 70%-90% 中可信
    C_PENDING = "C"  # 50%-70% 待复核
    D_LOW = "D"  # <50% 低可信


class DataSourceReliability(Enum):
    """数据来源可靠性"""
    HIGH = 1.0
    MEDIUM = 0.85
    LOW = 0.70
    ANONYMOUS = 0.50


class DataCompleteness(Enum):
    """数据完整性"""
    COMPLETE = 1.0
    BASIC_COMPLETE = 0.85
    PARTIAL = 0.70
    SEVERE_MISSING = 0.50


@dataclass
class ConfidenceResult:
    """置信度计算结果"""
    raw_confidence: float
    source_reliability: float
    data_completeness: float
    calibrated_confidence: float
    confidence_level: str
    needs_review: bool
    reasoning: str


class ConfidenceCalculator:
    """
    置信度计算器

    置信度计算公式：
    综合置信度 = 大模型置信度 × 来源可靠性系数 × 数据完整性系数

    置信度分级：
    - A级 (≥90%): 直接采用，无需复核
    - B级 (70%-90%): 正常进入流程
    - C级 (50%-70%): 触发人工复核
    - D级 (<50%): 强制人工复核
    """

    SOURCE_RELIABILITY = {
        "官方天气预报API": 1.0,
        "官方体育赛事API": 1.0,
        "权威新闻媒体": 0.95,
        "社交媒体热搜": 0.85,
        "用户生成内容": 0.70,
        "匿名爆料": 0.50
    }

    DATA_COMPLETENESS = {
        "完全完整": 1.0,
        "基本完整": 0.85,
        "部分缺失": 0.70,
        "严重缺失": 0.50
    }

    CONFIDENCE_THRESHOLDS = {
        "A": 90,
        "B": 70,
        "C": 50,
        "D": 0
    }

    TEMPERATURE_SCALING = 1.2

    def __init__(self):
        pass

    def calculate(
        self,
        raw_confidence: float,
        data_source: str,
        data_completeness_level: str
    ) -> ConfidenceResult:
        """
        计算综合置信度

        Args:
            raw_confidence: 大模型输出的原始置信度 (0-1)
            data_source: 数据来源
            data_completeness_level: 数据完整性级别

        Returns:
            置信度计算结果
        """
        source_reliability = self._get_source_reliability(data_source)
        data_completeness = self._get_data_completeness(data_completeness_level)

        raw_confidence_calibrated = self._apply_temperature_scaling(raw_confidence)

        calibrated_confidence = raw_confidence_calibrated * source_reliability * data_completeness

        confidence_level = self._get_confidence_level(calibrated_confidence)
        needs_review = self._needs_review(confidence_level)
        reasoning = self._generate_reasoning(
            raw_confidence,
            source_reliability,
            data_completeness,
            calibrated_confidence
        )

        return ConfidenceResult(
            raw_confidence=raw_confidence,
            source_reliability=source_reliability,
            data_completeness=data_completeness,
            calibrated_confidence=round(calibrated_confidence, 3),
            confidence_level=confidence_level,
            needs_review=needs_review,
            reasoning=reasoning
        )

    def _get_source_reliability(self, data_source: str) -> float:
        """获取来源可靠性系数"""
        return self.SOURCE_RELIABILITY.get(data_source, 0.7)

    def _get_data_completeness(self, completeness_level: str) -> float:
        """获取数据完整性系数"""
        return self.DATA_COMPLETENESS.get(completeness_level, 0.7)

    def _apply_temperature_scaling(self, raw_confidence: float) -> float:
        """
        应用温度缩放进行置信度校准

        解决大模型过度自信或不够自信的问题
        """
        return pow(raw_confidence, 1 / self.TEMPERATURE_SCALING)

    def _get_confidence_level(self, confidence: float) -> str:
        """获取置信度级别"""
        if confidence >= self.CONFIDENCE_THRESHOLDS["A"] / 100:
            return "A"
        elif confidence >= self.CONFIDENCE_THRESHOLDS["B"] / 100:
            return "B"
        elif confidence >= self.CONFIDENCE_THRESHOLDS["C"] / 100:
            return "C"
        return "D"

    def _needs_review(self, confidence_level: str) -> bool:
        """判断是否需要人工复核"""
        return confidence_level in ["C", "D"]

    def _generate_reasoning(
        self,
        raw_confidence: float,
        source_reliability: float,
        data_completeness: float,
        calibrated_confidence: float
    ) -> str:
        """生成置信度分析理由"""
        reasons = []

        if raw_confidence >= 0.9:
            reasons.append("大模型对分类结果高度确定")
        elif raw_confidence >= 0.7:
            reasons.append("大模型对分类结果中等确定")
        else:
            reasons.append("大模型对分类结果不确定")

        if source_reliability >= 1.0:
            reasons.append("数据来源可靠（官方API/权威媒体）")
        elif source_reliability >= 0.85:
            reasons.append("数据来源中等可靠（社交媒体）")
        else:
            reasons.append("数据来源可靠性较低")

        if data_completeness >= 1.0:
            reasons.append("数据完整")
        elif data_completeness >= 0.85:
            reasons.append("数据基本完整")
        else:
            reasons.append("数据存在缺失")

        reasons.append(f"校准后置信度：{calibrated_confidence*100:.1f}%")

        return "; ".join(reasons)

    def adjust_for_special_cases(
        self,
        confidence: float,
        event_type: str,
        event_heat: Optional[float] = None,
        historical_match: bool = False
    ) -> float:
        """
        针对特殊情况进行置信度调整

        Args:
            confidence: 原始置信度
            event_type: 事件类型
            event_heat: 事件热度
            historical_match: 是否在历史映射表中存在

        Returns:
            调整后的置信度
        """
        adjusted = confidence

        if event_type == "赛事" and event_heat and event_heat > 90:
            if adjusted < 0.8:
                adjusted = 0.8

        if event_type in ["社会", "娱乐"] and event_heat and event_heat > 85:
            if adjusted < 0.6:
                adjusted = 0.6

        if historical_match:
            adjusted = min(1.0, adjusted + 0.1)

        return adjusted

    def calculate_batch(
        self,
        events: list[Dict]
    ) -> list[ConfidenceResult]:
        """
        批量计算置信度

        Args:
            events: 事件列表

        Returns:
            置信度结果列表
        """
        results = []

        for event in events:
            result = self.calculate(
                raw_confidence=event.get("raw_confidence", 0.5),
                data_source=event.get("data_source", "用户生成内容"),
                data_completeness_level=event.get("data_completeness", "部分缺失")
            )
            results.append(result)

        return results

    def get_review_priority(self, confidence_level: str, event_heat: float) -> str:
        """
        获取复核优先级

        Args:
            confidence_level: 置信度级别
            event_heat: 事件热度

        Returns:
            优先级描述
        """
        if confidence_level == "D":
            return "P0"
        elif confidence_level == "C" and event_heat > 90:
            return "P0"
        elif confidence_level == "C":
            return "P1"
        return "P2"

    def get_confidence_statistics(
        self,
        results: list[ConfidenceResult]
    ) -> Dict:
        """
        获取置信度统计信息

        Args:
            results: 置信度结果列表

        Returns:
            统计信息字典
        """
        total = len(results)
        if total == 0:
            return {}

        level_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
        review_count = 0

        for result in results:
            level_counts[result.confidence_level] += 1
            if result.needs_review:
                review_count += 1

        avg_confidence = sum(r.calibrated_confidence for r in results) / total

        return {
            "total_count": total,
            "level_distribution": {
                "A级(高可信)": level_counts["A"],
                "B级(中可信)": level_counts["B"],
                "C级(待复核)": level_counts["C"],
                "D级(低可信)": level_counts["D"]
            },
            "review_rate": f"{review_count / total * 100:.1f}%",
            "average_confidence": f"{avg_confidence * 100:.1f}%"
        }


_confidence_calculator = None

def get_confidence_calculator() -> ConfidenceCalculator:
    """获取置信度计算器实例"""
    global _confidence_calculator
    if _confidence_calculator is None:
        _confidence_calculator = ConfidenceCalculator()
    return _confidence_calculator
