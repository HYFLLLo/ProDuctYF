"""
FastAPI应用入口
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime
from pathlib import Path

app = FastAPI(
    title="AI夜宵爆品预测助手",
    version="1.0.0",
    description="即时零售夜间场景的B端智能决策SaaS服务"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


# ============ 请求/响应模型 ============

class DecisionRequest(BaseModel):
    merchant_id: str
    date: Optional[str] = None


class ProductItem(BaseModel):
    product_id: str
    product_name: str
    predicted_sales: Optional[float] = None


class RestockItem(BaseModel):
    product_id: str
    recommended_quantity: int
    urgency: str


class PricingItem(BaseModel):
    product_id: str
    current_price: float
    recommended_price: float


class DecisionResponse(BaseModel):
    decision_id: str
    merchant_id: str
    merchant_name: Optional[str] = None
    chain_brand: Optional[str] = None
    city: Optional[str] = None
    snack_culture: Optional[str] = None
    recommended_categories: List[str] = []
    hot_products: List[dict]
    restock_recommendations: List[dict]
    pricing_recommendations: List[dict]
    bundle_strategies: List[dict] = []
    created_at: str
    analysis: Optional[dict] = None
    hourly_sales_trend: List[dict] = []
    category_summary: List[dict] = []
    key_factors: Optional[dict] = None
    ai_suggestions: List[str] = []


class EventQuery(BaseModel):
    event_type: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    page: int = 1
    page_size: int = 20


class SceneAnalyzeRequest(BaseModel):
    user_id: str
    order_products: List[dict]
    order_time: str
    total_amount: float
    event_context: Optional[dict] = {}


class AnalysisRequest(BaseModel):
    merchant_id: str
    scene_type: str
    hot_products: List[dict]
    restock: List[dict]
    pricing: List[dict]


class AnalysisResponse(BaseModel):
    reasoning: str
    confidence: float


# ============ API路由 ============

@app.get("/", response_class=HTMLResponse)
async def root():
    """前端页面"""
    html_path = Path(__file__).parent / "static" / "index.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return {
        "message": "AI夜宵爆品预测助手 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/v1/analysis/generate", response_model=AnalysisResponse)
async def generate_analysis(request: AnalysisRequest):
    """
    生成AI分析理由

    基于爆品预测、补货建议、定价建议生成智能分析报告
    """
    from src.services.decision_service import get_decision_service

    decision_service = get_decision_service()
    result = await decision_service.generate_llm_analysis(
        merchant_id=request.merchant_id,
        scene_type=request.scene_type,
        hot_products=request.hot_products,
        restock=request.restock,
        pricing=request.pricing
    )

    return AnalysisResponse(
        reasoning=result.get("reasoning", ""),
        confidence=result.get("confidence", 0.9)
    )


@app.post("/api/v1/merchants/{merchant_id}/decisions", response_model=DecisionResponse)
async def get_decisions(merchant_id: str, request: DecisionRequest):
    """
    获取商家决策结果

    返回爆品清单、补货建议、定价建议、套餐组合
    """
    from src.services.decision_service import get_decision_service

    decision_service = get_decision_service()
    result = await decision_service.generate_decision(merchant_id, request.date)

    return DecisionResponse(
        decision_id=result["decision_id"],
        merchant_id=result["merchant_id"],
        merchant_name=result.get("merchant_name"),
        chain_brand=result.get("chain_brand"),
        city=result.get("city"),
        snack_culture=result.get("snack_culture"),
        recommended_categories=result.get("recommended_categories", []),
        hot_products=result["hot_products"],
        restock_recommendations=result["restock_recommendations"],
        pricing_recommendations=result["pricing_recommendations"],
        bundle_strategies=result.get("bundle_strategies", []),
        created_at=result["created_at"],
        analysis=result.get("analysis"),
        hourly_sales_trend=result.get("hourly_sales_trend", []),
        category_summary=result.get("category_summary", []),
        key_factors=result.get("key_factors"),
        ai_suggestions=result.get("ai_suggestions", [])
    )


@app.get("/api/v1/events")
async def get_events(
    event_type: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    page: int = 1,
    page_size: int = 20
):
    """
    查询事件列表

    支持按类型、时间范围筛选
    """
    # TODO: 实际应查询数据库
    return {
        "items": [],
        "total": 0,
        "page": page,
        "page_size": page_size
    }


@app.post("/api/v1/scene/analyze")
async def analyze_scene(request: SceneAnalyzeRequest):
    """
    分析用户场景

    输入用户订单和上下文，返回场景类型和推荐商品
    """
    # TODO: 实际应调用场景分析服务
    return {
        "user_id": request.user_id,
        "scene_type": "看球",
        "confidence": 0.85,
        "reasoning": "订单包含啤酒和零食，时间在赛事期间",
        "recommended_products": [
            {"product_id": "P010", "product_name": "花生", "priority": "高"},
            {"product_id": "P011", "product_name": "鸡爪", "priority": "中"}
        ]
    }


@app.get("/api/v1/events/context")
async def get_event_context():
    """
    获取当前事件上下文

    返回活跃事件列表
    """
    # TODO: 实际应查询事件服务
    return {
        "active_events": [
            {
                "event_id": "E001",
                "event_name": "赛事：阿根廷 vs 法国",
                "event_type": "赛事",
                "heat": 95
            }
        ],
        "weather": "晴"
    }


# ============ 运营后台API ============

@app.get("/api/v1/admin/events")
async def admin_get_events(
    needs_review: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20
):
    """运营后台：事件列表"""
    return {
        "items": [],
        "total": 0,
        "page": page,
        "page_size": page_size
    }


@app.get("/api/v1/admin/review/pending")
async def admin_review_pending():
    """运营后台：待复核事件"""
    return {
        "items": [],
        "total": 0
    }


@app.post("/api/v1/admin/review/{event_id}")
async def admin_submit_review(event_id: str, category: str, operator: str):
    """运营后台：提交复核结果"""
    return {
        "code": 0,
        "message": "复核成功",
        "event_id": event_id,
        "category": category,
        "operator": operator
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
