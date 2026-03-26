"""调试事件分类"""
import asyncio
import json
from src.services.event_classifier import EventClassifier

# 加载测试数据
with open('Truth_data_Aligned/event_annotations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
events = data['annotations']

# 测试前50条
classifier = EventClassifier(llm_client=None)
mismatches = []

for i, event in enumerate(events[:50]):
    raw_event = event.get('raw_data', event)
    truth_category = event.get('standard_classification', '')

    result = asyncio.run(classifier.classify(raw_event))
    actual_category = result.get('category', '')

    if truth_category != actual_category:
        mismatches.append({
            'id': i+1,
            'truth': truth_category,
            'actual': actual_category,
            'event_name': raw_event.get('event_name', '')
        })

print(f'不匹配样例 ({len(mismatches)}/50):')
for m in mismatches[:8]:
    print(f"{m['id']}. 期望'{m['truth']}' 实际'{m['actual']}'")
    print(f"   事件: {m['event_name']}")
