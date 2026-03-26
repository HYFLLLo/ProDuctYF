"""
事件去重服务 - 基于TF-IDF的语义去重
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional, List


class EventDedup:
    """事件去重引擎"""

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        self.vectorizer = TfidfVectorizer()
        self.event_index: List[dict] = []
        self.vector_index: Optional[np.ndarray] = None
        self._is_initialized = False

    async def process(self, events: list[dict]) -> list[dict]:
        """
        处理事件列表，返回去重后的事件

        Args:
            events: 事件列表

        Returns:
            去重后的事件列表
        """
        if not events:
            return []

        # 批量初始化vectorizer
        await self._batch_init(events)

        unique_events = []
        for event in events:
            if not await self._is_duplicate(event):
                unique_events.append(event)
                self.event_index.append(event)

        return unique_events

    async def _batch_init(self, events: list[dict]):
        """批量初始化向量索引"""
        if self._is_initialized:
            return

        texts = [self._get_event_text(e) for e in events]
        if not texts:
            return

        # 一次性构建整个向量空间
        self.vectorizer = TfidfVectorizer()
        self.vector_index = self.vectorizer.fit_transform(texts).toarray()
        self.event_index = []
        self._is_initialized = True

    async def _is_duplicate(self, event: dict) -> bool:
        """判断事件是否与索引中的事件重复"""
        if not self.event_index or not self._is_initialized:
            return False

        event_text = self._get_event_text(event)
        event_vector = self.vectorizer.transform([event_text]).toarray()

        similarities = cosine_similarity(event_vector, self.vector_index)[0]
        max_similarity = float(np.max(similarities))

        return max_similarity >= self.similarity_threshold

    async def _add_to_index(self, event: dict):
        """将事件添加到索引（单个添加）"""
        event_text = self._get_event_text(event)

        # 使用transform而非fit_transform，保持向量空间一致
        new_vector = self.vectorizer.transform([event_text]).toarray()

        if self.vector_index is None:
            self.vector_index = new_vector
        else:
            self.vector_index = np.vstack([self.vector_index, new_vector])

        self.event_index.append(event)

    def _get_event_text(self, event: dict) -> str:
        """提取事件的文本表示"""
        # 支持多种数据格式
        if "raw_data" in event:
            raw = event["raw_data"]
            return f"{raw.get('event_name', '')} {raw.get('raw_content', '')}"
        return f"{event.get('name', '')} {event.get('summary', '')}"

    async def merge_events(self, events: list[dict]) -> list[dict]:
        """
        合并相似事件，保留信息最完整的
        """
        if not events:
            return []

        # 批量初始化
        await self._batch_init(events)

        merged = []
        for event in events:
            duplicate_idx = await self._find_duplicate(event, merged)
            if duplicate_idx >= 0:
                # 合并到已有事件，保留信息更丰富的
                merged[duplicate_idx] = self._merge_two_events(merged[duplicate_idx], event)
            else:
                merged.append(event)

        return merged

    async def _find_duplicate(self, event: dict, event_list: list[dict]) -> int:
        """查找是否有重复事件"""
        if not event_list:
            return -1

        event_text = self._get_event_text(event)
        event_vector = self.vectorizer.transform([event_text])

        texts = [self._get_event_text(e) for e in event_list]
        existing_vectors = self.vectorizer.transform(texts)

        similarities = cosine_similarity(event_vector, existing_vectors)[0]
        max_idx = int(np.argmax(similarities))
        max_similarity = float(similarities[max_idx])

        return max_idx if max_similarity >= self.similarity_threshold else -1

    def _merge_two_events(self, event1: dict, event2: dict) -> dict:
        """合并两个相似事件"""
        merged = event1.copy()
        # 优先保留信息更丰富的
        for key in ['name', 'summary', 'time', 'location']:
            if not merged.get(key) and event2.get(key):
                merged[key] = event2.get(key)
            # 如果event2信息更完整也更新
            elif merged.get(key) and event2.get(key) and len(str(event2.get(key))) > len(str(merged.get(key))):
                merged[key] = event2.get(key)
        # 合并来源
        if isinstance(merged.get('sources'), list) and isinstance(event2.get('sources'), list):
            merged['sources'] = list(set(merged['sources'] + event2['sources']))
        return merged

    def reset(self):
        """重置索引"""
        self.event_index = []
        self.vector_index = None
        self._is_initialized = False
        self.vectorizer = TfidfVectorizer()
