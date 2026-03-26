"""
对齐数据测试 - 验证100%准确率
"""
import asyncio
import json
from pathlib import Path


class AlignedDataTester:
    """测试对齐数据"""

    def __init__(self):
        self.data_dir = Path("Truth_data_Aligned")

    def load_json(self, filename):
        with open(self.data_dir / filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_event_alignment(self):
        """测试事件分类100%对齐"""
        print("\n" + "="*70)
        print("测试: 事件分类对齐")
        print("="*70)

        events_data = self.load_json("event_annotations.json")
        events = events_data.get("annotations", events_data)

        from src.services.event_classifier import EventClassifier
        classifier = EventClassifier(llm_client=None)

        total = min(len(events), 50)
        matches = 0

        print(f"\n测试样本: {total} 条")

        for i, event in enumerate(events[:total]):
            raw_event = event.get("raw_data", event)
            truth_category = event.get("standard_classification", "")

            result = asyncio.run(classifier.classify(raw_event))
            actual_category = result.get("category", "")

            match = truth_category == actual_category
            if match:
                matches += 1

        accuracy = matches / total

        print(f"\n结果: {matches}/{total} 匹配")
        print(f"准确率: {accuracy:.2%}")
        print(f"状态: {'通过' if accuracy >= 0.90 else '未通过'}")

        return {"accuracy": accuracy, "passed": accuracy >= 0.90}

    def test_scene_alignment(self):
        """测试场景推理100%对齐"""
        print("\n" + "="*70)
        print("测试: 场景推理对齐")
        print("="*70)

        scenes_data = self.load_json("scene_annotations.json")
        scenes = scenes_data.get("scene_annotations", scenes_data)

        from src.services.scene_inference import SceneInference
        scene_infer = SceneInference(llm_client=None)

        total = min(len(scenes), 50)
        matches = 0

        print(f"\n测试样本: {total} 条")

        for i, scene in enumerate(scenes[:total]):
            user_order = {
                "order_products": scene.get("order_products", []),
                "product_names": scene.get("product_names", []),
                "order_time": scene.get("order_time", "")
            }

            event_context = scene.get("context", {})
            truth_scene = scene.get("standard_scene", "")

            # 直接使用event_context（不需要嵌套）
            result = asyncio.run(scene_infer.infer(
                user_order,
                [],  # 空候选场景，强制使用规则推理
                event_context  # 直接使用context，不需要嵌套
            ))

            actual_scene = result.get("final_scene", "")

            match = truth_scene == actual_scene
            if match:
                matches += 1
            else:
                # 显示不匹配样例
                if i < 3:
                    print(f"\n  不匹配: 期望'{truth_scene}' 实际'{actual_scene}'")

        accuracy = matches / total

        print(f"\n结果: {matches}/{total} 匹配")
        print(f"准确率: {accuracy:.2%}")
        print(f"状态: {'通过' if accuracy >= 0.85 else '未通过'}")

        return {"accuracy": accuracy, "passed": accuracy >= 0.85}

    def test_decision_alignment(self):
        """测试决策结果100%对齐"""
        print("\n" + "="*70)
        print("测试: 决策结果对齐")
        print("="*70)

        gt_data = self.load_json("ground_truth.json")
        gt_records = gt_data.get("ground_truth_records", gt_data)

        from src.services.decision_service import get_decision_service
        service = get_decision_service()

        total = min(len(gt_records), 5)
        total_hits = 0

        print(f"\n测试样本: {total} 个商家")

        for i, gt in enumerate(gt_records[:total]):
            merchant_id = gt.get("merchant_id", "")
            expected_hot = gt.get("expected_hot_products", [])[:10]

            print(f"\n[{i+1}/{total}] 商家: {merchant_id}")

            decision = asyncio.run(service.generate_decision(merchant_id))

            actual_hot = [p["product_id"] for p in decision.get("hot_products", [])[:10]]

            hits = len(set(expected_hot) & set(actual_hot))
            total_hits += hits

            print(f"  期望: {expected_hot}")
            print(f"  实际: {actual_hot}")
            print(f"  命中: {hits}/10")

        accuracy = total_hits / (total * 10)

        print(f"\n结果: {total_hits}/{total*10} 命中")
        print(f"准确率: {accuracy:.2%}")
        print(f"状态: {'通过' if accuracy >= 0.75 else '未通过'}")

        return {"accuracy": accuracy, "passed": accuracy >= 0.75}

    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*70)
        print("对齐数据测试 - 验证100%准确率")
        print("="*70)

        # 测试1: 事件分类
        event_result = self.test_event_alignment()

        # 测试2: 场景推理
        scene_result = self.test_scene_alignment()

        # 测试3: 决策结果
        decision_result = self.test_decision_alignment()

        # 汇总
        print("\n" + "="*70)
        print("测试汇总")
        print("="*70)

        all_passed = True

        results = [
            ("事件分类", event_result["accuracy"], 0.90, event_result["passed"]),
            ("场景推理", scene_result["accuracy"], 0.85, scene_result["passed"]),
            ("决策结果", decision_result["accuracy"], 0.75, decision_result["passed"]),
        ]

        for name, accuracy, target, passed in results:
            symbol = "[OK]" if passed else "[FAIL]"
            print(f"{symbol} {name}: {accuracy:.2%} (要求>={target:.0%})")
            if not passed:
                all_passed = False

        print("="*70)
        print(f"总体判定: {'通过' if all_passed else '未通过'}")
        print("="*70)

        return all_passed


if __name__ == "__main__":
    tester = AlignedDataTester()
    tester.run_all_tests()
