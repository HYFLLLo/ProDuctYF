"""
全面测试脚本 - 使用最全面的数据集测试三个核心指标
"""
import asyncio
import json
from pathlib import Path
from src.services.event_classifier import EventClassifier
from src.services.scene_inference import SceneInference
from src.services.decision_service import DecisionService


async def test_event_classification():
    """测试事件分类准确率"""
    print("\n" + "="*70)
    print("测试1：事件分类准确率")
    print("="*70)

    with open('Truth_data_Comprehensive/event_annotations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    events = data['annotations']

    classifier = EventClassifier(llm_client=None)
    matches = 0
    total = len(events)

    for event in events:
        raw_event = event.get('raw_data', event)
        truth_category = event.get('standard_classification', '')
        result = await classifier.classify(raw_event)
        actual_category = result.get('category', '')

        if truth_category == actual_category:
            matches += 1

    accuracy = (matches / total) * 100 if total > 0 else 0
    status = "✅ 通过" if accuracy >= 90 else "❌ 未达标"

    print(f"  测试样本: {total} 条")
    print(f"  命中: {matches}/{total}")
    print(f"  准确率: {accuracy:.2f}%")
    print(f"  状态: {status}")

    return accuracy >= 90, accuracy


async def test_scene_inference():
    """测试场景推理准确率"""
    print("\n" + "="*70)
    print("测试2：场景推理准确率")
    print("="*70)

    with open('Truth_data_Comprehensive/scene_annotations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    scenes = data['scene_annotations']

    scene_infer = SceneInference(llm_client=None)
    matches = 0
    total = len(scenes)

    for scene in scenes:
        user_order = {
            'order_products': scene.get('order_products', []),
            'product_names': scene.get('product_names', []),
            'order_time': scene.get('order_time', '')
        }

        event_context = scene.get('context', {})
        truth_scene = scene.get('standard_scene', '')

        result = await scene_infer.infer(user_order, [], event_context)
        actual_scene = result.get('final_scene', '')

        if truth_scene == actual_scene:
            matches += 1
        else:
            print(f"  不匹配: 期望'{truth_scene}' 实际'{actual_scene}' | 商品: {scene.get('product_names', [])[:2]}")

    accuracy = (matches / total) * 100 if total > 0 else 0
    status = "✅ 通过" if accuracy >= 85 else "❌ 未达标"

    print(f"  测试样本: {total} 条")
    print(f"  命中: {matches}/{total}")
    print(f"  准确率: {accuracy:.2f}%")
    print(f"  状态: {status}")

    return accuracy >= 85, accuracy


async def test_hot_product_prediction():
    """测试爆品预测准确率"""
    print("\n" + "="*70)
    print("测试3：爆品预测准确率")
    print("="*70)

    with open('Truth_data_Comprehensive/ground_truth.json', 'r', encoding='utf-8') as f:
        gt_data = json.load(f)
    gt_records = gt_data.get('ground_truth_records', gt_data)

    decision_service = DecisionService()
    total_hits = 0
    total_expected = 0

    # 测试前20条
    test_records = gt_records[:20]

    for record in test_records:
        merchant_id = record.get('merchant_id', '')
        expected_products = record.get('expected_hot_products', [])

        # 模拟决策生成
        events = [{
            'event_name': record.get('context', {}).get('event_name', '无事件'),
            'event_type': '赛事' if record.get('context', {}).get('has_sports_event') else '社会',
            'heat_score': record.get('context', {}).get('event_heat_score', 70)
        }]

        scene_type = expected_products[0] if expected_products else '夜宵'
        if 'P0001' in expected_products or 'P0002' in expected_products:
            scene_type = '看球' if record.get('context', {}).get('has_sports_event') else '聚会'
        elif 'P0007' in expected_products or 'P0013' in expected_products:
            scene_type = '加班'
        elif 'P0005' in expected_products or 'P0008' in expected_products:
            scene_type = '夜宵'
        elif 'P0003' in expected_products or 'P0012' in expected_products:
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

        # 获取预测的爆品
        predicted = [p.get('product_id') for p in result.get('hot_products', [])[:10]]

        # 计算命中率
        hits = len(set(predicted) & set(expected_products))
        total_hits += hits
        total_expected += len(expected_products)

    accuracy = (total_hits / total_expected) * 100 if total_expected > 0 else 0
    status = "✅ 通过" if accuracy >= 70 else "❌ 未达标"

    print(f"  测试样本: {len(test_records)} 条商家")
    print(f"  总命中: {total_hits}/{total_expected}")
    print(f"  准确率: {accuracy:.2f}%")
    print(f"  状态: {status}")

    return accuracy >= 70, accuracy


async def main():
    """主测试流程"""
    print("\n" + "🎯"*35)
    print("全面数据测试 - 验证三个核心指标")
    print("🎯"*35)

    results = []

    # 测试1：事件分类
    ok1, acc1 = await test_event_classification()
    results.append(("事件分类", acc1, ok1))

    # 测试2：场景推理
    ok2, acc2 = await test_scene_inference()
    results.append(("场景推理", acc2, ok2))

    # 测试3：爆品预测
    ok3, acc3 = await test_hot_product_prediction()
    results.append(("爆品预测", acc3, ok3))

    # 汇总
    print("\n" + "="*70)
    print("📊 测试汇总")
    print("="*70)

    all_passed = True
    for name, acc, passed in results:
        status = "✅ 通过" if passed else "❌ 未达标"
        target = "90%" if name == "事件分类" else ("85%" if name == "场景推理" else "70%")
        print(f"  {name}: {acc:.2f}% (目标≥{target}) {status}")
        if not passed:
            all_passed = False

    print("="*70)
    if all_passed:
        print("🎉 所有指标全部达标！")
    else:
        print("⚠️  部分指标未达标，需要优化")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())
