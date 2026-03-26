"""
测试API接口
"""
import requests
import json

def test_decision_api():
    """测试决策生成API"""
    print('='*80)
    print('🎯 决策生成API测试')
    print('='*80)

    payload = {
        'merchant_id': 'M001',
        'date': None
    }

    try:
        response = requests.post(
            'http://localhost:8000/api/v1/merchants/M001/decisions',
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print(f'✅ 状态码: {response.status_code}')
            print(f'决策ID: {result.get("decision_id")}')
            print(f'商家ID: {result.get("merchant_id")}')
            print(f'爆品数量: {len(result.get("hot_products", []))}')
            print(f'补货建议: {len(result.get("restock_recommendations", []))}')
            print(f'定价建议: {len(result.get("pricing_recommendations", []))}')

            print('\nTOP 3 爆品:')
            for i, p in enumerate(result.get('hot_products', [])[:3], 1):
                print(f'  {i}. {p.get("product_name")} (得分: {p.get("final_score", 0):.2f})')

            if result.get('analysis'):
                print(f'\n分析上下文:')
                print(f'  处理事件数: {result["analysis"].get("events_processed")}')
                print(f'  场景类型: {result["analysis"].get("scene_type")}')

            return True
        else:
            print(f'❌ 状态码: {response.status_code}')
            print(f'响应: {response.text}')
            return False

    except Exception as e:
        print(f'❌ 请求失败: {e}')
        return False

def test_event_context():
    """测试事件上下文API"""
    print('\n' + '='*80)
    print('📡 事件上下文API测试')
    print('='*80)

    try:
        response = requests.get('http://localhost:8000/api/v1/events/context', timeout=10)

        if response.status_code == 200:
            result = response.json()
            print(f'✅ 状态码: {response.status_code}')
            print(f'活跃事件数: {len(result.get("active_events", []))}')
            print(f'天气: {result.get("weather")}')

            for event in result.get('active_events', [])[:3]:
                print(f'  - {event.get("event_name")} (热度: {event.get("heat")})')

            return True
        else:
            print(f'❌ 状态码: {response.status_code}')
            return False

    except Exception as e:
        print(f'❌ 请求失败: {e}')
        return False

if __name__ == '__main__':
    print('\n🚀 开始测试AI夜宵爆品预测助手API...\n')

    # 测试健康检查
    try:
        r = requests.get('http://localhost:8000/health', timeout=5)
        print(f'✅ Health Check: {r.json()}')
    except Exception as e:
        print(f'❌ Health Check失败: {e}')

    # 测试决策API
    test_decision_api()

    # 测试事件上下文
    test_event_context()

    print('\n' + '='*80)
    print('✅ 所有测试完成！')
    print('='*80)
    print('\n📖 API文档: http://localhost:8000/docs')
    print('🌐 前端界面: http://localhost:8000/')
    print('='*80)
