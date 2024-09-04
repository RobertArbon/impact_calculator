import os
import rich

class Config(object): 
    DEBUG = True
    TESTING = False
    HOST = os.getenv('HOST')
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD', None)
    PORT = os.getenv('PORT')
    TABLE_CONN = os.getenv('TABLE_CONN', None)
    DB_NAME = os.getenv('DB_NAME')
    DATABASE_URL = f"postgresql://{HOST}:{PORT}/{DB_NAME}"

class DevelopmentConfig(Config):
    DEVELOPMENT=True
    APP_PORT = 8888

class ProductionConfig(Config):
    DEVELOPMENT = False
    DATABASE_URL = os.getenv('DATABASE_URL')



