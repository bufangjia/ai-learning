# 安装说明：
# 执行如下命令，快速安装Python语言的最新版本AppBuilder-SDK（要求Python >= 3.9)：
# pip install --upgrade appbuilder-sdk
import appbuilder
import os

# 设置环境中的TOKEN，以下TOKEN请替换为您的个人TOKEN，个人TOKEN可通过该页面【获取鉴权参数】或控制台页【密钥管理】处获取
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-9K0kktgQ0XM4SHE2mvpnJ/d44f6c9d28e99b9dd5b5e972f08d4e914f7a1edd"

# 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID
app_id = "47557e8c-f26f-4bf2-89ce-0d34d6a90e97"

app_builder_client = appbuilder.AppBuilderClient(app_id)
conversation_id = app_builder_client.create_conversation()

resp = app_builder_client.run(conversation_id, "你好，你能做什么？")
print(resp.content.answer)