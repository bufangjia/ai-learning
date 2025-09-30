#!/usr/bin/env python3
"""
测试Markdown格式的天气预测结果展示
"""

import requests
import json

def test_markdown_weather():
    """测试Markdown格式的天气预测结果"""
    
    try:
        # 发送请求到天气预测API
        response = requests.post(
            'http://localhost:3000/api/weather-predict',
            json={
                'date': '2025-10-01'
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 天气预测API测试成功!")
            print("=" * 60)
            print("Markdown格式的预测结果:")
            print("=" * 60)
            print(result.get('prediction', '无结果'))
            print("=" * 60)
            
            # 检查是否包含Markdown元素
            prediction = result.get('prediction', '')
            if '# ' in prediction:
                print("✅ 包含标题格式")
            if '## ' in prediction:
                print("✅ 包含二级标题")
            if '|' in prediction:
                print("✅ 包含表格格式")
            if '**' in prediction:
                print("✅ 包含粗体格式")
            if '> ' in prediction:
                print("✅ 包含引用格式")
            if '---' in prediction:
                print("✅ 包含水平线")
                
        else:
            print(f"❌ API请求失败: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保应用正在运行")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    print("测试Markdown格式的天气预测结果...")
    print("=" * 60)
    test_markdown_weather()
    print("=" * 60)
    print("测试完成!")
