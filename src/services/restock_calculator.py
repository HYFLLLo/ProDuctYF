"""
补货计算服务 - 基于预测的补货建议
"""
from typing import Optional, List


class RestockCalculator:
    """补货计算器"""

    def __init__(self, safety_stock_days: float = 1.5):
        """
        初始化补货计算器

        Args:
            safety_stock_days: 安全库存天数，默认1.5天
        """
        self.safety_stock_days = safety_stock_days

    async def calculate(
        self,
        merchant_id: str,
        sales_predictions: dict[str, dict],
        inventory_data: dict[str, dict],
        replenishment_period_hours: int = 24
    ) -> List[dict]:
        """
        计算补货建议

        Args:
            merchant_id: 商家ID
            sales_predictions: 销量预测结果 {product_id: {predicted_hourly_avg, ...}}
            inventory_data: 库存数据 {product_id: {usable_stock, ...}}
            replenishment_period_hours: 补货周期（小时）

        Returns:
            补货建议列表
        """
        recommendations = []

        for product_id, prediction in sales_predictions.items():
            inv = inventory_data.get(product_id, {})
            current_stock = inv.get("usable_stock", 0)

            # 计算预测需求
            predicted_hourly_avg = prediction.get("predicted_hourly_avg", 0)
            predicted_demand = predicted_hourly_avg * replenishment_period_hours

            # 计算安全库存
            safety_stock = self._calculate_safety_stock(predicted_hourly_avg)

            # 计算建议补货量
            recommended_qty = max(
                0,
                predicted_demand - current_stock + safety_stock
            )

            # 确定紧急程度
            urgency = self._determine_urgency(
                current_stock, safety_stock, predicted_demand
            )

            recommendations.append({
                "product_id": product_id,
                "current_stock": current_stock,
                "safety_stock": round(safety_stock, 2),
                "predicted_demand": round(predicted_demand, 2),
                "recommended_quantity": max(1, int(recommended_qty)),
                "urgency": urgency
            })

        # 按紧急程度排序
        urgency_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(
            key=lambda x: (
                urgency_order.get(x["urgency"], 3),
                -x["recommended_quantity"]
            )
        )

        return recommendations

    def _calculate_safety_stock(self, predicted_hourly_avg: float) -> float:
        """
        计算安全库存

        安全库存 = 平均小时销量 × 安全库存天数
        """
        return predicted_hourly_avg * self.safety_stock_days

    def _determine_urgency(
        self,
        current_stock: float,
        safety_stock: float,
        predicted_demand: float
    ) -> str:
        """
        确定补货紧急程度

        Returns:
            critical/high/medium/low
        """
        if predicted_demand <= 0:
            return "low"

        coverage_ratio = current_stock / predicted_demand

        # critical: 库存低于安全库存的50% 或 覆盖率低于50%
        if current_stock < safety_stock * 0.5 or coverage_ratio < 0.5:
            return "critical"
        # high: 库存低于安全库存 或 覆盖率低于100%
        elif current_stock < safety_stock or coverage_ratio < 1.0:
            return "high"
        # medium: 覆盖率低于150%
        elif coverage_ratio < 1.5:
            return "medium"
        # low: 库存充足
        return "low"

    def calculate_with_lead_time(
        self,
        predicted_hourly_avg: float,
        current_stock: float,
        lead_time_hours: int,
        safety_stock_days: float = 1.5
    ) -> dict:
        """
        考虑补货周期的精确计算

        Args:
            predicted_hourly_avg: 预测平均小时销量
            current_stock: 当前库存
            lead_time_hours: 补货周期（小时）
            safety_stock_days: 安全库存天数

        Returns:
            包含详细计算结果的字典
        """
        # 补货周期内的需求
        lead_time_demand = predicted_hourly_avg * lead_time_hours

        # 安全库存
        safety_stock = predicted_hourly_avg * 24 * safety_stock_days

        # 补货后库存 = 当前库存 - 补货周期需求 + 补货量
        # 目标：补货后库存 >= 安全库存
        min_restock = max(0, lead_time_demand + safety_stock - current_stock)

        # 紧急补货量（考虑覆盖额外安全库存）
        urgent_restock = max(
            0,
            lead_time_demand + safety_stock * 1.5 - current_stock
        )

        urgency = self._determine_urgency(
            current_stock,
            safety_stock,
            predicted_hourly_avg * 24
        )

        return {
            "lead_time_demand": round(lead_time_demand, 2),
            "safety_stock": round(safety_stock, 2),
            "min_recommended_quantity": max(1, int(min_restock)),
            "urgent_recommended_quantity": max(1, int(urgent_restock)),
            "urgency": urgency,
            "coverage_hours": (
                round(current_stock / predicted_hourly_avg, 1)
                if predicted_hourly_avg > 0 else 999
            )
        }
