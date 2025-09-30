#!/usr/bin/env python3
"""
调试日期显示问题
"""

import requests
from datetime import datetime, timedelta

def debug_date_issue():
    """调试日期显示问题"""
    
    print("调试日期显示问题...")
    print("=" * 60)
    
    # 获取当前时间信息
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    
    print("当前时间信息:")
    print(f"今天: {today.strftime('%Y-%m-%d')} ({today.strftime('%A')})")
    print(f"明天: {tomorrow.strftime('%Y-%m-%d')} ({tomorrow.strftime('%A')})")
    
    print("\n检查页面HTML内容:")
    print("-" * 40)
    
    try:
        response = requests.get('http://localhost:3000/weather', timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            
            # 检查日期输入框
            if 'id="startDate"' in html_content:
                print("✅ 开始日期输入框存在")
            else:
                print("❌ 开始日期输入框不存在")
                
            if 'id="endDate"' in html_content:
                print("✅ 结束日期输入框存在")
            else:
                print("❌ 结束日期输入框不存在")
            
            # 检查JavaScript代码
            if 'initializeDateRange' in html_content:
                print("✅ 日期初始化函数存在")
            else:
                print("❌ 日期初始化函数不存在")
                
            if 'setDate(today.getDate() + 1)' in html_content:
                print("✅ 日期设置逻辑存在")
            else:
                print("❌ 日期设置逻辑不存在")
                
            # 检查是否有默认值设置
            if 'value=' in html_content and 'date' in html_content:
                print("✅ 日期输入框有默认值设置")
            else:
                print("❌ 日期输入框没有默认值设置")
                
        else:
            print(f"❌ 页面访问失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
    except Exception as e:
        print(f"❌ 调试失败: {str(e)}")
    
    print("\n可能的解决方案:")
    print("-" * 40)
    print("1. 清除浏览器缓存")
    print("2. 硬刷新页面 (Ctrl+F5 或 Cmd+Shift+R)")
    print("3. 检查浏览器控制台是否有JavaScript错误")
    print("4. 确认页面完全加载后再查看日期")
    
    print("\n手动测试步骤:")
    print("-" * 40)
    print("1. 打开浏览器访问: http://localhost:3000/weather")
    print("2. 按F12打开开发者工具")
    print("3. 查看Console标签页的日志输出")
    print("4. 检查日期输入框的实际值")
    print("5. 如果日期不正确，尝试手动点击日期输入框")

if __name__ == "__main__":
    debug_date_issue()
    print("\n" + "=" * 60)
    print("调试完成!")
