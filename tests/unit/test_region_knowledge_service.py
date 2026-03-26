"""
地域知识库查询服务测试
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from src.services.region_knowledge_service import RegionKnowledgeService


class TestRegionKnowledgeService:
    """测试地域知识库查询服务"""

    def setup_method(self):
        """初始化测试环境"""
        self.service = RegionKnowledgeService()

    def test_query_exact_match_chengdu_summer_huarun(self):
        """测试精确匹配：成都+夏季+华润万家"""
        results = self.service.query(
            region_name="成都",
            season_or_festival="夏季",
            chain_brand="华润万家"
        )

        assert len(results) > 0
        assert "小龙虾" in results[0].recommended_categories
        assert "冰啤" in results[0].recommended_categories

    def test_query_city_match_chengdu_summer(self):
        """测试城市匹配：成都+夏季（忽略商超品牌）"""
        results = self.service.query(
            region_name="成都",
            season_or_festival="夏季"
        )

        assert len(results) > 0
        assert "小龙虾" in results[0].recommended_categories

    def test_query_national_match_holiday(self):
        """测试全国匹配：国庆节"""
        results = self.service.query(
            region_name="全国",
            season_or_festival="国庆节"
        )

        assert len(results) > 0
        assert "山姆会员店" in [r.chain_brand for r in results]

    def test_query_winter_festival_yuanxiao(self):
        """测试元宵节南北方差异"""
        results_north = self.service.query(
            region_name="北方城市",
            season_or_festival="元宵节"
        )
        results_south = self.service.query(
            region_name="南方城市",
            season_or_festival="元宵节"
        )

        assert len(results_north) > 0
        assert len(results_south) > 0
        assert "元宵" in results_north[0].recommended_categories
        assert "汤圆" in results_south[0].recommended_categories

    def test_query_shanghai_hema_late_night(self):
        """测试上海+盒马鲜生+深夜时段"""
        results = self.service.query(
            region_name="上海",
            season_or_festival="深夜时段",
            chain_brand="盒马鲜生"
        )

        assert len(results) > 0
        assert "泡饭" in results[0].recommended_categories
        assert "小馄饨" in results[0].recommended_categories

    def test_query_chongqing_yonghui_summer(self):
        """测试重庆+永辉超市+夏季"""
        results = self.service.query(
            region_name="重庆",
            season_or_festival="夏季",
            chain_brand="永辉超市"
        )

        assert len(results) > 0
        assert "小龙虾" in results[0].recommended_categories
        assert "火锅食材" in results[0].recommended_categories

    def test_query_no_match_default(self):
        """测试无匹配时的默认推荐"""
        results = self.service.query(
            region_name="拉萨",
            season_or_festival="夏季"
        )

        assert len(results) > 0
        assert "零食" in results[0].recommended_categories

    def test_query_empty_season(self):
        """测试空季节查询"""
        results = self.service.query(
            region_name="长沙",
            season_or_festival=None
        )

        assert len(results) > 0
        assert "口味虾" in results[0].recommended_categories

    def test_get_chain_brand_info(self):
        """测试获取连锁商超品牌信息"""
        info = self.service.get_chain_brand_info("盒马鲜生")

        assert info is not None
        assert info["brand_level"] == "中高端"
        assert "上海" in info["core_cities"]
        assert "进口商品" in info["night_snack_categories"]

        info_walmart = self.service.get_chain_brand_info("山姆会员店")
        assert info_walmart["brand_level"] == "高端"

    def test_recommend_products_for_merchant_chengdu_huarun_summer(self):
        """测试为商家推荐商品"""
        recommendations = self.service.recommend_products_for_merchant(
            merchant_city="成都",
            merchant_chain_brand="华润万家",
            current_season="夏季"
        )

        assert len(recommendations) > 0
        assert "小龙虾" in recommendations
        assert "冰啤" in recommendations

    def test_recommend_products_for_merchant_shanghai_hema_late_night(self):
        """测试上海盒马深夜推荐"""
        recommendations = self.service.recommend_products_for_merchant(
            merchant_city="上海",
            merchant_chain_brand="盒马鲜生",
            current_season="深夜时段"
        )

        assert len(recommendations) > 0
        assert "泡饭" in recommendations

    def test_priority_ordering(self):
        """测试优先级排序"""
        results = self.service.query(
            region_name="成都",
            season_or_festival="夏季"
        )

        priorities = [r.priority for r in results]
        assert priorities == sorted(priorities)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
