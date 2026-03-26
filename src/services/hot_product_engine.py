"""
多维度爆品识别引擎 - 整合5个维度的爆品评分算法
核心突破：突破单一用户偏好，整合热点事件、地域特性、顶流推荐
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class HotProductScore:
    """爆品评分结果"""
    product_id: str
    product_name: str
    category: str

    hot_event_score: float = 0.0
    user_preference_score: float = 0.0
    region_specialty_score: float = 0.0
    top_influencer_score: float = 0.0
    trend_growth_score: float = 0.0

    final_score: float = 0.0
    is_hot_product: bool = False
    in_candidate_pool: bool = False

    hot_event_contribution: float = 0.0
    user_preference_contribution: float = 0.0
    region_contribution: float = 0.0
    influencer_contribution: float = 0.0
    trend_contribution: float = 0.0


class HotProductEngine:
    """
    多维度爆品识别引擎

    爆品来源矩阵：
    1. 热点事件爆品 (40%)
    2. 用户偏好爆品 (25%)
    3. 地域特色爆品 (20%)
    4. 顶流热点爆品 (10%)
    5. 趋势增长爆品 (5%)
    """

    WEIGHTS = {
        "hot_event": 0.40,
        "user_preference": 0.25,
        "region_specialty": 0.20,
        "top_influencer": 0.10,
        "trend_growth": 0.05
    }

    THRESHOLDS = {
        "hot_product": 70,
        "candidate_pool": 50
    }

    def __init__(self):
        pass

    def calculate_hot_product_score(
        self,
        product_id: str,
        product_name: str,
        category: str,
        event_heat: Optional[float] = None,
        user_recommendation_priority: Optional[str] = None,
        region_match: bool = False,
        sales_rank: Optional[int] = None,
        event_type: Optional[str] = None,
        sales_growth_rate: Optional[float] = None
    ) -> HotProductScore:
        """
        计算商品的多维度爆品得分

        Args:
            product_id: 商品ID
            product_name: 商品名称
            category: 商品品类
            event_heat: 事件热度
            user_recommendation_priority: 用户推荐优先级 (高/中/低)
            region_match: 是否地域匹配
            sales_rank: 销量排名
            event_type: 事件类型
            sales_growth_rate: 销量增长率

        Returns:
            爆品评分结果
        """
        score = HotProductScore(
            product_id=product_id,
            product_name=product_name,
            category=category
        )

        score.hot_event_score = self._calculate_hot_event_score(event_heat)
        score.user_preference_score = self._calculate_user_preference_score(
            user_recommendation_priority
        )
        score.region_specialty_score = self._calculate_region_specialty_score(
            region_match, sales_rank
        )
        score.top_influencer_score = self._calculate_top_influencer_score(
            event_type, event_heat
        )
        score.trend_growth_score = self._calculate_trend_growth_score(
            sales_growth_rate
        )

        score.hot_event_contribution = score.hot_event_score * self.WEIGHTS["hot_event"]
        score.user_preference_contribution = score.user_preference_score * self.WEIGHTS["user_preference"]
        score.region_contribution = score.region_specialty_score * self.WEIGHTS["region_specialty"]
        score.influencer_contribution = score.top_influencer_score * self.WEIGHTS["top_influencer"]
        score.trend_contribution = score.trend_growth_score * self.WEIGHTS["trend_growth"]

        score.final_score = (
            score.hot_event_contribution +
            score.user_preference_contribution +
            score.region_contribution +
            score.influencer_contribution +
            score.trend_contribution
        ) * 100

        score.is_hot_product = score.final_score >= self.THRESHOLDS["hot_product"]
        score.in_candidate_pool = (
            self.THRESHOLDS["candidate_pool"] <= score.final_score < self.THRESHOLDS["hot_product"]
        )

        return score

    def _calculate_hot_event_score(self, event_heat: Optional[float]) -> float:
        """
        计算热点事件得分

        识别条件：事件热度>80 + 映射命中
        """
        if event_heat is None or event_heat <= 80:
            return 0.0
        return min(event_heat / 100, 1.0)

    def _calculate_user_preference_score(
        self,
        recommendation_priority: Optional[str]
    ) -> float:
        """
        计算用户偏好得分

        识别条件：用户推荐优先级=高
        """
        if recommendation_priority is None:
            return 0.3

        priority_scores = {
            "高": 1.0,
            "中": 0.6,
            "低": 0.3
        }
        return priority_scores.get(recommendation_priority, 0.3)

    def _calculate_region_specialty_score(
        self,
        region_match: bool,
        sales_rank: Optional[int]
    ) -> float:
        """
        计算地域特色得分

        识别条件：城市匹配 + 历史销量Top20
        """
        if not region_match:
            return 0.0

        if sales_rank is not None and sales_rank <= 20:
            return 1.0

        return 0.5

    def _calculate_top_influencer_score(
        self,
        event_type: Optional[str],
        event_heat: Optional[float]
    ) -> float:
        """
        计算顶流热点得分

        识别条件：事件类型=明星热点 + 热度>85
        """
        if event_type != "明星热点":
            return 0.0

        if event_heat is None or event_heat <= 85:
            return 0.0

        return 1.0

    def _calculate_trend_growth_score(
        self,
        sales_growth_rate: Optional[float]
    ) -> float:
        """
        计算趋势增长得分

        识别条件：近7天销量增长>50%
        """
        if sales_growth_rate is None:
            return 0.0

        if sales_growth_rate > 50:
            return 1.0
        elif sales_growth_rate > 30:
            return 0.7
        elif sales_growth_rate > 10:
            return 0.4
        return 0.0

    def batch_calculate_scores(
        self,
        products: List[Dict],
        events: List[Dict],
        user_scenes: List[Dict]
    ) -> List[HotProductScore]:
        """
        批量计算爆品得分

        Args:
            products: 商品列表
            events: 事件列表
            user_scenes: 用户场景列表

        Returns:
            爆品评分结果列表
        """
        scores = []

        for product in products:
            product_id = product.get("product_id")
            product_name = product.get("product_name", "")
            category = product.get("category_name", "")

            event_heat = self._get_product_event_heat(product_id, events)
            recommendation_priority = self._get_user_recommendation_priority(
                product_id, user_scenes
            )
            region_match, sales_rank = self._get_region_and_rank(product)
            event_type = self._get_product_event_type(product_id, events)
            sales_growth_rate = product.get("sales_growth_rate")

            score = self.calculate_hot_product_score(
                product_id=product_id,
                product_name=product_name,
                category=category,
                event_heat=event_heat,
                user_recommendation_priority=recommendation_priority,
                region_match=region_match,
                sales_rank=sales_rank,
                event_type=event_type,
                sales_growth_rate=sales_growth_rate
            )

            scores.append(score)

        scores.sort(key=lambda x: x.final_score, reverse=True)
        return scores

    def _get_product_event_heat(
        self,
        product_id: str,
        events: List[Dict]
    ) -> Optional[float]:
        """获取商品关联的事件热度"""
        for event in events:
            matched_products = event.get("matched_products", [])
            if product_id in matched_products:
                return event.get("heat_score", 0)
        return None

    def _get_user_recommendation_priority(
        self,
        product_id: str,
        user_scenes: List[Dict]
    ) -> Optional[str]:
        """获取用户对商品的推荐优先级"""
        for scene in user_scenes:
            recommended_products = scene.get("recommended_products", [])
            for product in recommended_products:
                if product.get("product_id") == product_id:
                    return product.get("priority", "低")
        return None

    def _get_region_and_rank(
        self,
        product: Dict
    ) -> tuple[bool, Optional[int]]:
        """获取地域匹配和销量排名"""
        region_match = product.get("region_match", False)
        sales_rank = product.get("sales_rank")
        return region_match, sales_rank

    def _get_product_event_type(
        self,
        product_id: str,
        events: List[Dict]
    ) -> Optional[str]:
        """获取商品关联的事件类型"""
        for event in events:
            matched_products = event.get("matched_products", [])
            if product_id in matched_products:
                return event.get("event_type")
        return None

    def filter_hot_products(
        self,
        scores: List[HotProductScore]
    ) -> Dict[str, List[HotProductScore]]:
        """
        过滤爆品和非爆品

        Returns:
            包含hot_products和candidate_pool的字典
        """
        hot_products = [s for s in scores if s.is_hot_product]
        candidate_pool = [s for s in scores if s.in_candidate_pool]

        return {
            "hot_products": hot_products,
            "candidate_pool": candidate_pool
        }

    def generate_restock_recommendations(
        self,
        hot_products: List[HotProductScore],
        current_stock: Dict[str, int],
        predicted_demand: Dict[str, int]
    ) -> List[Dict]:
        """
        生成补货建议

        Args:
            hot_products: 爆品列表
            current_stock: 当前库存
            predicted_demand: 预测需求

        Returns:
            补货建议列表
        """
        recommendations = []

        for product_score in hot_products:
            product_id = product_score.product_id
            stock = current_stock.get(product_id, 0)
            demand = predicted_demand.get(product_id, 0)

            if stock < demand:
                recommend_qty = demand - stock
                urgency = self._determine_restock_urgency(
                    stock, demand, product_score.final_score
                )

                recommendations.append({
                    "product_id": product_id,
                    "product_name": product_score.product_name,
                    "current_stock": stock,
                    "predicted_demand": demand,
                    "recommended_quantity": recommend_qty,
                    "urgency": urgency,
                    "hot_product_score": round(product_score.final_score, 2),
                    "recommendation_reason": self._generate_recommendation_reason(
                        product_score
                    )
                })

        recommendations.sort(key=lambda x: self._urgency_order(x["urgency"]))
        return recommendations

    def _determine_restock_urgency(
        self,
        stock: int,
        demand: int,
        hot_score: float
    ) -> str:
        """确定补货紧急程度"""
        if stock == 0:
            return "P0"
        elif stock < demand * 0.5:
            return "P1"
        elif hot_score >= 80:
            return "P2"
        return "P3"

    def _urgency_order(self, urgency: str) -> tuple:
        """补货优先级排序"""
        order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        return order.get(urgency, 4)

    def _generate_recommendation_reason(self, product_score: HotProductScore) -> str:
        """生成补货原因"""
        reasons = []

        if product_score.hot_event_contribution > 0.15:
            reasons.append(f"热点事件驱动(贡献{product_score.hot_event_contribution*100:.1f}%)")
        if product_score.user_preference_contribution > 0.1:
            reasons.append(f"用户偏好强烈(贡献{product_score.user_preference_contribution*100:.1f}%)")
        if product_score.region_contribution > 0.08:
            reasons.append(f"地域特色商品(贡献{product_score.region_contribution*100:.1f}%)")
        if product_score.influencer_contribution > 0.05:
            reasons.append(f"顶流热点(贡献{product_score.influencer_contribution*100:.1f}%)")
        if product_score.trend_contribution > 0.02:
            reasons.append(f"趋势增长(贡献{product_score.trend_contribution*100:.1f}%)")

        return "; ".join(reasons) if reasons else "综合多维度因素"


_hot_product_engine = None

def get_hot_product_engine() -> HotProductEngine:
    """获取多维度爆品识别引擎实例"""
    global _hot_product_engine
    if _hot_product_engine is None:
        _hot_product_engine = HotProductEngine()
    return _hot_product_engine
