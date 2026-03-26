"""检查decision_service加载ground_truth"""
from pathlib import Path
import json

truth_data_dir = Path("Truth_data_Comprehensive")
gt_file = truth_data_dir / "ground_truth.json"

print(f"检查文件: {gt_file}")
print(f"文件存在: {gt_file.exists()}")

if gt_file.exists():
    with open(gt_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    records = data.get("ground_truth_records", data)
    print(f"记录数量: {len(records)}")

    # 检查M001
    for r in records:
        if r.get('merchant_id') == 'M001':
            print(f"\n找到M001:")
            print(f"  expected_hot_products: {r.get('expected_hot_products')}")
            print(f"  real_sales_data: {list(r.get('real_sales_data', {}).keys())}")
