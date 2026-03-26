"""
数据采集模块 - 基础采集器抽象类
"""
import json
import hashlib
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Optional


class BaseCollector(ABC):
    """数据采集器基类"""

    def __init__(self, source_name: str, api_config: dict):
        self.source_name = source_name
        self.api_config = api_config

    @abstractmethod
    async def collect(self, time_range: tuple[datetime, datetime]) -> list[dict]:
        """采集数据，返回事件列表"""
        pass

    async def normalize(self, raw_event: dict) -> dict:
        """标准化事件数据格式"""
        return {
            "event_id": self._generate_event_id(raw_event),
            "source": self.source_name,
            "raw_content": json.dumps(raw_event, ensure_ascii=False),
            "collected_at": datetime.now(),
            "status": "pending"
        }

    def _generate_event_id(self, raw_event: dict) -> str:
        """根据事件名和时间生成唯一ID"""
        content = f"{raw_event.get('name', '')}{raw_event.get('time', '')}"
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def _is_night_hours(self, time_str: str) -> bool:
        """判断是否在夜间时段(20:00-06:00)"""
        try:
            hour = int(time_str.split()[1].split(":")[0])
            return hour >= 20 or hour <= 6
        except:
            return False
