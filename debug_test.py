import sys
sys.path.insert(0, '.')

from tests.agent_pipeline_test import AgentPipelineEvaluator

evaluator = AgentPipelineEvaluator()

order_context = {
    "order_time": "02:00",
    "is_weekend": False,
    "user_occupation": "设计师",
    "location_type": "公寓"
}

raw_events = [
    "娱乐：周杰伦演唱会广州站门票开售",
    "天气：晴，气温20度",
    "体育：CBA季后赛广东VS辽宁"
]

result = evaluator._rule_infer_scene(order_context, raw_events)
print(f"Predicted: {result}")
print(f"Expected: 独饮")
print(f"Match: {result == '独饮'}")

hour = int(order_context["order_time"].split(":")[0])
location = order_context["location_type"]
print(f"Hour: {hour}")
print(f"Location: {location}")
print(f"hour >= 1 and hour < 6: {hour >= 1 and hour < 6}")
print(f"Location in [公寓, 出租屋, 居民区]: {location in ['公寓', '出租屋', '居民区']}")
