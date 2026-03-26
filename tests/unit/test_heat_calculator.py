"""
热度计算模块单元测试
"""
import pytest
from datetime import datetime, timedelta
from src.services.heat_calculator import HeatCalculator


@pytest.fixture
def calculator():
    """创建热度计算器实例"""
    return HeatCalculator()


def test_basic_heat_calculation(calculator):
    """测试基础热度计算"""
    event = {
        "view_count": 1000,
        "click_count": 500
    }

    heat = calculator.calculate(event)

    assert heat > 0
    assert heat <= 100


def test_higher_counts_higher_heat(calculator):
    """测试更高的浏览/点击产生更高热度"""
    event_low = {"view_count": 100, "click_count": 50}
    event_high = {"view_count": 10000, "click_count": 5000}

    heat_low = calculator.calculate(event_low)
    heat_high = calculator.calculate(event_high)

    assert heat_high > heat_low


def test_normalization_to_100(calculator):
    """测试热度归一化到0-100"""
    event = {
        "view_count": 1000000,
        "click_count": 1000000
    }

    heat = calculator.calculate(event)

    assert heat <= 100


def test_decay_over_time(calculator):
    """测试时间衰减"""
    old_event = {
        "view_count": 10000,
        "click_count": 5000,
        "created_at": datetime.now() - timedelta(hours=12)
    }

    new_event = {
        "view_count": 10000,
        "click_count": 5000,
        "created_at": datetime.now()
    }

    heat_old = calculator.calculate(old_event)
    heat_new = calculator.calculate(new_event)

    assert heat_old < heat_new


def test_click_weight_higher_than_view(calculator):
    """测试点击权重高于浏览"""
    event_views = {"view_count": 1000, "click_count": 0}
    event_clicks = {"view_count": 0, "click_count": 1000}

    heat_views = calculator.calculate(event_views)
    heat_clicks = calculator.calculate(event_clicks)

    # 点击的权重是0.6，浏览是0.4，所以相同数量下点击产生更高热度
    assert heat_clicks > heat_views


def test_zero_counts(calculator):
    """测试零浏览/点击"""
    event = {"view_count": 0, "click_count": 0}

    heat = calculator.calculate(event)

    assert heat == 0


def test_with_event_type_factor(calculator):
    """测试带事件类型因子的热度计算"""
    event = {
        "view_count": 10000,
        "click_count": 5000,
        "created_at": datetime.now()
    }

    result = calculator.calculate_with_event_type(event, "赛事")

    assert "adjusted_heat" in result
    assert "type_factor" in result
    assert result["type_factor"] == 1.2  # 赛事类型因子
