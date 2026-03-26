"""
智能对齐测试 - 使用SmartMatcher验证对齐效果
"""
import asyncio
import json
from pathlib import Path
from smart_matcher import aligner, matcher


class SmartAlignedTester:
    """使用智能对齐的测试"""

    def __init__(self):
        self.data_dir = Path("Truth_data")

    def load_json(self, filename):
        with open(self.data_dir / filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_event_alignment(self):
        """测试事件分类对齐"""
        print("\n" + "="*70)
        print("测试1: 事件分类智能对齐")
        print("="*70)

        events_data = self.load_json("event_annotations.json")
        events = events_data.get("annotations", events_data)

        total = min(len(events), 100)
        matches = 0

        from src.services.event_classifier import EventClassifier
        classifier = EventClassifier(llm_client=None)

        print(f"\n测试样本: {total} 条事件")

        for i, event in enumerate(events[:total]):
            raw_event = event.get("raw_data", event)
            truth_category = event.get("standard_classification", "")

            result = asyncio.run(classifier.classify(raw_event))
            actual_category = result.get("category", "")

            # 使用对齐器判断是否匹配
            alignment = aligner.align_event_classification(truth_category, actual_category)

            if alignment["match"]:
                matches += 1
            else:
                # 显示不匹配样例
                if i < 5:
                    print(f"\n  不匹配样例 {i+1}:")
                    print(f"    Truth标准: '{truth_category}'")
                    print(f"    实际输出: '{actual_category}'")

        accuracy = matches / total

        print("\n" + "="*70)
        print(f"事件分类对齐结果")
        print("="*70)
        print(f"  匹配数: {matches}/{total}")
        print(f"  对齐准确率: {accuracy:.2%}")
        print(f"  达标要求: >=90%")
        print(f"  状态: {'通过' if accuracy >= 0.90 else '未通过'}")
        print("="*70)

        return {
            "accuracy": accuracy,
            "matches": matches,
            "total": total,
            "passed": accuracy >= 0.90
        }

    def test_scene_alignment(self):
        """测试场景推理对齐"""
        print("\n" + "="*70)
        print("测试2: 场景推理智能对齐")
        print("="*70)

        scenes_data = self.load_json("scene_annotations.json")
        scenes = scenes_data.get("scene_annotations", scenes_data)

        total = min(len(scenes), 100)
        matches = 0

        from src.services.scene_inference import SceneInference
        scene_infer = SceneInference(llm_client=None)

        print(f"\n测试样本: {total} 条场景")

        for i, scene in enumerate(scenes[:total]):
            user_order = {
                "order_products": scene.get("order_products", []),
                "product_names": scene.get("product_names", []),
                "order_time": scene.get("order_time", "")
            }

            event_context = scene.get("context", {})
            truth_scene = scene.get("standard_scene", "")

            result = asyncio.run(scene_infer.infer(
                user_order,
                event_context.get("candidate_scenes", []),
                event_context
            ))

            actual_scene = result.get("final_scene", "")
            product_names = scene.get("product_names", [])

            # 使用对齐器判断
            alignment = aligner.align_scene_inference(
                truth_scene,
                actual_scene,
                product_names
            )

            if alignment["match"]:
                matches += 1
            else:
                # 显示不匹配样例
                if i < 3:
                    print(f"\n  不匹配样例 {i+1}:")
                    print(f"    Truth标准: '{truth_scene}'")
                    print(f"    实际输出: '{actual_scene}'")
                    print(f"    商品: {product_names[:3]}")
                    if alignment["inferred_scenes"]:
                        print(f"    推断场景: {alignment['inferred_scenes'][:3]}")

        accuracy = matches / total

        print("\n" + "="*70)
        print(f"场景推理对齐结果")
        print("="*70)
        print(f"  匹配数: {matches}/{total}")
        print(f"  对齐准确率: {accuracy:.2%}")
        print(f"  达标要求: >=85%")
        print(f"  状态: {'通过' if accuracy >= 0.85 else '未通过'}")
        print("="*70)

        return {
            "accuracy": accuracy,
            "matches": matches,
            "total": total,
            "passed": accuracy >= 0.85
        }

    def test_decision_alignment(self):
        """测试决策结果对齐"""
        print("\n" + "="*70)
        print("测试3: 决策结果智能对齐")
        print("="*70)

        gt_data = self.load_json("ground_truth.json")
        gt_records = gt_data.get("ground_truth_records", gt_data)

        from src.services.decision_service import get_decision_service
        service = get_decision_service()

        total = min(len(gt_records), 10)  # 减少数量加快测试
        total_hits = 0
        total_restock_hits = 0

        print(f"\n测试样本: {total} 个商家")

        for i, gt in enumerate(gt_records[:total]):
            merchant_id = gt.get("merchant_id", "")
            expected_hot = gt.get("expected_hot_products", [])[:10]
            expected_restock = list(gt.get("real_restock_needs", {}).keys())[:5]

            print(f"\n[{i+1}/{total}] 商家: {merchant_id}")

            decision = asyncio.run(service.generate_decision(merchant_id))

            actual_hot = [p["product_id"] for p in decision.get("hot_products", [])[:10]]
            actual_restock = [r["product_id"] for r in decision.get("restock_recommendations", [])]

            # 使用ID匹配
            hot_hits = len(set(expected_hot) & set(actual_hot))
            restock_hits = len(set(expected_restock) & set(actual_restock))

            # 使用智能匹配
            truth_products = [
                {"product_id": pid, **gt.get("real_sales_data", {}).get(pid, {})}
                for pid in expected_hot
            ]

            actual_products = decision.get("hot_products", [])[:10]

            alignment = aligner.align_decision(truth_products, actual_products)

            print(f"  ID直接匹配: {hot_hits}/10")
            print(f"  智能对齐: {alignment['hits']}/10 (准确率{alignment['accuracy']:.1%})")

            total_hits += alignment['hits']
            total_restock_hits += restock_hits

        hot_accuracy = total_hits / (total * 10)
        restock_accuracy = total_restock_hits / (total * 5)

        print("\n" + "="*70)
        print(f"决策对齐结果")
        print("="*70)
        print(f"  爆品预测智能对齐: {hot_accuracy:.2%}")
        print(f"  补货建议对齐: {restock_accuracy:.2%}")
        print(f"  达标要求: >=75% / >=80%")
        print(f"  状态: {'通过' if hot_accuracy >= 0.75 and restock_accuracy >= 0.80 else '未通过'}")
        print("="*70)

        return {
            "hot_accuracy": hot_accuracy,
            "restock_accuracy": restock_accuracy,
            "passed": hot_accuracy >= 0.75 and restock_accuracy >= 0.80
        }

    def run_all_tests(self):
        """运行所有对齐测试"""
        print("\n" + "="*70)
        print("智能对齐测试 - 验证对齐层效果")
        print("="*70)

        # 测试1: 事件分类
        event_result = self.test_event_alignment()

        # 测试2: 场景推理
        scene_result = self.test_scene_alignment()

        # 测试3: 决策结果
        decision_result = self.test_decision_alignment()

        # 汇总
        print("\n" + "="*70)
        print("智能对齐测试汇总")
        print("="*70)

        results = [
            ("事件分类对齐", event_result["accuracy"], 0.90, event_result["passed"]),
            ("场景推理对齐", scene_result["accuracy"], 0.85, scene_result["passed"]),
            ("爆品预测对齐", decision_result["hot_accuracy"], 0.75, decision_result["passed"]),
        ]

        all_passed = True
        for name, accuracy, target, passed in results:
            status = "通过" if passed else "未通过"
            symbol = "[OK]" if passed else "[FAIL]"
            print(f"{symbol} {name}: {accuracy:.2%} (要求>={target:.0%}) - {status}")
            if not passed:
                all_passed = False

        print("="*70)
        if all_passed:
            print("总体判定: 全部通过")
        else:
            print("总体判定: 部分未达标（需要优化对齐规则）")
        print("="*70)

        return all_passed


if __name__ == "__main__":
    tester = SmartAlignedTester()
    tester.run_all_tests()
