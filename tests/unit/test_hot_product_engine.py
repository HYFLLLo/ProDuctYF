"""
多维度爆品识别引擎测试
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from src.services.hot_product_engine import HotProductEngine, HotProductScore


class TestHotProductEngine:
    """测试多维度爆品识别引擎"""

    def setup_method(self):
        """初始化测试环境"""
        self.engine = HotProductEngine()

    def test_calculate_hot_event_score(self):
        """测试热点事件得分计算"""
        score = self.engine._calculate_hot_event_score(95)
        assert score == 0.95

        score = self.engine._calculate_hot_event_score(80)
        assert score == 0.0

        score = self.engine._calculate_hot_event_score(100)
        assert score == 1.0

        score = self.engine._calculate_hot_event_score(None)
        assert score == 0.0

    def test_calculate_user_preference_score(self):
        """测试用户偏好得分计算"""
        assert self.engine._calculate_user_preference_score("高") == 1.0
        assert self.engine._calculate_user_preference_score("中") == 0.6
        assert self.engine._calculate_user_preference_score("低") == 0.3
        assert self.engine._calculate_user_preference_score(None) == 0.3

    def test_calculate_region_specialty_score(self):
        """测试地域特色得分计算"""
        assert self.engine._calculate_region_specialty_score(True, 10) == 1.0
        assert self.engine._calculate_region_specialty_score(True, 25) == 0.5
        assert self.engine._calculate_region_specialty_score(False, 5) == 0.0

    def test_calculate_top_influencer_score(self):
        """测试顶流热点得分计算"""
        assert self.engine._calculate_top_influencer_score("明星热点", 90) == 1.0
        assert self.engine._calculate_top_influencer_score("明星热点", 80) == 0.0
        assert self.engine._calculate_top_influencer_score("赛事", 90) == 0.0
        assert self.engine._calculate_top_influencer_score(None, 90) == 0.0

    def test_calculate_trend_growth_score(self):
        """测试趋势增长得分计算"""
        assert self.engine._calculate_trend_growth_score(60) == 1.0
        assert self.engine._calculate_trend_growth_score(40) == 0.7
        assert self.engine._calculate_trend_growth_score(20) == 0.4
        assert self.engine._calculate_trend_growth_score(5) == 0.0
        assert self.engine._calculate_trend_growth_score(None) == 0.0

    def test_calculate_hot_product_score_full(self):
        """测试完整爆品得分计算"""
        score = self.engine.calculate_hot_product_score(
            product_id="beer_001",
            product_name="啤酒",
            category="酒水",
            event_heat=95,
            user_recommendation_priority="高",
            region_match=True,
            sales_rank=5,
            event_type="赛事",
            sales_growth_rate=80
        )

        assert isinstance(score, HotProductScore)
        assert score.hot_event_score == 0.95
        assert score.user_preference_score == 1.0
        assert score.region_specialty_score == 1.0
        assert score.top_influencer_score == 0.0
        assert score.trend_growth_score == 1.0

        expected_final = (0.95 * 0.40 + 1.0 * 0.25 + 1.0 * 0.20 + 0 * 0.10 + 1.0 * 0.05) * 100
        assert abs(score.final_score - expected_final) < 0.1

        assert score.is_hot_product == True
        assert score.in_candidate_pool == False

    def test_calculate_hot_product_score_candidate_pool(self):
        """测试候选池商品得分"""
        score = self.engine.calculate_hot_product_score(
            product_id="candy_001",
            product_name="糖果",
            category="零食",
            event_heat=90,
            user_recommendation_priority="高",
            region_match=False,
            sales_rank=None,
            event_type="其他",
            sales_growth_rate=None
        )

        assert 50 <= score.final_score < 70
        assert score.in_candidate_pool == True
        assert score.is_hot_product == False

    def test_calculate_hot_product_score_not_hot(self):
        """测试非爆品商品得分"""
        score = self.engine.calculate_hot_product_score(
            product_id="water_001",
            product_name="矿泉水",
            category="饮料",
            event_heat=50,
            user_recommendation_priority="低",
            region_match=False,
            sales_rank=None,
            event_type="其他",
            sales_growth_rate=None
        )

        assert score.final_score < 50
        assert score.is_hot_product == False
        assert score.in_candidate_pool == False

    def test_batch_calculate_scores(self):
        """测试批量计算得分"""
        products = [
            {
                "product_id": "beer_001",
                "product_name": "啤酒",
                "category_name": "酒水",
                "region_match": True,
                "sales_rank": 5,
                "sales_growth_rate": 80
            },
            {
                "product_id": "snack_001",
                "product_name": "薯片",
                "category_name": "零食",
                "region_match": False,
                "sales_rank": 15,
                "sales_growth_rate": 30
            }
        ]

        events = [
            {
                "event_id": "worldcup",
                "heat_score": 95,
                "event_type": "赛事",
                "matched_products": ["beer_001", "snack_001"]
            }
        ]

        user_scenes = [
            {
                "scene_id": "scene_001",
                "recommended_products": [
                    {"product_id": "beer_001", "priority": "高"},
                    {"product_id": "snack_001", "priority": "中"}
                ]
            }
        ]

        scores = self.engine.batch_calculate_scores(products, events, user_scenes)

        assert len(scores) == 2
        assert scores[0].product_id == "beer_001"
        assert scores[0].final_score > scores[1].final_score

    def test_filter_hot_products(self):
        """测试爆品过滤"""
        scores = [
            self.engine.calculate_hot_product_score(
                "p1", "商品1", "类别1",
                event_heat=95,
                user_recommendation_priority="高",
                region_match=True,
                sales_rank=5,
                sales_growth_rate=80
            ),
            self.engine.calculate_hot_product_score(
                "p2", "商品2", "类别2",
                event_heat=82,
                user_recommendation_priority="高",
                region_match=False,
                sales_rank=None,
                sales_growth_rate=None
            ),
            self.engine.calculate_hot_product_score(
                "p3", "商品3", "类别3",
                event_heat=40,
                user_recommendation_priority="低",
                region_match=False,
                sales_rank=None,
                sales_growth_rate=None
            )
        ]

        filtered = self.engine.filter_hot_products(scores)

        assert len(filtered["hot_products"]) == 1
        assert len(filtered["candidate_pool"]) == 1
        assert filtered["hot_products"][0].product_id == "p1"
        assert filtered["candidate_pool"][0].product_id == "p2"

    def test_determine_restock_urgency(self):
        """测试补货紧急程度判定"""
        assert self.engine._determine_restock_urgency(0, 100, 85) == "P0"
        assert self.engine._determine_restock_urgency(20, 100, 75) == "P1"
        assert self.engine._determine_restock_urgency(60, 100, 85) == "P2"
        assert self.engine._determine_restock_urgency(80, 50, 60) == "P3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
