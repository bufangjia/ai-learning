#!/usr/bin/env python3
"""
测试日期默认设置功能
"""

import requests
from datetime import datetime, timedelta

def test_date_default():
    """测试日期默认设置"""
    
    print("测试日期默认设置功能...")
    print("=" * 50)
    
    try:
        # 访问天气页面
        response = requests.get('http://localhost:3000/weather', timeout=10)
        
        if response.status_code == 200:
            print("✅ 天气页面访问成功")
            
            # 检查页面内容
            if "长白山天气预测" in response.text:
                print("✅ 页面内容正确")
            else:
                print("❌ 页面内容不正确")
                
            # 检查是否包含日期输入框
            if 'type="date"' in response.text:
                print("✅ 日期输入框存在")
            else:
                print("❌ 日期输入框不存在")
                
        else:
            print(f"❌ 页面访问失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保应用正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print("\n当前时间信息:")
    print("-" * 30)
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)
    
    print(f"今天: {today.strftime('%Y-%m-%d')}")
    print(f"明天: {tomorrow.strftime('%Y-%m-%d')}")
    print(f"后天: {day_after_tomorrow.strftime('%Y-%m-%d')}")
    
    print("\n预期默认日期:")
    print("-" * 30)
    print(f"开始日期（明天）: {tomorrow.strftime('%Y-%m-%d')}")
    print(f"结束日期（后天）: {day_after_tomorrow.strftime('%Y-%m-%d')}")
    
    print("\n测试API接口:")
    print("-" * 30)
    
    try:
        # 使用默认日期测试API
        response = requests.post(
            'http://localhost:3000/api/weather-predict',
            json={
                'start_date': tomorrow.strftime('%Y-%m-%d'),
                'end_date': day_after_tomorrow.strftime('%Y-%m-%d')
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ API接口正常")
            data = response.json()
            if 'prediction' in data:
                print("✅ 预测结果正常")
                print(f"预测结果长度: {len(data['prediction'])}")
            else:
                print("❌ 预测结果异常")
        else:
            print(f"❌ API接口异常: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器")
    except Exception as e:
        print(f"❌ API测试失败: {str(e)}")

if __name__ == "__main__":
    test_date_default()
    print("\n" + "=" * 50)
    print("测试完成!")
    print("\n💡 提示: 打开浏览器访问 http://localhost:3000/weather")
    print("   查看日期输入框是否默认显示明天和后天")
