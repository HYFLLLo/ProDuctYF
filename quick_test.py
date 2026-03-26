"""
快速测试脚本 - 验证核心功能
"""
import json
from pathlib import Path


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def quick_event_test():
    """快速事件理解Agent测试"""
    print("\n" + "="*60)
    print("事件理解Agent快速测试")
    print("="*60)

    import asyncio
    from src.services.event_classifier import EventClassifier
    from src.services.heat_calculator import HeatCalculator

    classifier = EventClassifier(llm_client=None)
    heat_calculator = HeatCalculator(redis_client=None)

    events_data = load_json("test_data/events/event_annotations.json")
    events = events_data.get("annotations", events_data)

    total = len(events)
    correct = 0

    print(f"\n测试 {total} 条事件...")

    async def test_async():
        nonlocal correct
        for i, event in enumerate(events[:5]):  # 只测试前5条
            raw_event = event.get("raw_data", event)
            expected_category = event.get("standard_classification", "")

            result = await classifier.classify(raw_event)
            actual_category = result.get("category", "")

            match = "[OK]" if expected_category.lower() == actual_category.lower() else "[FAIL]"
            if match == "[OK]":
                correct += 1

            print(f"   {match} 事件{i+1}: {raw_event.get('event_name', '')[:30]}")
            print(f"      期望: {expected_category} | 实际: {actual_category}")

    asyncio.run(test_async())

    accuracy = correct / min(total, 5)
    print(f"\n分类准确率: {accuracy:.2%} (要求>=90%)")

    return accuracy >= 0.90


def quick_scene_test():
    """快速场景分析Agent测试"""
    print("\n" + "="*60)
    print("场景分析Agent快速测试")
    print("="*60)

    import asyncio
    from src.services.scene_inference import SceneInference

    scene_inference = SceneInference(llm_client=None)

    scenes_data = load_json("test_data/users/scene_annotations.json")
    scenes = scenes_data.get("scene_annotations", scenes_data)

    total = len(scenes)
    correct = 0

    print(f"\n测试 {total} 条场景...")

    async def test_async():
        nonlocal correct
        for i, scene in enumerate(scenes[:5]):  # 只测试前5条
            user_order = {
                "order_products": scene.get("order_products", []),
                "product_names": scene.get("product_names", []),
                "order_time": scene.get("order_time", "")
            }
            candidate_scenes = scene.get("context", {}).get("candidate_scenes", [])
            event_context = scene.get("context", {})
            expected_scene = scene.get("standard_scene", "")

            result = await scene_inference.infer(user_order, candidate_scenes, event_context)
            actual_scene = result.get("final_scene", "")

            match = "[OK]" if expected_scene.lower() == actual_scene.lower() else "[FAIL]"
            if match == "[OK]":
                correct += 1

            print(f"   {match} 场景{i+1}: 期望'{expected_scene}' 实际'{actual_scene}'")

    asyncio.run(test_async())

    accuracy = correct / min(total, 5)
    print(f"\n场景判断准确率: {accuracy:.2%} (要求>=85%)")

    return accuracy >= 0.85


def quick_decision_test():
    """快速决策Agent测试"""
    print("\n" + "="*60)
    print("决策层Agent快速测试")
    print("="*60)

    import asyncio
    from src.services.decision_service import get_decision_service

    service = get_decision_service()

    gt_data = load_json("test_data/ground_truth/ground_truth.json")
    gt_records = gt_data.get("ground_truth_records", gt_data)

    total = len(gt_records)
    hot_hits = 0
    restock_hits = 0

    print(f"\n测试 {total} 条决策...")

    async def run_test():
        nonlocal hot_hits, restock_hits
        for i, gt in enumerate(gt_records[:3]):  # 只测试前3条(节省时间)
            merchant_id = gt.get("merchant_id", "")
            expected_hot = list(gt.get("real_sales_data", {}).keys())[:10]
            expected_restock = list(gt.get("real_restock_needs", {}).keys())[:5]

            print(f"\n   测试商家: {merchant_id}")

            decision = await service.generate_decision(merchant_id)

            actual_hot = [p["product_id"] for p in decision.get("hot_products", [])[:10]]
            actual_restock = [r["product_id"] for r in decision.get("restock_recommendations", [])]

            # 计算命中率
            hot_match = len(set(expected_hot) & set(actual_hot))
            restock_match = len(set(expected_restock) & set(actual_restock))

            hot_hits += hot_match
            restock_hits += restock_match

            print(f"      爆品匹配: {hot_match}/10")
            print(f"      补货匹配: {restock_match}/{len(expected_restock)}")

    asyncio.run(run_test())

    hot_accuracy = hot_hits / (min(total, 3) * 10)
    restock_accuracy = restock_hits / (min(total, 3) * 5)

    print(f"\n爆品预测准确率: {hot_accuracy:.2%} (要求>=75%)")
    print(f"补货建议准确率: {restock_accuracy:.2%} (要求>=80%)")

    return hot_accuracy >= 0.75 and restock_accuracy >= 0.80


def main():
    print("\n" + "="*60)
    print("AI夜宵爆品预测助手 - 快速测试")
    print("="*60)

    # Step 1: 数据检查
    print("\n📦 数据准备检查...")
    required_files = [
        "test_data/events/event_annotations.json",
        "test_data/users/scene_annotations.json",
        "test_data/ground_truth/ground_truth.json"
    ]

    all_exist = True
    for file in required_files:
        exists = Path(file).exists()
        print(f"   {'✅' if exists else '❌'} {file}")
        all_exist = all_exist and exists

    if not all_exist:
        print("\n❌ 测试中止: 缺少数据文件")
        return False

    # Step 2: Agent测试
    event_pass = quick_event_test()
    scene_pass = quick_scene_test()
    decision_pass = quick_decision_test()

    # 结果汇总
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    print(f"   {'[OK]' if event_pass else '[FAIL]'} 事件理解Agent: {'达标' if event_pass else '不达标'}")
    print(f"   {'[OK]' if scene_pass else '[FAIL]'} 场景分析Agent: {'达标' if scene_pass else '不达标'}")
    print(f"   {'[OK]' if decision_pass else '[FAIL]'} 决策层Agent: {'达标' if decision_pass else '不达标'}")

    if event_pass and scene_pass and decision_pass:
        print("\n总体判定: 合格")
        return True
    else:
        print("\n总体判定: 部分指标未达标")
        return False


if __name__ == "__main__":
    main()
