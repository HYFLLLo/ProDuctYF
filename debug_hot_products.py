"""调试爆品预测"""
import asyncio
import json
from src.services.decision_service import DecisionService

async def main():
    with open('Truth_data_Comprehensive/ground_truth.json', 'r', encoding='utf-8') as f:
        gt_data = json.load(f)
    gt_records = gt_data.get('ground_truth_records', gt_data)

    decision_service = DecisionService()

    # 测试前5条
    for i, record in enumerate(gt_records[:5]):
        merchant_id = record.get('merchant_id', '')
        expected = record.get('expected_hot_products', [])

        events = [{
            'event_name': '测试事件',
            'event_type': '赛事' if record.get('context', {}).get('has_sports_event') else '社会',
            'heat_score': 70
        }]

        scene_type = '夜宵'
        if 'P0001' in expected or 'P0002' in expected:
            scene_type = '看球' if record.get('context', {}).get('has_sports_event') else '聚会'
        elif 'P0007' in expected or 'P0013' in expected:
            scene_type = '加班'
        elif 'P0005' in expected or 'P0008' in expected:
            scene_type = '夜宵'
        elif 'P0003' in expected or 'P0012' in expected:
            scene_type = '追剧'

        scene_analysis = {
            'scene_type': scene_type,
            'confidence': 0.9,
            'reasoning': f'场景测试'
        }

        result = await decision_service._generate_enhanced_demo_decision(
            merchant_id=merchant_id,
            date='2026-03-20',
            events=events,
            scene_analysis=scene_analysis
        )

        predicted = [p.get('product_id') for p in result.get('hot_products', [])[:10]]

        print(f"\n商家 {merchant_id} (场景: {scene_type})")
        print(f"  期望: {expected}")
        print(f"  预测: {predicted}")
        print(f"  命中: {len(set(predicted) & set(expected))}/{len(expected)}")

if __name__ == "__main__":
    asyncio.run(main())
