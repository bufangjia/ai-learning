# 生产环境配置
import os

class Config:
    # 百度AI配置
    APPBUILDER_TOKEN = os.environ.get('APPBUILDER_TOKEN', 'bce-v3/ALTAK-9K0kktgQ0XM4SHE2mvpnJ/d44f6c9d28e99b9dd5b5e972f08d4e914f7a1edd')
    APP_ID = os.environ.get('APP_ID', '47557e8c-f26f-4bf2-89ce-0d34d6a90e97')
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    DEBUG = False
    
    # 服务器配置
    HOST = '0.0.0.0'
    PORT = 3000

    # 可选：meteoblue 配置（无则回退到AI推理）
    METEOBLUE_API_KEY = os.environ.get('METEOBLUE_API_KEY')
    METEOBLUE_LAT = os.environ.get('METEOBLUE_LAT', '42.006')  # 长白山附近
    METEOBLUE_LON = os.environ.get('METEOBLUE_LON', '128.067')
    METEOBLUE_ENDPOINT = os.environ.get('METEOBLUE_ENDPOINT', 'https://my.meteoblue.com/packages/basic-1h_basic-day')
