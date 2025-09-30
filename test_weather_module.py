#!/usr/bin/env python3
"""
测试天气模块的功能
"""

import requests
import json
from weather import get_weather_prediction, validate_date_range, get_weather_summary

def test_weather_module():
    """测试天气模块功能"""
    
    print("测试天气模块功能...")
    print("=" * 50)
    
    # 测试日期验证功能
    print("1. 测试日期验证功能:")
    print("-" * 30)
    
    # 有效日期
    is_valid, error = validate_date_range('2025-10-01', '2025-10-03')
    print(f"有效日期测试: {is_valid}, 错误信息: {error}")
    
    # 无效日期（开始日期晚于结束日期）
    is_valid, error = validate_date_range('2025-10-03', '2025-10-01')
    print(f"无效日期测试: {is_valid}, 错误信息: {error}")
    
    # 空日期
    is_valid, error = validate_date_range('', '2025-10-01')
    print(f"空日期测试: {is_valid}, 错误信息: {error}")
    
    print("\n2. 测试天气预测功能:")
    print("-" * 30)
    
    try:
        result = get_weather_prediction('2025-10-01', '2025-10-02')
        print("✅ 天气预测功能正常")
        print(f"预测结果长度: {len(result.get('prediction', ''))}")
        print(f"对话ID: {result.get('conversation_id', 'N/A')}")
    except Exception as e:
        print(f"❌ 天气预测功能异常: {str(e)}")
    
    print("\n3. 测试天气模块信息:")
    print("-" * 30)
    
    summary = get_weather_summary()
    print(f"模块名称: {summary['name']}")
    print(f"模块描述: {summary['description']}")
    print(f"支持格式: {', '.join(summary['supported_formats'])}")
    print(f"最大日期范围: {summary['max_date_range']}")
    
    print("\n4. 测试API接口:")
    print("-" * 30)
    
    try:
        response = requests.post(
            'http://localhost:3000/api/weather-predict',
            json={
                'start_date': '2025-10-01',
                'end_date': '2025-10-02'
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ API接口正常")
            data = response.json()
            print(f"响应包含预测结果: {'prediction' in data}")
            print(f"响应包含对话ID: {'conversation_id' in data}")
        else:
            print(f"❌ API接口异常: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保应用正在运行")
    except Exception as e:
        print(f"❌ API测试失败: {str(e)}")

if __name__ == "__main__":
    test_weather_module()
    print("\n" + "=" * 50)
    print("测试完成!")
