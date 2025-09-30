from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import appbuilder
import os
import uuid

app = Flask(__name__)
CORS(app)

# 设置环境中的TOKEN
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-9K0kktgQ0XM4SHE2mvpnJ/d44f6c9d28e99b9dd5b5e972f08d4e914f7a1edd"

# 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID
app_id = "47557e8c-f26f-4bf2-89ce-0d34d6a90e97"

# 存储对话的字典，key为conversation_id
conversations = {}

@app.route('/')
def index():
    """返回聊天页面"""
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
