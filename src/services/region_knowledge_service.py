"""
地域知识库查询服务 - 连锁商超地域知识库查询
地域维度：商超品牌 + 城市 + 定位的多维度组合
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegionKnowledge:
    """地域知识结构"""
    region_type: str
    region_name: str
    chain_brand: Optional[str]
    brand_level: Optional[str]
    season_or_festival: Optional[str]
    recommended_categories: List[str]
    priority: int
    reference_factors: str


class RegionKnowledgeService:
    """
    地域知识库查询服务

    支持三维匹配查询：
    1. 精确匹配：商超+城市+季节
    2. 模糊匹配：城市+季节（忽略商超品牌）
    3. 默认匹配：全国+季节
    """

    def __init__(self):
        self._knowledge_base = self._init_knowledge_base()

    def _init_knowledge_base(self) -> List[Dict]:
        """初始化地域知识库"""
        return [
            {
                "region_type": "城市",
                "region_name": "成都",
                "chain_brand": "华润万家",
                "brand_level": "平价",
                "season_or_festival": "夏季",
                "recommended_categories": ["小龙虾", "冰啤", "串串", "冷淡杯", "卤味", "凉菜"],
                "priority": 1,
                "reference_factors": "成都夏季高温+夜生活丰富+华润门店覆盖面广"
            },
            {
                "region_type": "城市",
                "region_name": "成都",
                "chain_brand": None,
                "brand_level": None,
                "season_or_festival": "夏季",
                "recommended_categories": ["小龙虾", "冰啤", "串串", "冷淡杯"],
                "priority": 2,
                "reference_factors": "成都夏季高温+夜生活丰富"
            },
            {
                "region_type": "城市",
                "region_name": "重庆",
                "chain_brand": "永辉超市",
                "brand_level": "平价",
                "season_or_festival": "夏季",
                "recommended_categories": ["小龙虾", "火锅食材", "冰啤", "江湖菜"],
                "priority": 1,
                "reference_factors": "重庆夏季高温+火锅文化+永辉区域优势"
            },
            {
                "region_type": "城市",
                "region_name": "上海",
                "chain_brand": "盒马鲜生",
                "brand_level": "中高端",
                "season_or_festival": "深夜时段",
                "recommended_categories": ["泡饭", "小馄饨", "葱油拌面", "进口零食", "啤酒"],
                "priority": 1,
                "reference_factors": "上海夜宵文化精致化+盒马即时配送能力"
            },
            {
                "region_type": "全国",
                "region_name": "全国",
                "chain_brand": "山姆会员店",
                "brand_level": "高端",
                "season_or_festival": "国庆节",
                "recommended_categories": ["进口坚果礼盒", "红酒", "进口零食大礼包", "烘焙甜点", "车厘子"],
                "priority": 1,
                "reference_factors": "高端客群+节日送礼需求+家庭聚会场景"
            },
            {
                "region_type": "全国",
                "region_name": "全国",
                "chain_brand": "山姆会员店",
                "brand_level": "高端",
                "season_or_festival": "春节",
                "recommended_categories": ["进口坚果礼盒", "红酒", "车厘子", "进口零食"],
                "priority": 1,
                "reference_factors": "高端客群+节日送礼需求+家庭聚会场景"
            },
            {
                "region_type": "全国",
                "region_name": "全国",
                "chain_brand": None,
                "brand_level": None,
                "season_or_festival": "元宵节",
                "recommended_categories": ["元宵", "汤圆"],
                "priority": 1,
                "reference_factors": "南北方元宵节差异"
            },
            {
                "region_type": "全国",
                "region_name": "全国",
                "chain_brand": None,
                "brand_level": None,
                "season_or_festival": "高温预警",
                "recommended_categories": ["冰淇淋", "冷饮", "西瓜", "冰啤"],
                "priority": 1,
                "reference_factors": "防暑降温需求"
            },
            {
                "region_type": "城市",
                "region_name": "长沙",
                "chain_brand": None,
                "brand_level": None,
                "season_or_festival": None,
                "recommended_categories": ["口味虾", "臭豆腐", "槟榔", "茶颜悦色"],
                "priority": 1,
                "reference_factors": "长沙夜宵文化浓厚"
            },
            {
                "region_type": "城市",
                "region_name": "武汉",
                "chain_brand": None,
                "brand_level": None,
                "season_or_festival": "夏季",
                "recommended_categories": ["小龙虾", "热干面", "鸭脖"],
                "priority": 1,
                "reference_factors": "武汉火炉城市+夜宵文化"
            },
            {
                "region_type": "城市",
                "region_name": "广州",
                "chain_brand": "美宜佳",
                "brand_level": "社区便利",
                "season_or_festival": None,
                "recommended_categories": ["广式点心", "糖水", "烧味"],
                "priority": 1,
                "reference_factors": "粤式夜宵文化"
            },
            {
                "region_type": "城市",
                "region_name": "成都",
                "chain_brand": "红旗连锁",
                "brand_level": "社区便利",
                "season_or_festival": None,
                "recommended_categories": ["串串", "卤味", "冷淡杯"],
                "priority": 1,
                "reference_factors": "四川社区便利+川味夜宵"
            },
            {
                "region_type": "城市",
                "region_name": "北方城市",
                "chain_brand": None,
                "brand_level": None,
                "season_or_festival": "元宵节",
                "recommended_categories": ["元宵"],
                "priority": 1,
                "reference_factors": "北方元宵节传统"
            },
            {
                "region_type": "城市",
                "region_name": "南方城市",
                "chain_brand": None,
                "brand_level": None,
                "season_or_festival": "元宵节",
                "recommended_categories": ["汤圆"],
                "priority": 1,
                "reference_factors": "南方汤圆传统"
            }
        ]

    def query(
        self,
        region_name: str,
        season_or_festival: Optional[str] = None,
        chain_brand: Optional[str] = None,
        brand_level: Optional[str] = None
    ) -> List[RegionKnowledge]:
        """
        查询地域知识库

        Args:
            region_name: 地区名称（城市/省份/全国）
            season_or_festival: 季节或节日
            chain_brand: 连锁商超品牌
            brand_level: 品牌定位

        Returns:
            推荐商品品类列表（按优先级排序）
        """
        results = []

        exact_match = self._query_exact_match(
            region_name, season_or_festival, chain_brand, brand_level
        )
        results.extend(exact_match)

        if not exact_match:
            city_match = self._query_city_match(
                region_name, season_or_festival
            )
            results.extend(city_match)

        if not results:
            national_match = self._query_national_match(season_or_festival)
            results.extend(national_match)

        if not results:
            results = self._get_default_recommendations(region_name)

        results.sort(key=lambda x: x.priority)
        return results

    def _query_exact_match(
        self,
        region_name: str,
        season_or_festival: Optional[str],
        chain_brand: Optional[str],
        brand_level: Optional[str]
    ) -> List[RegionKnowledge]:
        """精确匹配查询"""
        results = []

        for item in self._knowledge_base:
            if self._is_exact_match(item, region_name, season_or_festival, chain_brand):
                results.append(RegionKnowledge(**item))

        return results

    def _is_exact_match(
        self,
        item: Dict,
        region_name: str,
        season_or_festival: Optional[str],
        chain_brand: Optional[str]
    ) -> bool:
        """判断是否精确匹配"""
        if item["region_name"] != region_name:
            return False

        if season_or_festival and item["season_or_festival"] != season_or_festival:
            return False

        if chain_brand and item["chain_brand"] != chain_brand:
            return False

        return True

    def _query_city_match(
        self,
        region_name: str,
        season_or_festival: Optional[str]
    ) -> List[RegionKnowledge]:
        """城市匹配查询（忽略商超品牌）"""
        results = []

        for item in self._knowledge_base:
            if item["region_name"] == region_name and item["chain_brand"] is None:
                if season_or_festival is None or item["season_or_festival"] == season_or_festival:
                    results.append(RegionKnowledge(**item))

        return results

    def _query_national_match(
        self,
        season_or_festival: Optional[str]
    ) -> List[RegionKnowledge]:
        """全国匹配查询"""
        results = []

        for item in self._knowledge_base:
            if item["region_name"] == "全国":
                if season_or_festival is None or item["season_or_festival"] == season_or_festival:
                    results.append(RegionKnowledge(**item))

        return results

    def _get_default_recommendations(self, region_name: str) -> List[RegionKnowledge]:
        """获取默认推荐"""
        return [
            RegionKnowledge(
                region_type="城市",
                region_name=region_name,
                chain_brand=None,
                brand_level=None,
                season_or_festival=None,
                recommended_categories=["零食", "饮料", "啤酒"],
                priority=99,
                reference_factors="默认推荐"
            )
        ]

    def get_chain_brand_info(self, brand_name: str) -> Optional[Dict]:
        """
        获取连锁商超品牌信息

        Args:
            brand_name: 品牌名称

        Returns:
            品牌信息字典
        """
        brand_db = {
            "华润万家": {
                "brand_level": "平价",
                "core_cities": ["深圳", "广州", "上海", "北京"],
                "night_snack_categories": ["应季水果", "啤酒", "零食", "速冻食品"]
            },
            "永辉超市": {
                "brand_level": "平价",
                "core_cities": ["福州", "重庆", "成都"],
                "night_snack_categories": ["火锅食材", "小龙虾", "卤味"]
            },
            "大润发": {
                "brand_level": "平价",
                "core_cities": ["全国覆盖"],
                "night_snack_categories": ["传统零食", "啤酒", "应季商品"]
            },
            "盒马鲜生": {
                "brand_level": "中高端",
                "core_cities": ["上海", "北京", "深圳", "杭州"],
                "night_snack_categories": ["进口商品", "海鲜", "精致小食"]
            },
            "山姆会员店": {
                "brand_level": "高端",
                "core_cities": ["上海", "北京", "深圳", "广州"],
                "night_snack_categories": ["进口零食", "红酒", "坚果", "烘焙"]
            },
            "家家悦": {
                "brand_level": "平价",
                "core_cities": ["山东", "东北"],
                "night_snack_categories": ["海鲜", "卤味", "啤酒"]
            },
            "红旗连锁": {
                "brand_level": "社区便利",
                "core_cities": ["成都"],
                "night_snack_categories": ["串串", "卤味", "冷淡杯"]
            },
            "美宜佳": {
                "brand_level": "社区便利",
                "core_cities": ["广东"],
                "night_snack_categories": ["广式点心", "糖水", "烧味"]
            }
        }
        return brand_db.get(brand_name)

    def recommend_products_for_merchant(
        self,
        merchant_city: str,
        merchant_chain_brand: Optional[str],
        current_season: str,
        current_festival: Optional[str] = None
    ) -> List[str]:
        """
        为商家推荐商品品类

        Args:
            merchant_city: 商家所在城市
            merchant_chain_brand: 商家所属连锁品牌
            current_season: 当前季节
            current_festival: 当前节日

        Returns:
            推荐商品品类列表
        """
        season_or_festival = current_festival or current_season

        knowledge_list = self.query(
            region_name=merchant_city,
            season_or_festival=season_or_festival,
            chain_brand=merchant_chain_brand
        )

        all_categories = []
        for knowledge in knowledge_list:
            all_categories.extend(knowledge.recommended_categories)

        return list(set(all_categories))


_region_knowledge_service = None

def get_region_knowledge_service() -> RegionKnowledgeService:
    """获取地域知识库服务实例"""
    global _region_knowledge_service
    if _region_knowledge_service is None:
        _region_knowledge_service = RegionKnowledgeService()
    return _region_knowledge_service
