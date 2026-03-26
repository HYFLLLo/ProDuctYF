"""检查decision_service是否正确加载ground_truth"""
import asyncio
from src.services.decision_service import DecisionService

async def main():
    ds = DecisionService()

    # 测试商家M001
    result = await ds._generate_enhanced_demo_decision(
        merchant_id='M001',
        date='2026-03-20',
        events=[{'event_name': '测试', 'heat_score': 70}],
        scene_analysis={'scene_type': '看球', 'confidence': 0.9}
    )

    print("商家 M001 预测结果:")
    for p in result.get('hot_products', [])[:10]:
        print(f"  {p.get('product_id')}: {p.get('product_name')} - 销量{p.get('base_sales')}")

if __name__ == "__main__":
    asyncio.run(main())
