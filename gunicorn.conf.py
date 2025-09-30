# Gunicorn配置文件
bind = "127.0.0.1:3000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
accesslog = "/www/wwwroot/your-domain.com/logs/access.log"
errorlog = "/www/wwwroot/your-domain.com/logs/error.log"
loglevel = "info"
