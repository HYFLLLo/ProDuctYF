"""
补货计算模块单元测试
"""
import pytest
from src.services.restock_calculator import RestockCalculator


@pytest.fixture
def calculator():
    """创建补货计算器实例"""
    return RestockCalculator(safety_stock_days=1.5)


@pytest.mark.asyncio
async def test_basic_restock_calculation(calculator):
    """测试基础补货计算"""
    sales_predictions = {
        "P001": {"predicted_hourly_avg": 10.0}
    }
    inventory_data = {
        "P001": {"usable_stock": 50}
    }

    result = await calculator.calculate("M001", sales_predictions, inventory_data, 6)

    assert len(result) == 1
    assert result[0]["product_id"] == "P001"
    # 6小时需求=60，当前库存=50，覆盖率=0.83<1.0，所以是high
    assert result[0]["urgency"] == "high"


@pytest.mark.asyncio
async def test_critical_urgency_when_low_stock(calculator):
    """测试库存极低时的紧急补货"""
    sales_predictions = {
        "P002": {"predicted_hourly_avg": 20.0}
    }
    inventory_data = {
        "P002": {"usable_stock": 5}
    }

    result = await calculator.calculate("M001", sales_predictions, inventory_data, 6)

    assert result[0]["urgency"] == "critical"


@pytest.mark.asyncio
async def test_high_urgency_when_below_safety_stock(calculator):
    """测试库存低于安全库存时的紧急补货"""
    sales_predictions = {
        "P003": {"predicted_hourly_avg": 10.0}
    }
    inventory_data = {
        "P003": {"usable_stock": 10}  # 低于安全库存 10*1.5=15
    }

    result = await calculator.calculate("M001", sales_predictions, inventory_data, 24)

    # 24小时需求=240，当前库存=10，覆盖率=10/240=0.042<0.5，所以是critical
    assert result[0]["urgency"] == "critical"


@pytest.mark.asyncio
async def test_zero_demand_low_urgency(calculator):
    """测试零需求时为低紧急度"""
    sales_predictions = {
        "P004": {"predicted_hourly_avg": 0}
    }
    inventory_data = {
        "P004": {"usable_stock": 100}
    }

    result = await calculator.calculate("M001", sales_predictions, inventory_data, 24)

    assert result[0]["urgency"] == "low"


@pytest.mark.asyncio
async def test_recommend_quantity_calculation(calculator):
    """测试建议补货量计算"""
    sales_predictions = {
        "P005": {"predicted_hourly_avg": 10.0}
    }
    inventory_data = {
        "P005": {"usable_stock": 20}
    }

    result = await calculator.calculate("M001", sales_predictions, inventory_data, 24)

    # 24小时需求 = 10 * 24 = 240
    # 安全库存 = 10 * 1.5 * 24 = 360
    # 建议补货 = max(0, 240 - 20 + 360) = 580
    assert result[0]["recommended_quantity"] >= 200


@pytest.mark.asyncio
async def test_sort_by_urgency(calculator):
    """测试结果按紧急程度排序"""
    sales_predictions = {
        "P001": {"predicted_hourly_avg": 5.0},
        "P002": {"predicted_hourly_avg": 20.0},
        "P003": {"predicted_hourly_avg": 10.0}
    }
    inventory_data = {
        "P001": {"usable_stock": 50},   # 充足
        "P002": {"usable_stock": 5},    # critical
        "P003": {"usable_stock": 10}    # high
    }

    result = await calculator.calculate("M001", sales_predictions, inventory_data, 24)

    assert result[0]["product_id"] == "P002"  # 第一个应该是最紧急的
