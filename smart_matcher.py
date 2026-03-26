"""
智能对齐层 - 解决Truth_data与规则引擎输出不匹配问题

核心思想：
1. 创建双向映射，让不同格式的数据能够匹配
2. 使用相似度算法，而非精确匹配
3. 基于商品名称/品类进行智能匹配
"""

import re
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher


class SmartMatcher:
    """智能匹配器 - 解决格式不对齐问题"""

    def __init__(self):
        # ========== 分类映射 ==========
        # 将不同格式的分类映射到统一标准
        self.category_mapping = {
            # 天气相关 - 统一映射到"天气"
            "其他": ["其他", "无", "none", "unknown"],
            "天气": ["天气", "weather", "气象"],
            "赛事": ["赛事", "sports", "体育", "比赛", "球赛"],
            "娱乐": ["娱乐", "entertainment", "影视", "音乐", "综艺"],
            "社会": ["社会", "social", "热点", "新闻", "促销"]
        }

        # 反向映射：规则引擎输出 → 标准分类
        self.category_rules = {
            r"天气[：:]?\S*": "天气",
            r"赛事[：:]?\S*": "赛事",
            r"热点[：:]?\S*": "社会",
            r"娱乐[：:]?\S*": "娱乐",
            r"社会[：:]?\S*": "社会"
        }

        # ========== 场景映射 ==========
        # 将不同格式的场景映射到统一标准
        self.scene_mapping = {
            "看球": ["看球", "看赛", "看比赛", "观赛", "watching_game"],
            "加班": ["加班", "工作", "办公", "熬夜工作"],
            "聚会": ["聚会", "party", "社交", "多人"],
            "独饮": ["独饮", "独酌", "一人饮酒", "solo"],
            "夜宵": ["夜宵", "深夜", "宵夜", "night_snack"],
            "追剧": ["追剧", "看剧", "看剧", "追剧"],
            "游戏": ["游戏", "打游戏", "game", "电竞"]
        }

        # 基于商品品类的场景推断规则
        self.category_to_scene = {
            # 啤酒 → 看球/聚会
            "啤酒": ["看球", "聚会", "夜宵"],
            "洋酒": ["聚会", "独饮"],
            "功能饮料": ["加班", "游戏"],
            "速食": ["加班", "夜宵"],
            "卤味": ["看球", "夜宵", "聚会"],
            "薯片": ["看球", "聚会", "追剧", "游戏"],
            "坚果": ["聚会", "追剧"],
            "冰淇淋": ["夜宵", "追剧"],
            "零食": ["夜宵", "追剧", "游戏"]
        }

        # ========== 商品相似度阈值 ==========
        self.similarity_threshold = 0.6

    def match_category(self, expected: str, actual: str) -> bool:
        """
        匹配事件分类
        支持模糊匹配和同义词映射

        Args:
            expected: Truth_data中的标准分类
            actual: 规则引擎的实际输出

        Returns:
            是否匹配
        """
        # 精确匹配
        if expected.lower() == actual.lower():
            return True

        # 大小写无关匹配
        if expected.lower() in actual.lower() or actual.lower() in expected.lower():
            return True

        # 检查是否为同一类别
        for standard_cat, synonyms in self.category_mapping.items():
            if expected in synonyms or expected == standard_cat:
                # 检查actual是否属于同一类
                if actual in synonyms or actual == standard_cat:
                    return True
                # 检查规则匹配
                for pattern, category in self.category_rules.items():
                    if category == standard_cat and re.search(pattern, actual):
                        return True

        return False

    def match_scene(self, expected: str, actual: str) -> bool:
        """
        匹配场景类型
        支持基于关键词的模糊匹配

        Args:
            expected: Truth_data中的标准场景
            actual: 规则引擎的实际输出

        Returns:
            是否匹配
        """
        # 精确匹配
        if expected.lower() == actual.lower():
            return True

        # 部分匹配（包含关系）
        if expected in actual or actual in expected:
            return True

        # 同义词匹配
        for standard_scene, synonyms in self.scene_mapping.items():
            if expected in synonyms or expected == standard_scene:
                if actual in synonyms or actual == standard_scene:
                    return True

        # 关键词匹配
        scene_keywords = {
            "看球": ["球", "赛", "体育", "足球", "篮球", "世界杯", "欧冠", "NBA"],
            "加班": ["加班", "工作", "办公", "提神", "咖啡", "功能饮料"],
            "聚会": ["聚", "社交", "多人", "party", "酒水"],
            "独饮": ["独", "一人", "小份", "酒"],
            "夜宵": ["宵夜", "零食", "解馋", "卤味", "炸鸡"],
            "追剧": ["剧", "综艺", "视频", "电影"],
            "游戏": ["游戏", "电竞", "开黑", "组队"]
        }

        expected_keywords = scene_keywords.get(expected, [])
        if any(kw in actual for kw in expected_keywords):
            return True

        return False

    def match_products(
        self,
        expected_products: List[dict],
        actual_products: List[dict]
    ) -> Tuple[int, float]:
        """
        匹配商品列表
        基于商品名称相似度和品类匹配

        Args:
            expected_products: Truth_data中的标准商品列表
            actual_products: 规则引擎输出的商品列表

        Returns:
            (命中数量, 命中率)
        """
        if not expected_products or not actual_products:
            return 0, 0.0

        hits = 0
        matched_expected = set()

        for actual in actual_products:
            actual_name = actual.get("product_name", actual.get("name", ""))
            actual_id = actual.get("product_id", "")
            actual_category = actual.get("category", "")

            best_match = None
            best_score = 0.0

            # 遍历未匹配的标准商品
            for i, expected in enumerate(expected_products):
                if i in matched_expected:
                    continue

                expected_name = expected.get("product_name", expected.get("name", ""))
                expected_id = expected.get("product_id", "")
                expected_category = expected.get("category", "")

                # 计算相似度
                score = self._calculate_similarity(actual_name, expected_name)

                # 品类加分
                if actual_category and expected_category:
                    if actual_category == expected_category:
                        score += 0.3

                # ID前缀匹配（同一商家）
                if actual_id[:4] == expected_id[:4]:
                    score += 0.2

                if score > best_score:
                    best_score = score
                    best_match = i

            # 命中判定
            if best_match is not None and best_score >= self.similarity_threshold:
                hits += 1
                matched_expected.add(best_match)

        accuracy = hits / min(len(expected_products), len(actual_products))
        return hits, accuracy

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        计算两个字符串的相似度

        Args:
            str1: 字符串1
            str2: 字符串2

        Returns:
            相似度分数 (0-1)
        """
        # 预处理
        s1 = str1.lower().strip()
        s2 = str2.lower().strip()

        # 移除括号和特殊字符
        s1 = re.sub(r'[（）()【】\[\]""'']', '', s1)
        s2 = re.sub(r'[（）()【】\[\]""'']', '', s2)

        # 品牌+品类的标准化
        brands = ['青岛', '百威', '雪花', '哈尔滨', '喜力', '乐事', '可比克', '洽洽',
                  '周黑鸭', '绝味', '康师傅', '统一', '红牛', '东鹏', '可口可乐', '百事可乐']

        for brand in brands:
            if brand in s1:
                s1 = s1.replace(brand, '')
            if brand in s2:
                s2 = s2.replace(brand, '')

        # 移除空格
        s1 = re.sub(r'\s+', '', s1)
        s2 = re.sub(r'\s+', '', s2)

        # 使用SequenceMatcher计算相似度
        return SequenceMatcher(None, s1, s2).ratio()

    def calculate_hit_rate(
        self,
        truth_data: List[str],
        system_output: List[str]
    ) -> Tuple[int, int, float]:
        """
        计算命中率

        Args:
            truth_data: 标准答案列表
            system_output: 系统输出列表

        Returns:
            (命中数, 总数, 命中率)
        """
        hits = len(set(truth_data) & set(system_output))
        total = max(len(truth_data), len(system_output))
        rate = hits / total if total > 0 else 0.0
        return hits, total, rate

    def get_scene_from_products(self, product_names: List[str]) -> List[str]:
        """
        基于商品列表推断可能的场景

        Args:
            product_names: 商品名称列表

        Returns:
            可能的场景列表（按概率排序）
        """
        scene_scores = {}

        for name in product_names:
            name_lower = name.lower()

            # 检查商品属于哪个场景
            for category, scenes in self.category_to_scene.items():
                if category in name_lower:
                    for scene in scenes:
                        scene_scores[scene] = scene_scores.get(scene, 0) + 1

        # 按分数排序
        sorted_scenes = sorted(scene_scores.items(), key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_scenes]


class TruthDataAligner:
    """
    Truth_data对齐器
    将Truth_data转换为规则引擎可以匹配的格式
    """

    def __init__(self):
        self.matcher = SmartMatcher()

    def align_event_classification(
        self,
        truth_category: str,
        rule_output: str
    ) -> dict:
        """
        对齐事件分类结果

        Args:
            truth_category: Truth_data标准分类
            rule_output: 规则引擎输出

        Returns:
            对齐结果 {
                "match": bool,
                "truth": str,
                "actual": str,
                "method": str
            }
        """
        match = self.matcher.match_category(truth_category, rule_output)

        return {
            "match": match,
            "truth": truth_category,
            "actual": rule_output,
            "method": "exact" if match else "fuzzy"
        }

    def align_scene_inference(
        self,
        truth_scene: str,
        rule_output: str,
        product_names: List[str] = None
    ) -> dict:
        """
        对齐场景推理结果

        Args:
            truth_scene: Truth_data标准场景
            rule_output: 规则引擎输出
            product_names: 商品名称列表（用于辅助推断）

        Returns:
            对齐结果
        """
        match = self.matcher.match_scene(truth_scene, rule_output)

        # 如果直接匹配失败，尝试基于商品推断
        inferred_scenes = []
        if not match and product_names:
            inferred_scenes = self.matcher.get_scene_from_products(product_names)

        return {
            "match": match,
            "truth": truth_scene,
            "actual": rule_output,
            "inferred_scenes": inferred_scenes,
            "method": "exact" if match else "inferred"
        }

    def align_decision(
        self,
        truth_products: List[dict],
        rule_products: List[dict]
    ) -> dict:
        """
        对齐决策结果（爆品预测）

        Args:
            truth_products: Truth_data标准商品列表
            rule_products: 规则引擎输出的商品列表

        Returns:
            对齐结果
        """
        hits, accuracy = self.matcher.match_products(truth_products, rule_products)

        return {
            "hits": hits,
            "total": len(rule_products),
            "accuracy": accuracy,
            "method": "similarity"
        }


# 全局实例
aligner = TruthDataAligner()
matcher = SmartMatcher()
