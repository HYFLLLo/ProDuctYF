"""
置信度计算服务测试
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from src.services.confidence_calculator import ConfidenceCalculator, ConfidenceLevel


class TestConfidenceCalculator:
    """测试置信度计算服务"""

    def setup_method(self):
        """初始化测试环境"""
        self.calculator = ConfidenceCalculator()

    def test_calculate_high_confidence(self):
        """测试高置信度计算"""
        result = self.calculator.calculate(
            raw_confidence=0.95,
            data_source="官方体育赛事API",
            data_completeness_level="完全完整"
        )

        assert result.raw_confidence == 0.95
        assert result.source_reliability == 1.0
        assert result.data_completeness == 1.0
        assert result.confidence_level == "A"
        assert result.needs_review == False
        assert result.calibrated_confidence > 0.8

    def test_calculate_medium_confidence(self):
        """测试中等置信度计算"""
        result = self.calculator.calculate(
            raw_confidence=0.85,
            data_source="官方体育赛事API",
            data_completeness_level="完全完整"
        )

        assert result.confidence_level == "B"
        assert result.needs_review == False
        assert "可靠" in result.reasoning

    def test_calculate_low_confidence_social_media(self):
        """测试低置信度：社交媒体数据"""
        result = self.calculator.calculate(
            raw_confidence=0.65,
            data_source="社交媒体热搜",
            data_completeness_level="基本完整"
        )

        assert result.confidence_level == "C"
        assert result.needs_review == True

    def test_calculate_low_confidence_anonymous(self):
        """测试低置信度：匿名爆料"""
        result = self.calculator.calculate(
            raw_confidence=0.90,
            data_source="匿名爆料",
            data_completeness_level="严重缺失"
        )

        assert result.confidence_level == "D"
        assert result.needs_review == True
        assert result.calibrated_confidence < 0.3

    def test_source_reliability_mapping(self):
        """测试数据来源可靠性映射"""
        assert self.calculator._get_source_reliability("官方天气预报API") == 1.0
        assert self.calculator._get_source_reliability("权威新闻媒体") == 0.95
        assert self.calculator._get_source_reliability("社交媒体热搜") == 0.85
        assert self.calculator._get_source_reliability("用户生成内容") == 0.70
        assert self.calculator._get_source_reliability("匿名爆料") == 0.50
        assert self.calculator._get_source_reliability("未知来源") == 0.70

    def test_data_completeness_mapping(self):
        """测试数据完整性映射"""
        assert self.calculator._get_data_completeness("完全完整") == 1.0
        assert self.calculator._get_data_completeness("基本完整") == 0.85
        assert self.calculator._get_data_completeness("部分缺失") == 0.70
        assert self.calculator._get_data_completeness("严重缺失") == 0.50
        assert self.calculator._get_data_completeness("未知") == 0.70

    def test_temperature_scaling(self):
        """测试温度缩放"""
        raw = 0.85
        scaled = self.calculator._apply_temperature_scaling(raw)
        assert scaled > raw
        assert scaled < 1.0

    def test_confidence_level_boundaries(self):
        """测试置信度级别边界"""
        assert self.calculator._get_confidence_level(0.95) == "A"
        assert self.calculator._get_confidence_level(0.90) == "A"
        assert self.calculator._get_confidence_level(0.89) == "B"
        assert self.calculator._get_confidence_level(0.70) == "B"
        assert self.calculator._get_confidence_level(0.69) == "C"
        assert self.calculator._get_confidence_level(0.50) == "C"
        assert self.calculator._get_confidence_level(0.49) == "D"

    def test_needs_review_logic(self):
        """测试是否需要复核"""
        assert self.calculator._needs_review("A") == False
        assert self.calculator._needs_review("B") == False
        assert self.calculator._needs_review("C") == True
        assert self.calculator._needs_review("D") == True

    def test_adjust_for_special_cases_sports_event(self):
        """测试特殊调整：赛事事件"""
        adjusted = self.calculator.adjust_for_special_cases(
            confidence=0.70,
            event_type="赛事",
            event_heat=95
        )
        assert adjusted >= 0.8

        adjusted2 = self.calculator.adjust_for_special_cases(
            confidence=0.75,
            event_type="赛事",
            event_heat=85
        )
        assert adjusted2 == 0.75

    def test_adjust_for_special_cases_historical_match(self):
        """测试特殊调整：历史匹配"""
        adjusted = self.calculator.adjust_for_special_cases(
            confidence=0.60,
            event_type="其他",
            historical_match=True
        )
        assert adjusted == 0.70

        adjusted2 = self.calculator.adjust_for_special_cases(
            confidence=0.95,
            event_type="其他",
            historical_match=True
        )
        assert adjusted2 == 1.0

    def test_batch_calculate(self):
        """测试批量计算"""
        events = [
            {
                "raw_confidence": 0.95,
                "data_source": "官方体育赛事API",
                "data_completeness": "完全完整"
            },
            {
                "raw_confidence": 0.75,
                "data_source": "社交媒体热搜",
                "data_completeness": "基本完整"
            },
            {
                "raw_confidence": 0.50,
                "data_source": "匿名爆料",
                "data_completeness": "部分缺失"
            }
        ]

        results = self.calculator.calculate_batch(events)

        assert len(results) == 3
        assert results[0].confidence_level == "A"
        assert results[1].confidence_level in ["B", "C"]
        assert results[2].confidence_level in ["C", "D"]

    def test_get_review_priority(self):
        """测试复核优先级"""
        assert self.calculator.get_review_priority("D", 50) == "P0"
        assert self.calculator.get_review_priority("C", 95) == "P0"
        assert self.calculator.get_review_priority("C", 70) == "P1"
        assert self.calculator.get_review_priority("B", 80) == "P2"

    def test_get_confidence_statistics(self):
        """测试置信度统计"""
        results = [
            self.calculator.calculate(0.95, "官方体育赛事API", "完全完整"),
            self.calculator.calculate(0.85, "权威新闻媒体", "完全完整"),
            self.calculator.calculate(0.65, "社交媒体热搜", "基本完整"),
            self.calculator.calculate(0.45, "匿名爆料", "部分缺失")
        ]

        stats = self.calculator.get_confidence_statistics(results)

        assert stats["total_count"] == 4
        assert "A级(高可信)" in stats["level_distribution"]
        assert "D级(低可信)" in stats["level_distribution"]
        assert "review_rate" in stats
        assert "average_confidence" in stats

    def test_generate_reasoning(self):
        """测试生成分析理由"""
        reasoning = self.calculator._generate_reasoning(
            raw_confidence=0.95,
            source_reliability=1.0,
            data_completeness=1.0,
            calibrated_confidence=0.9
        )

        assert "高度确定" in reasoning
        assert "可靠" in reasoning
        assert "完整" in reasoning
        assert "90.0%" in reasoning


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
