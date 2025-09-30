"""
长白山天气预测模块
"""

import appbuilder
from config import Config
import os

# 设置环境中的TOKEN
os.environ["APPBUILDER_TOKEN"] = Config.APPBUILDER_TOKEN

# 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID
app_id = Config.APP_ID


def get_weather_prediction(start_date, end_date):
    """
    获取长白山天气预测
    
    Args:
        start_date (str): 开始日期，格式：YYYY-MM-DD
        end_date (str): 结束日期，格式：YYYY-MM-DD
    
    Returns:
        dict: 包含预测结果和对话ID的字典
    """
    try:
        # 创建新的对话用于天气预测
        app_builder_client = appbuilder.AppBuilderClient(app_id)
        conversation_id = app_builder_client.create_conversation()
        
        # 构建天气预测的prompt
        weather_prompt = f"""
你是一个专业的气象专家，请为长白山地区提供详细的天气预测分析。

预测时间范围：{start_date} 至 {end_date}

请严格按照以下Markdown格式返回结果，确保结构清晰、层次分明：

# 🌤️ 长白山天气预测报告

## 📊 天气概况
> 整体天气趋势和主要特点（2-3句话概括）

## 📅 每日详细预报

### {start_date}
- **🌡️ 温度**: 最高 XX°C / 最低 XX°C
- **🌧️ 降水**: 概率 XX% | 类型：XX | 时段：XX
- **💨 风力**: XX级 | 风向：XX | 阵风：XX级
- **🌫️ 天气**: XX | 能见度：XX | 湿度：XX%

### {end_date}
- **🌡️ 温度**: 最高 XX°C / 最低 XX°C
- **🌧️ 降水**: 概率 XX% | 类型：XX | 时段：XX
- **💨 风力**: XX级 | 风向：XX | 阵风：XX级
- **🌫️ 天气**: XX | 能见度：XX | 湿度：XX%

## 🏔️ 长白山特色天气

| 项目 | 详情 |
|------|------|
| 🏔️ 山顶温度 | 比山脚低8-10°C |
| 🏞️ 天池区域 | 风力较大，温度较低 |
| ⛰️ 海拔影响 | 每升高100米温度下降0.6°C |
| 🌡️ 温差变化 | 昼夜温差可达15-20°C |

## 🎒 旅游建议

### 👕 穿衣建议
- 建议穿着：XX
- 必备物品：XX
- 特殊提醒：XX

### 🏃 户外活动
- 推荐活动：XX
- 最佳时间：XX
- 注意事项：XX

### ⚠️ 安全提醒
- 重要提醒：XX
- 风险提示：XX
- 应急准备：XX

## 🚨 天气预警
> 如有极端天气，请在此处详细说明

---

**预测时间**: {start_date} 至 {end_date}  
**更新时间**: 实时更新  
**数据来源**: 长白山气象站 + AI智能分析

请确保：
1. 所有温度使用摄氏度
2. 风力使用中文描述（如：微风、3-4级风等）
3. 降水概率使用百分比
4. 内容专业且实用
5. 针对长白山地区的气候特点
6. 使用丰富的emoji图标增强可读性
        """
        
        # 调用百度AI接口
        resp = app_builder_client.run(conversation_id, weather_prompt)
        
        return {
            'prediction': resp.content.answer,
            'conversation_id': conversation_id
        }
        
    except Exception as e:
        raise Exception(f'天气预测失败: {str(e)}')


def validate_date_range(start_date, end_date):
    """
    验证日期范围是否有效
    
    Args:
        start_date (str): 开始日期
        end_date (str): 结束日期
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not start_date or not end_date:
        return False, '请提供开始和结束日期'
    
    try:
        from datetime import datetime
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start > end:
            return False, '开始日期不能晚于结束日期'
        
        # 检查日期范围是否在合理范围内（前后3个月）
        from datetime import datetime, timedelta
        today = datetime.now()
        min_date = today - timedelta(days=90)
        max_date = today + timedelta(days=90)
        
        if start < min_date or end > max_date:
            return False, '日期范围超出允许范围（前后3个月）'
        
        return True, None
        
    except ValueError:
        return False, '日期格式不正确，请使用YYYY-MM-DD格式'
    except Exception as e:
        return False, f'日期验证失败: {str(e)}'


def get_weather_summary():
    """
    获取天气预测功能的简要说明
    
    Returns:
        dict: 功能说明信息
    """
    return {
        'name': '长白山天气预测',
        'description': '基于AI技术的长白山地区天气预测服务',
        'features': [
            '智能天气预测',
            '结构化Markdown展示',
            '旅游建议',
            '长白山特色天气分析'
        ],
        'supported_formats': ['Markdown'],
        'max_date_range': '前后3个月'
    }
