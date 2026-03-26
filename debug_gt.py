"""直接检查Ground Truth数据"""
import json

with open('Truth_data_Comprehensive/ground_truth.json', 'r', encoding='utf-8') as f:
    gt_data = json.load(f)
gt_records = gt_data.get('ground_truth_records', gt_data)

print("前5条Ground Truth:")
for i, record in enumerate(gt_records[:5]):
    print(f"\n{i+1}. 商家 {record.get('merchant_id')}")
    print(f"   期望爆品: {record.get('expected_hot_products')}")
    print(f"   真实销量:")
    for pid, info in record.get('real_sales_data', {}).items():
        print(f"      {pid}: {info.get('product_name')} - 销量{info.get('actual_sales')}")
