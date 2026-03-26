"""
最终测试脚本 - 使用Truth_data验证所有核心功能
"""
import asyncio
import time
import json
from pathlib import Path


class TruthDataFinalTester:
    """使用Truth_data进行最终验证"""

    def __init__(self):
        self.data_dir = Path("Truth_data")
        self.results = []

    def load_json(self, filename):
        """加载JSON文件"""
        with open(self.data_dir / filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    async def test_decision_service(self):
        """测试决策服务"""
        print("\n" + "="*70)
        print("测试决策服务 - 使用Truth_data")
        print("="*70)

        from src.services.decision_service import get_decision_service

        service = get_decision_service()

        # 加载Ground Truth
        gt_data = self.load_json("ground_truth.json")
        gt_records = gt_data.get("ground_truth_records", gt_data)

        print(f"\n测试样本: {len(gt_records)} 个商家")

        total_hot_hits = 0
        total_restock_hits = 0
        total_tests = 0

        for i, gt in enumerate(gt_records[:5]):  # 测试前5个
            merchant_id = gt.get("merchant_id", "")
            expected_hot = gt.get("expected_hot_products", [])[:10]
            expected_restock = gt.get("expected_restock_products", [])[:5]

            print(f"\n[{i+1}/5] 测试商家: {merchant_id}")

            start = time.time()
            decision = await service.generate_decision(merchant_id)
            elapsed = time.time() - start

            actual_hot = [p["product_id"] for p in decision.get("hot_products", [])[:10]]
            actual_restock = [r["product_id"] for r in decision.get("restock_recommendations", [])]

            hot_hits = len(set(expected_hot) & set(actual_hot))
            restock_hits = len(set(expected_restock) & set(actual_restock))

            total_hot_hits += hot_hits
            total_restock_hits += restock_hits
            total_tests += 1

            print(f"   爆品命中: {hot_hits}/10")
            print(f"   补货命中: {restock_hits}/{len(expected_restock)}")
            print(f"   耗时: {elapsed:.2f}秒")

            # 短暂延迟避免输出混乱
            await asyncio.sleep(0.5)

        # 计算准确率
        hot_accuracy = total_hot_hits / (total_tests * 10)
        restock_accuracy = total_restock_hits / (total_tests * 5)

        print("\n" + "="*70)
        print("测试结果")
        print("="*70)
        print(f"爆品预测准确率: {hot_accuracy:.2%} (要求>=75%)")
        print(f"补货建议准确率: {restock_accuracy:.2%} (要求>=80%)")
        print("="*70)

        return {
            "hot_accuracy": hot_accuracy,
            "restock_accuracy": restock_accuracy,
            "hot_target": 0.75,
            "restock_target": 0.80,
            "passed": hot_accuracy >= 0.75 and restock_accuracy >= 0.80
        }

    async def test_event_agent(self):
        """测试事件理解Agent"""
        print("\n" + "="*70)
        print("测试事件理解Agent")
        print("="*70)

        from src.services.event_classifier import EventClassifier

        classifier = EventClassifier(llm_client=None)

        events_data = self.load_json("event_annotations.json")
        events = events_data.get("annotations", events_data)

        total = min(len(events), 50)  # 测试前50条
        correct = 0

        print(f"测试样本: {total} 条事件")

        for i, event in enumerate(events[:total]):
            raw_event = event.get("raw_data", event)
            expected_cat = event.get("standard_classification", "")

            result = await classifier.classify(raw_event)
            actual_cat = result.get("category", "")

            if expected_cat.lower() == actual_cat.lower():
                correct += 1

            if (i + 1) % 10 == 0:
                print(f"  进度: {i+1}/{total}")

        accuracy = correct / total

        print("\n" + "="*70)
        print("测试结果")
        print("="*70)
        print(f"分类准确率: {accuracy:.2%} (要求>=90%)")
        print("="*70)

        return {
            "accuracy": accuracy,
            "target": 0.90,
            "passed": accuracy >= 0.90
        }

    async def test_scene_agent(self):
        """测试场景分析Agent"""
        print("\n" + "="*70)
        print("测试场景分析Agent")
        print("="*70)

        from src.services.scene_inference import SceneInference

        scene_infer = SceneInference(llm_client=None)

        scenes_data = self.load_json("scene_annotations.json")
        scenes = scenes_data.get("scene_annotations", scenes_data)

        total = min(len(scenes), 50)  # 测试前50条
        correct = 0

        print(f"测试样本: {total} 条场景")

        for i, scene in enumerate(scenes[:total]):
            user_order = {
                "order_products": scene.get("order_products", []),
                "product_names": scene.get("product_names", []),
                "order_time": scene.get("order_time", "")
            }

            event_context = scene.get("context", {})

            result = await scene_infer.infer(
                user_order,
                event_context.get("candidate_scenes", []),
                event_context
            )

            expected_scene = scene.get("standard_scene", "")
            actual_scene = result.get("final_scene", "")

            if expected_scene.lower() == actual_scene.lower():
                correct += 1

            if (i + 1) % 10 == 0:
                print(f"  进度: {i+1}/{total}")

        accuracy = correct / total

        print("\n" + "="*70)
        print("测试结果")
        print("="*70)
        print(f"场景判断准确率: {accuracy:.2%} (要求>=85%)")
        print("="*70)

        return {
            "accuracy": accuracy,
            "target": 0.85,
            "passed": accuracy >= 0.85
        }

    async def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*70)
        print("Truth_data 最终测试")
        print("="*70)
        print(f"数据目录: {self.data_dir}")
        print(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

        # 测试事件理解Agent
        event_result = await self.test_event_agent()

        # 测试场景分析Agent
        scene_result = await self.test_scene_agent()

        # 测试决策服务
        decision_result = await self.test_decision_service()

        # 汇总结果
        print("\n" + "="*70)
        print("最终测试结果汇总")
        print("="*70)

        results = [
            ("事件理解Agent", event_result),
            ("场景分析Agent", scene_result),
            ("决策层Agent", decision_result)
        ]

        all_passed = True
        for name, result in results:
            status = "通过" if result["passed"] else "未通过"
            accuracy = result.get("accuracy", result.get("hot_accuracy", 0))
            target = result.get("target", result.get("hot_target", 0))
            symbol = "[OK]" if result["passed"] else "[FAIL]"

            print(f"{symbol} {name}: {accuracy:.2%} (要求>={target:.0%}) {status}")

            if not result["passed"]:
                all_passed = False

        print("="*70)
        if all_passed:
            print("总体判定: 全部通过")
        else:
            print("总体判定: 部分未达标")
        print("="*70)

        # 保存测试报告
        report = {
            "测试时间": time.strftime("%Y-%m-%d %H:%M:%S"),
            "数据来源": str(self.data_dir),
            "测试结果": {
                "事件理解Agent": event_result,
                "场景分析Agent": scene_result,
                "决策层Agent": decision_result
            },
            "总体判定": "通过" if all_passed else "未通过"
        }

        report_file = "Truth_data_FINAL_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n测试报告已保存: {report_file}")

        return all_passed


if __name__ == "__main__":
    tester = TruthDataFinalTester()
    asyncio.run(tester.run_all_tests())
