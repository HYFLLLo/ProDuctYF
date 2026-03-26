"""调试聚会场景"""
import asyncio
import json
from src.services.scene_inference import SceneInference

async def main():
    with open('Truth_data_Comprehensive/scene_annotations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    scenes = data['scene_annotations']

    scene_infer = SceneInference(llm_client=None)

    for scene in scenes:
        truth = scene.get('standard_scene', '')
        if truth != '聚会':
            continue

        user_order = {
            'order_products': scene.get('order_products', []),
            'product_names': scene.get('product_names', []),
            'order_time': scene.get('order_time', '')
        }
        event_context = scene.get('context', {})

        result = await scene_infer.infer(user_order, [], event_context)
        actual = result.get('final_scene', '')

        if truth != actual:
            print(f"\n期望'{truth}' 实际'{actual}'")
            print(f"  商品: {scene.get('product_names', [])}")
            print(f"  规则推理: {result}")

if __name__ == "__main__":
    asyncio.run(main())
