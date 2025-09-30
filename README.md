# AI助手聊天框项目

这是一个基于Flask和百度AI的聊天助手项目，提供美观的Web界面与AI进行对话。

## 功能特点

- 🎨 现代化的聊天界面设计
- 💬 支持连续对话（保持上下文）
- 🔄 支持创建新对话
- 📱 响应式设计，支持移动端
- ⚡ 实时消息发送和接收
- 🎯 集成百度AI大模型

## 项目结构

```
ai-learning/
├── app.py                 # Flask后端服务器
├── baidu_requset.py      # 百度AI接口（原有文件）
├── main.py               # 原有文件
├── requirements.txt      # Python依赖
├── templates/
│   └── index.html        # 前端聊天界面
└── README.md            # 项目说明
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行服务器

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问：http://localhost:3000

## 使用说明

1. **开始对话**：在输入框中输入问题，按回车或点击发送按钮
2. **新对话**：点击"新对话"按钮开始一个全新的对话
3. **连续对话**：AI会记住之前的对话内容，可以进行上下文相关的交流

## 技术栈

- **后端**：Flask + Flask-CORS
- **前端**：HTML + CSS + JavaScript
- **AI服务**：百度AppBuilder SDK
- **样式**：纯CSS，渐变背景，现代化设计

## 注意事项

- 确保您的百度AI Token有效
- 项目默认运行在3000端口
- 支持跨域请求，可以部署到不同域名

## 自定义配置

如需修改配置，请编辑 `app.py` 文件中的相关参数：

- `APPBUILDER_TOKEN`：您的百度AI Token
- `app_id`：您的应用ID
- 端口号：修改 `app.run()` 中的 `port` 参数
