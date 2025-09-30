#!/usr/bin/env python3
"""
测试长白山天气预测功能
"""

import requests
import json
from datetime import datetime, timedelta

def test_weather_prediction():
    """测试天气预测API"""
    
    # 设置测试日期（明天）
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    date = tomorrow.strftime('%Y-%m-%d')
    print(f"测试日期: {date}")
    
    # 测试数据（单日预测）
    test_data = { 'date': date }
    
    try:
        # 发送请求到天气预测API
        response = requests.post(
            'http://localhost:3000/api/weather-predict',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 天气预测API测试成功!")
            print(f"预测结果: {result.get('prediction', '无结果')[:200]}...")
        else:
            print(f"❌ API请求失败: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保应用正在运行")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_weather_page():
    """测试天气页面"""
    try:
        response = requests.get('http://localhost:3000/weather', timeout=10)
        if response.status_code == 200:
            print("✅ 天气页面访问成功!")
            if "长白山天气预测" in response.text:
                print("✅ 页面内容正确")
            else:
                print("❌ 页面内容不正确")
        else:
            print(f"❌ 天气页面访问失败: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保应用正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    print("开始测试长白山天气预测功能...")
    print("=" * 50)
    
    print("\n1. 测试天气页面访问:")
    test_weather_page()
    
    print("\n2. 测试天气预测API:")
    test_weather_prediction()
    
    print("\n" + "=" * 50)
    print("测试完成!")
