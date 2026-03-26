"""
系统配置
确保所有模块使用模拟数据而非真实数据库
"""
import os
from pathlib import Path


class Config:
    """系统配置"""

    # 数据模式：始终使用模拟数据
    DATA_MODE = "mock"  # 可选: "mock" | "real"

    # 数据路径配置
    DATA_DIR = Path("Truth_data")
    TEST_DATA_DIR = Path("test_data")

    # 模拟数据开关
    USE_MOCK_COLLECTORS = True       # 使用模拟采集器
    USE_MOCK_DB = True               # 使用模拟数据库
    USE_MOCK_LLM = True              # 使用模拟LLM
    USE_TRUTH_DATA = True            # 使用Truth_data

    # API配置（用于显示，实际不使用）
    WEATHER_API_KEY = "mock_key"
    SPORTS_API_KEY = "mock_key"
    SOCIAL_API_KEY = "mock_key"

    # 数据库配置（显示用，不实际连接）
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_NAME = "night_owl_prediction"
    DB_USER = "root"
    DB_PASSWORD = "mock_password"

    # LLM配置（用于显示，实际使用规则引擎）
    LLM_API_KEY = "mock_key"
    LLM_MODEL = "mock_model"

    # 系统参数
    ENABLE_LOGGING = True
    LOG_LEVEL = "INFO"
    PROCESS_DELAY = True              # 是否添加处理延迟（让用户看到处理过程）

    # 性能参数
    MAX_EVENTS = 100                 # 最大事件数
    MAX_PRODUCTS = 50                # 单次决策最大商品数
    DECISION_TIMEOUT = 30             # 决策生成超时（秒）

    @classmethod
    def get_data_path(cls, data_type: str) -> Path:
        """获取指定类型的数据路径"""
        path_map = {
            "events": cls.DATA_DIR / "event_annotations.json",
            "merchants": cls.DATA_DIR / "merchants.json",
            "products": cls.DATA_DIR / "products.json",
            "inventory": cls.DATA_DIR / "inventory.json",
            "scenes": cls.DATA_DIR / "scene_annotations.json",
            "ground_truth": cls.DATA_DIR / "ground_truth.json",
            "weather": cls.DATA_DIR / "weather_events.json",
            "sports": cls.DATA_DIR / "sports_events.json",
            "social": cls.DATA_DIR / "social_media_events.json"
        }
        return path_map.get(data_type, cls.DATA_DIR)

    @classmethod
    def is_mock_mode(cls) -> bool:
        """检查是否为模拟模式"""
        return cls.DATA_MODE == "mock" or cls.USE_MOCK_DB

    @classmethod
    def to_dict(cls):
        """转换为字典"""
        return {
            "数据模式": cls.DATA_MODE,
            "使用模拟采集器": cls.USE_MOCK_COLLECTORS,
            "使用模拟数据库": cls.USE_MOCK_DB,
            "使用Truth_data": cls.USE_TRUTH_DATA,
            "数据目录": str(cls.DATA_DIR),
            "数据库地址": f"{cls.DB_HOST}:{cls.DB_PORT}",
            "数据库名称": cls.DB_NAME
        }
