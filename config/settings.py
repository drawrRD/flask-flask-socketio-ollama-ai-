class BaseSettings(object):
    # 邮箱配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '*********'
    MAIL_PASSWORD = '******'
    MAIL_DEFAULT_SENDER = '*********'

    # redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 0  # 数据库索引，默认为 0
    REDIS_URL = 'redis://localhost:6379/0'

    # 加密盐值
    SECRET_KEY = 'abcdefghijk'

#本机调试用
class TestSettings(BaseSettings):
    # 数据库配置
    PORT = 3306
    HOSTNAME = '127.0.0.1'
    USERNAME = 'root'
    PASSWORD = '*********'
    DATABASE = '*********'
    DBURI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
    SQLALCHEMY_DATABASE_URI = DBURI


# 生产环境配置
class ProSettings(BaseSettings):
    PORT = 3306
    HOSTNAME = '*********'
    USERNAME = '*********'
    PASSWORD = '*********'
    DATABASE = '*********'
    DBURI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
    SQLALCHEMY_DATABASE_URI = DBURI

