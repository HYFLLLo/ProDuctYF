"""
事件热度计算服务增强版测试
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from datetime import datetime, timedelta
from src.services.heat_calculator import HeatCalculator


class TestHeatCalculator:
    """测试事件热度计算服务（增强版）"""

    def setup_method(self):
        """初始化测试环境"""
        self.calculator = HeatCalculator()

    def test_calculate_basic(self):
        """测试基础热度计算"""
        event = {
            "view_count": 100000,
            "click_count": 50000,
            "created_at": datetime.now() - timedelta(hours=2)
        }

        heat = self.calculator.calculate(event)
        assert 0 <= heat <= 100
        assert isinstance(heat, float)

    def test_calculate_with_zero_counts(self):
        """测试零值热度计算"""
        event = {
            "view_count": 0,
            "click_count": 0,
            "created_at": datetime.now()
        }

        heat = self.calculator.calculate(event)
        assert heat == 0

    def test_calculate_enhanced_basic(self):
        """测试增强版热度计算"""
        platform_data = {
            "微博": {
                "浏览量": 1200000,
                "点赞量": 85000,
                "转发量": 32000,
                "评论量": 15000
            },
            "抖音": {
                "浏览量": 5600000,
                "点赞量": 230000,
                "转发量": 45000,
                "评论量": 67000
            }
        }

        event_time = datetime.now() - timedelta(hours=6)
        result = self.calculator.calculate_enhanced(
            platform_data=platform_data,
            event_created_at=event_time,
            event_type="体育赛事"
        )

        assert "raw_heat" in result
        assert "normalized_heat" in result
        assert "decayed_heat" in result
        assert "heat_level" in result
        assert result["raw_heat"] > 0
        assert 0 <= result["normalized_heat"] <= 100

    def test_calculate_platform_heat(self):
        """测试多平台热度计算"""
        platform_data = {
            "微博": {
                "浏览量": 1000000,
                "点赞量": 50000,
                "转发量": 10000,
                "评论量": 5000
            }
        }

        raw_heat = self.calculator._calculate_platform_heat(platform_data)
        assert raw_heat > 0

    def test_normalize_with_reference(self):
        """测试带参考数据的标准化"""
        reference_data = [10000, 50000, 100000, 500000, 1000000]

        normalized1 = self.calculator._normalize(100000, reference_data)
        normalized2 = self.calculator._normalize(500000, reference_data)
        normalized3 = self.calculator._normalize(1000000, reference_data)

        assert normalized1 < normalized2 < normalized3
        assert 0 <= normalized1 <= 100
        assert 0 <= normalized3 <= 100

    def test_normalize_without_reference(self):
        """测试不带参考数据的标准化"""
        normalized = self.calculator._normalize(1000000)
        assert 0 <= normalized <= 100

    def test_decay_formula(self):
        """测试衰减公式"""
        heat = 100
        age_hours = 6
        half_life = 6

        decayed = self.calculator._apply_decay(heat, age_hours, half_life)
        assert decayed < heat
        assert 45 < decayed < 55

        decayed_12h = self.calculator._apply_decay(heat, 12, half_life)
        assert decayed_12h < decayed
        assert 22 < decayed_12h < 28

    def test_different_event_type_half_life(self):
        """测试不同事件类型的半衰期"""
        assert self.calculator.EVENT_TYPE_HALF_LIFE["突发新闻"] == 9
        assert self.calculator.EVENT_TYPE_HALF_LIFE["体育赛事"] == 18
        assert self.calculator.EVENT_TYPE_HALF_LIFE["娱乐热点"] == 36
        assert self.calculator.EVENT_TYPE_HALF_LIFE["节日庆典"] == 60
        assert self.calculator.EVENT_TYPE_HALF_LIFE["常规天气"] == 24

    def test_get_heat_level(self):
        """测试热度级别判定"""
        assert self.calculator._get_heat_level(95) == "A"
        assert self.calculator._get_heat_level(85) == "B"
        assert self.calculator._get_heat_level(75) == "C"
        assert self.calculator._get_heat_level(65) == "D"
        assert self.calculator._get_heat_level(55) == "E"
        assert self.calculator._get_heat_level(40) == "F"

    def test_get_heat_level_desc(self):
        """测试热度级别描述"""
        desc_a = self.calculator._get_heat_level_desc("A")
        assert "极高热" in desc_a
        assert "爆品预警" in desc_a

        desc_f = self.calculator._get_heat_level_desc("F")
        assert "低热" in desc_f

    def test_heat_thresholds(self):
        """测试热度阈值"""
        assert self.calculator.HEAT_THRESHOLDS["A"] == 90
        assert self.calculator.HEAT_THRESHOLDS["B"] == 80
        assert self.calculator.HEAT_THRESHOLDS["C"] == 70

    def test_calculate_with_event_type(self):
        """测试带事件类型的热度计算"""
        event = {
            "view_count": 100000,
            "click_count": 50000,
            "created_at": datetime.now()
        }

        result = self.calculator.calculate_with_event_type(event, "赛事")
        assert "raw_heat" in result
        assert "adjusted_heat" in result
        assert result["type_factor"] == 1.2

    def test_should_trigger_alert(self):
        """测试是否触发预警"""
        assert self.calculator.should_trigger_alert(95) == True
        assert self.calculator.should_trigger_alert(90) == False
        assert self.calculator.should_trigger_alert(80) == False

    def test_get_event_age_hours(self):
        """测试事件年龄计算"""
        event_2h_ago = {"created_at": datetime.now() - timedelta(hours=2)}
        age = self.calculator._get_event_age_hours(event_2h_ago)
        assert 1.9 < age < 2.1

        event_string = {"created_at": (datetime.now() - timedelta(hours=3)).isoformat()}
        age = self.calculator._get_event_age_hours(event_string)
        assert 2.9 < age < 3.1

        event_no_time = {}
        age = self.calculator._get_event_age_hours(event_no_time)
        assert age == 0

    def test_platform_weights(self):
        """测试平台权重"""
        assert self.calculator.PLATFORM_WEIGHTS["微博"] == 0.30
        assert self.calculator.PLATFORM_WEIGHTS["抖音"] == 0.25
        assert self.calculator.PLATFORM_WEIGHTS["新闻媒体"] == 0.25
        assert self.calculator.PLATFORM_WEIGHTS["搜索引擎"] == 0.20

    def test_weights(self):
        """测试基础权重"""
        assert self.calculator.WEIGHTS["view_count"] == 0.4
        assert self.calculator.WEIGHTS["click_count"] == 0.6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
