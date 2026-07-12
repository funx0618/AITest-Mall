"""
项目配置文件
"""

# ========== 数据库配置 ==========
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "mall",
}

# ========== 后台管理（Admin）环境配置 ==========
ADMIN_BASE_URL = "http://localhost:8090"
ADMIN_LOGIN_URL = f"{ADMIN_BASE_URL}/#/login"

# ========== Web App（前台商城）环境配置 ==========
WEB_BASE_URL = "http://localhost:8060"
WEB_LOGIN_URL = f"{WEB_BASE_URL}/#/pages/public/login"

# ========== API 配置 ==========
ADMIN_API_BASE_URL = "http://localhost:8080"
APP_API_BASE_URL = "http://localhost:8085"

# ========== 兼容旧配置 ==========
BASE_URL = ADMIN_BASE_URL
LOGIN_URL = ADMIN_LOGIN_URL

# ========== 后台登录账号 ==========
DEFAULT_USERNAME = "funx"
DEFAULT_PASSWORD = "123456"

# ========== Web App 登录账号 ==========
WEB_USERNAME = "funxapp"
WEB_PASSWORD = "123456funx"
