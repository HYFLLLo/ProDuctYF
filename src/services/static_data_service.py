"""
静态数据服务 - 管理静态数据与动态数据的分离
核心优化：避免每日重复计算历史数据，节省TOKEN消耗
"""
import json
from typing import Optional, List, Dict
from datetime import datetime
import pymysql
import os


class StaticDataService:
    """静态数据服务"""

    CACHE_TTL = {
        "user_profile": 3600,
        "event_mapping": 86400,
        "region_knowledge": 21600,
        "chain_brand": 21600
    }

    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.db_config = {
            "host": os.getenv("DB_HOST", "127.0.0.1"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("MYSQL_PASSWORD", ""),
            "database": "night_owl_prediction",
            "charset": "utf8mb4"
        }
        self._cache = {}

    def _get_connection(self):
        """获取数据库连接"""
        try:
            return pymysql.connect(**self.db_config)
        except Exception as e:
            print(f"⚠️  数据库连接失败: {e}")
            return None

    async def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        获取用户画像（静态数据）

        Args:
            user_id: 用户ID

        Returns:
            用户画像字典，包含偏好标签、消费能力等
        """
        cache_key = f"user_profile:{user_id}"

        if self.redis:
            cached = await self.redis.get(cache_key)
            if cached:
                return json.loads(cached)

        conn = self._get_connection()
        if not conn:
            return self._get_default_user_profile(user_id)

        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM user_profiles WHERE user_id = %s",
                (user_id,)
            )
            result = cursor.fetchone()

            if result and self.redis:
                await self.redis.setex(
                    cache_key,
                    self.CACHE_TTL["user_profile"],
                    json.dumps(result, ensure_ascii=False)
                )

            return result
        finally:
            conn.close()

    def _get_default_user_profile(self, user_id: str) -> Dict:
        """获取默认用户画像（数据库不可用时）"""
        return {
            "user_id": user_id,
            "preferences": ["零食", "啤酒"],
            "consumption_level": "medium",
            "preferred_categories": ["零食", "饮料", "啤酒"]
        }

    async def get_event_product_mapping(self, event_type: str) -> List[Dict]:
        """
        获取事件-爆品映射关系（静态数据）

        Args:
            event_type: 事件类型

        Returns:
            映射的商品品类列表
        """
        cache_key = f"event_mapping:{event_type}"

        if self.redis:
            cached = await self.redis.get(cache_key)
            if cached:
                return json.loads(cached)

        conn = self._get_connection()
        if not conn:
            return self._get_default_event_mapping(event_type)

        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM event_product_mapping WHERE event_type = %s",
                (event_type,)
            )
            results = cursor.fetchall()

            if results and self.redis:
                await self.redis.setex(
                    cache_key,
                    self.CACHE_TTL["event_mapping"],
                    json.dumps(results, ensure_ascii=False)
                )

            return results
        finally:
            conn.close()

    def _get_default_event_mapping(self, event_type: str) -> List[Dict]:
        """获取默认事件-爆品映射（数据库不可用时）"""
        default_mappings = {
            "赛事": [
                {"product_categories": ["啤酒", "炸鸡", "零食", "饮料"], "priority": 1}
            ],
            "娱乐": [
                {"product_categories": ["零食", "饮料", "爆米花"], "priority": 1}
            ],
            "天气": [
                {"product_categories": ["冰淇淋", "冷饮", "西瓜"], "priority": 1}
            ],
            "节日": [
                {"product_categories": ["月饼", "粽子", "汤圆"], "priority": 1}
            ],
            "明星热点": [
                {"product_categories": ["代言品牌商品"], "priority": 1}
            ]
        }
        return default_mappings.get(event_type, [])

    async def get_region_knowledge(
        self,
        region_name: str,
        season_or_festival: Optional[str] = None,
        chain_brand: Optional[str] = None
    ) -> List[Dict]:
        """
        获取地域知识库（静态数据）

        Args:
            region_name: 地区名称（城市/省份）
            season_or_festival: 季节或节日
            chain_brand: 连锁商超品牌

        Returns:
            推荐商品品类列表
        """
        cache_key = f"region_knowledge:{region_name}:{season_or_festival}:{chain_brand}"

        if self.redis:
            cached = await self.redis.get(cache_key)
            if cached:
                return json.loads(cached)

        conn = self._get_connection()
        if not conn:
            return self._get_default_region_knowledge(region_name, season_or_festival, chain_brand)

        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            query = "SELECT * FROM region_knowledge WHERE region_name = %s"
            params = [region_name]

            if season_or_festival:
                query += " AND (season_or_festival = %s OR season_or_festival IS NULL)"
                params.append(season_or_festival)

            if chain_brand:
                query += " AND (chain_brand = %s OR chain_brand IS NULL)"
                params.append(chain_brand)

            query += " ORDER BY priority DESC"

            cursor.execute(query, tuple(params))
            results = cursor.fetchall()

            if results and self.redis:
                await self.redis.setex(
                    cache_key,
                    self.CACHE_TTL["region_knowledge"],
                    json.dumps(results, ensure_ascii=False)
                )

            return results
        finally:
            conn.close()

    def _get_default_region_knowledge(
        self,
        region_name: str,
        season_or_festival: Optional[str] = None,
        chain_brand: Optional[str] = None
    ) -> List[Dict]:
        """获取默认地域知识（数据库不可用时）"""
        knowledge_db = {
            "成都": {
                "夏季": {
                    "华润万家": ["小龙虾", "冰啤", "串串", "冷淡杯", "卤味", "凉菜"],
                    None: ["小龙虾", "冰啤", "串串", "冷淡杯"]
                },
                None: {
                    None: ["火锅", "串串", "冷淡杯"]
                }
            },
            "重庆": {
                "夏季": {
                    None: ["小龙虾", "冰啤", "火锅", "江湖菜"]
                },
                None: {
                    None: ["火锅", "江湖菜", "小面"]
                }
            },
            "上海": {
                None: {
                    "盒马鲜生": ["泡饭", "小馄饨", "葱油拌面", "进口零食", "啤酒"],
                    None: ["泡饭", "小馄饨", "本帮菜"]
                }
            },
            "全国": {
                "国庆节": {
                    "山姆会员店": ["进口坚果礼盒", "红酒", "进口零食大礼包", "烘焙甜点", "车厘子"],
                    None: ["零食大礼包", "啤酒", "烧烤食材"]
                },
                "春节": {
                    "山姆会员店": ["进口坚果礼盒", "红酒", "车厘子", "进口零食"],
                    None: ["坚果", "糖果", "酒水", "礼盒"]
                },
                "高温预警": {
                    None: ["冰淇淋", "冷饮", "西瓜", "冰啤"]
                }
            }
        }

        region_data = knowledge_db.get(region_name, {})
        season_data = season_data = season_data = season_data = season_data = season_data = region_data.get(
            season_or_festival,
            region_data.get(None, {})
        )

        if chain_brand and chain_brand in season_data:
            return [{"recommended_categories": season_data[chain_brand]}]
        elif None in season_data:
            return [{"recommended_categories": season_data[None]}]

        return [{"recommended_categories": ["零食", "饮料", "啤酒"]}]

    async def get_chain_brand_knowledge(self, brand_name: str) -> Optional[Dict]:
        """
        获取连锁商超品牌知识（静态数据）

        Args:
            brand_name: 品牌名称

        Returns:
            品牌知识字典
        """
        cache_key = f"chain_brand:{brand_name}"

        if self.redis:
            cached = await self.redis.get(cache_key)
            if cached:
                return json.loads(cached)

        conn = self._get_connection()
        if not conn:
            return self._get_default_chain_brand(brand_name)

        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM chain_brand_knowledge WHERE brand_name = %s",
                (brand_name,)
            )
            result = cursor.fetchone()

            if result and self.redis:
                await self.redis.setex(
                    cache_key,
                    self.CACHE_TTL["chain_brand"],
                    json.dumps(result, ensure_ascii=False)
                )

            return result
        finally:
            conn.close()

    def _get_default_chain_brand(self, brand_name: str) -> Dict:
        """获取默认连锁商超品牌知识（数据库不可用时）"""
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
            "红旗连锁": {
                "brand_level": "社区便利",
                "core_cities": ["成都"],
                "night_snack_categories": ["串串", "卤味", "冷淡杯"]
            }
        }
        return brand_db.get(brand_name, {})

    async def invalidate_cache(self, cache_type: str):
        """
        清除指定类型的缓存

        Args:
            cache_type: 缓存类型 (user_profile/event_mapping/region_knowledge/chain_brand)
        """
        if not self.redis:
            return

        pattern = f"{cache_type}:*"
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)


_static_data_service = None

def get_static_data_service(redis_client=None) -> StaticDataService:
    """获取静态数据服务实例"""
    global _static_data_service
    if _static_data_service is None:
        _static_data_service = StaticDataService(redis_client)
    return _static_data_service
