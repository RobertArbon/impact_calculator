import os
import rich

class Config(object): 
    DEBUG = True
    TESTING = False
    HOST = os.environ['HOST']
    USER = os.environ['USER']
    PASSWORD = os.getenv('PASSWORD', None)
    PORT = os.environ['PORT']
    TABLE_CONN = os.getenv('TABLE_CONN', None)
    DB_NAME = os.environ['DB_NAME']
    SQLALCHEMY_DATABASE_URI = f"postgresql://{HOST}:{PORT}/{DB_NAME}"

class DevelopmentConfig(Config):
    DEVELOPMENT=True
    APP_PORT = 8888


