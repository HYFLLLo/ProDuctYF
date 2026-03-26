"""
API请求/响应模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UrgencyEnum(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class StockStatusEnum(str, Enum):
    ADEQUATE = "充足"
    NORMAL = "正常"
    TIGHT = "紧张"
    OUT_OF_STOCK = "缺货"


# ============ 事件相关模型 ============

class EventBase(BaseModel):
    event_name: str
    event_type: str
    event_time: datetime
    event_location: Optional[str] = None
    summary: Optional[str] = None


class EventCreate(EventBase):
    sources: List[str] = []
    entities: List[str] = []


class EventResponse(EventBase):
    event_id: str
    event_heat: float
    heat_rank: int
    confidence: Optional[float] = None
    needs_review: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# ============ 商家决策相关模型 ============

class HotProduct(BaseModel):
    product_id: str
    product_name: str
    current_sales: Optional[float] = None
    predicted_sales: Optional[float] = None
    stock_status: StockStatusEnum = StockStatusEnum.NORMAL
    recommended_strategy: str = "维持补货"


class RestockRecommendation(BaseModel):
    product_id: str
    product_name: str
    current_stock: int
    recommended_quantity: int
    urgency: UrgencyEnum
    estimated_arrival_hours: Optional[int] = 2


class PricingRecommendation(BaseModel):
    product_id: str
    product_name: str
    current_price: float
    recommended_price: float
    adjustment_ratio: str
    reason: str


class BundleStrategy(BaseModel):
    bundle_id: str
    product_ids: List[str]
    bundle_price: float
    recommended_scene: str
    expected_effect: str


class MarketTrend(BaseModel):
    category_trend: str
    competition_situation: str
    opportunity: str


class MerchantDecision(BaseModel):
    decision_id: str
    merchant_id: str
    decision_date: str
    night_period: str
    hot_products: List[HotProduct]
    restock_recommendations: List[RestockRecommendation]
    pricing_recommendations: List[PricingRecommendation] = []
    bundle_strategies: List[BundleStrategy] = []
    market_trend: Optional[MarketTrend] = None
    adoption_status: str = "pending"
    created_at: datetime


# ============ 用户场景相关模型 ============

class SceneType(str, Enum):
    WATCH_GAME = "看球"
    OVERTIME = "加班"
    PARTY = "聚会"
    DRINK_ALONE = "独饮"
    SNACK = "零食"
    OTHER = "其他"


class UserScene(BaseModel):
    scene_id: str
    user_id: str
    scene_type: SceneType
    scene_reason: str
    confidence: float
    current_products: List[str] = []
    recommended_products: List[dict] = []
    order_time: datetime
    location: Optional[str] = None


# ============ 请求模型 ============

class SceneAnalyzeRequest(BaseModel):
    user_id: str
    order_products: List[dict]
    order_time: str
    total_amount: float
    location: Optional[str] = None
    event_context: Optional[dict] = {}


class DecisionQueryRequest(BaseModel):
    merchant_id: str
    date: Optional[str] = None
    include_pricing: bool = False
    include_bundles: bool = False


# ============ 响应模型 ============

class ApiResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[dict] = None


class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
