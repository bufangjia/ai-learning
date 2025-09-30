from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import appbuilder
import os
import uuid
from config import Config
from weather import get_weather_prediction, validate_date_range

app = Flask(__name__)
CORS(app)

# 设置环境中的TOKEN
os.environ["APPBUILDER_TOKEN"] = Config.APPBUILDER_TOKEN

# 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID
app_id = Config.APP_ID

# 存储对话的字典，key为conversation_id
conversations = {}

@app.route('/')
def index():
    """返回聊天页面"""
    return render_template('index.html')

@app.route('/weather')
def weather():
    """返回天气预测页面"""
    return render_template('weather.html')

@app.route('/test-date')
def test_date():
    """返回日期测试页面"""
    with open('test_simple_date.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        conversation_id = data.get('conversation_id')
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 如果没有conversation_id，创建新的对话
        if not conversation_id:
            app_builder_client = appbuilder.AppBuilderClient(app_id)
            conversation_id = app_builder_client.create_conversation()
            conversations[conversation_id] = app_builder_client
        
        # 获取对应的客户端
        client = conversations.get(conversation_id)
        if not client:
            app_builder_client = appbuilder.AppBuilderClient(app_id)
            conversation_id = app_builder_client.create_conversation()
            conversations[conversation_id] = app_builder_client
            client = app_builder_client
        
        # 调用百度AI接口
        resp = client.run(conversation_id, message)
        
        return jsonify({
            'response': resp.content.answer,
            'conversation_id': conversation_id
        })
        
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/api/new_conversation', methods=['POST'])
def new_conversation():
    """创建新的对话"""
    try:
        app_builder_client = appbuilder.AppBuilderClient(app_id)
        conversation_id = app_builder_client.create_conversation()
        conversations[conversation_id] = app_builder_client
        
        return jsonify({
            'conversation_id': conversation_id,
            'message': '新对话已创建'
        })
        
    except Exception as e:
        return jsonify({'error': f'创建对话失败: {str(e)}'}), 500

@app.route('/api/weather-predict', methods=['POST'])
def weather_predict():
    """处理天气预测请求"""
    try:
        data = request.get_json()
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')
        
        # 验证日期范围
        is_valid, error_message = validate_date_range(start_date, end_date)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # 调用天气预测模块
        result = get_weather_prediction(start_date, end_date)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'天气预测失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
