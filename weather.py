"""
长白山天气预测模块
"""

import appbuilder
from config import Config
import os
import requests

# 设置环境中的TOKEN
os.environ["APPBUILDER_TOKEN"] = Config.APPBUILDER_TOKEN

# 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID
app_id = Config.APP_ID

# 复用单例客户端，减少初始化开销
_APPBUILDER_CLIENT = appbuilder.AppBuilderClient(app_id)


def get_weather_prediction_for_date(target_date):
    """
    获取长白山某一天的天气预测

    Args:
        target_date (str): 预测日期，格式：YYYY-MM-DD

    Returns:
        dict: 包含预测结果和对话ID的字典
    """
    try:
        app_builder_client = _APPBUILDER_CLIENT
        conversation_id = app_builder_client.create_conversation()

        meteoblue_hourly_md = ''

        weather_prompt = f"""
你是一个专业的气象专家，请为长白山地区提供准确的单日天气预测，并评估景区各坡开放概率。整体数据与表达风格请参考 meteoblue（meteoblue.com）的呈现方式，但无需主动联网抓取 meteoblue 数据；请生成与该网站常见展示口径对齐的结果，并在需要时提供“可信度/不确定性”说明，保证结论严谨可信。

预测日期：{target_date}

请基于以下信息进行综合判断（无需实际联网）：
- 近60天的天气情况，重点考虑风力、降雨/降雪、极端天气对通行与安全的影响
- 长白山官网近60天的北坡/西坡/南坡开放历史（如有波动请总结规律）
- 地形差异（山顶/山脚、风口、道路条件）对当天开放概率的影响

严格按照下列 Markdown 结构输出，内容简洁清晰、可读性强：

# 🌤️ 长白山{target_date}天气预测

## 📊 天气概况
> 当天整体天气趋势和主要特点
XX

## 📅 当日详细预报（{target_date}）
- **🌡️ 温度**: 最高 XX°C / 最低 XX°C
- **🌧️ 降水**: 概率 XX% | 类型：XX | 时段：XX
- **💨 风力**: XX级 | 风向：XX | 阵风：XX级
- **🌫️ 能见度/湿度**: 能见度：XX | 湿度：XX%

## 🏔️ 当天开放概率
北坡开放概率：XX%
西坡开放概率：XX%
南坡开放概率：XX%

> 计算依据：结合近60天风力与降水等指标，以及官网过往开放记录，给出当天开放概率的主要影响因素（不超过3条）。

## 🕒 最佳登顶看天池时段（分坡位）
- 北坡：HH:MM–HH:MM（原因：1-2句，结合风力、降水、能见度与客流）
- 西坡：HH:MM–HH:MM（原因：1-2句，结合风力、降水、能见度与客流）
- 南坡：HH:MM–HH:MM（原因：1-2句，结合风力、降水、能见度与客流）

## ⏱️ 逐小时预报（{target_date} 00:00-23:00）
{meteoblue_hourly_md if meteoblue_hourly_md else "| 时段 | 温度(°C) | 天气 | 风力 | 能见度 |\n|---|---|---|---|---|\n| 00:00 | XX | XX | XX | XX |\n| 01:00 | XX | XX | XX | XX |\n| 02:00 | XX | XX | XX | XX |\n| 03:00 | XX | XX | XX | XX |\n| 04:00 | XX | XX | XX | XX |\n| 05:00 | XX | XX | XX | XX |\n| 06:00 | XX | XX | XX | XX |\n| 07:00 | XX | XX | XX | XX |\n| 08:00 | XX | XX | XX | XX |\n| 09:00 | XX | XX | XX | XX |\n| 10:00 | XX | XX | XX | XX |\n| 11:00 | XX | XX | XX | XX |\n| 12:00 | XX | XX | XX | XX |\n| 13:00 | XX | XX | XX | XX |\n| 14:00 | XX | XX | XX | XX |\n| 15:00 | XX | XX | XX | XX |\n| 16:00 | XX | XX | XX | XX |\n| 17:00 | XX | XX | XX | XX |\n| 18:00 | XX | XX | XX | XX |\n| 19:00 | XX | XX | XX | XX |\n| 20:00 | XX | XX | XX | XX |\n| 21:00 | XX | XX | XX | XX |\n| 22:00 | XX | XX | XX | XX |\n| 23:00 | XX | XX | XX | XX |"}

## 🎒 出行提示（当天）
- 穿衣建议：XX
- 出行建议：XX
- 安全提醒：XX

## 🚨 天气预警
> 如当天存在极端天气风险，请在此详细说明

---

**预测日期**: {target_date}  
**更新时间**: 实时更新  
**数据来源说明**: 以长白山气象站与以往开放记录为基础，参考 meteoblue 的展示风格（不直接抓取其实时数据）；请在必要处给出可信度或不确定性说明。

请确保：
1. 温度使用摄氏度  
2. 风力使用中文描述（如：微风、3-4级风等）  
3. 降水概率使用百分比  
4. 开放概率为百分比，三行分别给出北/西/南坡  
5. 内容专业、实用，逻辑自洽
        """

        resp = app_builder_client.run(conversation_id, weather_prompt)

        return {
            'prediction': resp.content.answer,
            'conversation_id': conversation_id
        }

    except Exception as e:
        raise Exception(f'天气预测失败: {str(e)}')


def validate_date(target_date):
    """
    验证单个日期是否有效（前后3个月范围内）

    Args:
        target_date (str): 预测日期

    Returns:
        tuple: (is_valid, error_message)
    """
    if not target_date:
        return False, '请提供预测日期'

    try:
        from datetime import datetime, timedelta
        date_obj = datetime.strptime(target_date, '%Y-%m-%d')

        today = datetime.now()
        min_date = today - timedelta(days=90)
        max_date = today + timedelta(days=90)

        if date_obj < min_date or date_obj > max_date:
            return False, '日期超出允许范围（前后3个月）'

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
        'description': '基于AI技术的长白山天池天气预测服务',
        'features': [
            '智能天气预测',
            '结构化Markdown展示',
            '旅游建议',
            '长白山特色天气分析'
        ],
        'supported_formats': ['Markdown'],
        'max_date_range': '前后3个月'
    }
