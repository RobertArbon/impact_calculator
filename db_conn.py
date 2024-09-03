"""
Manages connection to DB. 
Adpated from https://github.com/alan-navarro/street_team/blob/main/app_framework/db_connection/db_conn.py
"""
import psycopg2
import os
import config
config_env = getattr(config, os.getenv('APP_SETTINGS', 'DevelopmentConfig'))

class DbConn:

    def __init__(self):
        print("Initializing Connection class")

    def get_connection(self):
        host = config_env.HOST 
        db_name = config_env.DB_NAME
        user = config_env.USER
        password = config_env.PASSWORD
        port = config_env.PORT 

        conn = psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(host, port, db_name, user, password))

        uri = config_env.DATABASE_URL
        
        dict_conn = {"conn": conn, "DATABASE_URL": uri}
        
        return dict_conn
