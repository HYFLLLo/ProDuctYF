"""调试场景推理 - 详细分析"""
import asyncio
import json
from src.services.scene_inference import SceneInference

async def main():
    # 加载测试数据
    with open('Truth_data_Comprehensive/scene_annotations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    scenes = data['scene_annotations']

    # 测试所有场景
    scene_infer = SceneInference(llm_client=None)

    # 统计各场景准确率
    scene_stats = {}

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

        key = truth_scene
        if key not in scene_stats:
            scene_stats[key] = {'total': 0, 'correct': 0}

        scene_stats[key]['total'] += 1
        if truth_scene == actual_scene:
            scene_stats[key]['correct'] += 1
        else:
            # 打印错误样例
            if scene_stats[key]['total'] <= 3:  # 只打印前3个错误
                print(f"错误: 期望'{truth_scene}' 实际'{actual_scene}'")
                print(f"  商品: {scene.get('product_names', [])}")

    print("\n场景准确率统计:")
    for scene, stats in sorted(scene_stats.items()):
        accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"  {scene}: {stats['correct']}/{stats['total']} = {accuracy:.1f}%")

if __name__ == "__main__":
    asyncio.run(main())

print("\n场景准确率统计:")
for scene, stats in sorted(scene_stats.items()):
    accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
    print(f"  {scene}: {stats['correct']}/{stats['total']} = {accuracy:.1f}%")
