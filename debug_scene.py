"""调试场景推理"""
import json
from src.services.scene_inference import SceneInference

# 加载测试数据
with open('Truth_data_Aligned/scene_annotations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
scenes = data['scene_annotations']

# 测试前50条
scene_infer = SceneInference(llm_client=None)
mismatches = []

for i, scene in enumerate(scenes[:50]):
    user_order = {
        'order_products': scene.get('order_products', []),
        'product_names': scene.get('product_names', []),
        'order_time': scene.get('order_time', '')
    }
    event_context = scene.get('context', {})
    truth_scene = scene.get('standard_scene', '')

    result = scene_infer._rule_based_inference(user_order, [], event_context)
    actual_scene = result.get('final_scene', '')

    if truth_scene != actual_scene:
        mismatches.append({
            'id': i+1,
            'truth': truth_scene,
            'actual': actual_scene,
            'products': scene.get('product_names', [])
        })

print(f'不匹配样例 ({len(mismatches)}/50):')
for m in mismatches[:8]:
    print(f"{m['id']}. 期望'{m['truth']}' 实际'{m['actual']}'")
    print(f"   商品: {m['products'][:3]}")
