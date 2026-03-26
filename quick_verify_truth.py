"""
Truth_data 快速验证脚本
"""
import json
from pathlib import Path


def main():
    data_dir = Path("Truth_data")

    print("="*60)
    print("Truth_data 数据集验证")
    print("="*60)

    files = [
        ("weather_events.json", "天气事件"),
        ("sports_events.json", "体育赛事"),
        ("social_media_events.json", "社交媒体"),
        ("all_events.json", "所有事件"),
        ("event_annotations.json", "事件标注"),
        ("merchants.json", "商家档案"),
        ("products.json", "商品品类"),
        ("inventory.json", "库存数据"),
        ("scene_annotations.json", "场景标注"),
        ("ground_truth.json", "Ground Truth")
    ]

    total_records = 0

    for filename, description in files:
        filepath = data_dir / filename

        if not filepath.exists():
            print(f"[FAIL] {description}: 文件不存在")
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 统计数量
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict):
                if "annotations" in data:
                    count = len(data["annotations"])
                elif "ground_truth_records" in data:
                    count = len(data["ground_truth_records"])
                elif "scene_annotations" in data:
                    count = len(data["scene_annotations"])
                else:
                    count = len(data)
            else:
                count = 0

            total_records += count
            print(f"[OK] {description}: {count} 条")

        except Exception as e:
            print(f"[ERROR] {description}: {e}")

    print("="*60)
    print(f"总计: {total_records} 条数据")
    print("="*60)


if __name__ == "__main__":
    main()
