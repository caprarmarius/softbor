import os
import pymysql
import database_login

connect_database = "mysql+pymysql://{0}:{1}@{2}/{3}".format(database_login.dbuser, database_login.dbpassword, database_login.dbhost, database_login.dbname)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'apa-de-ploaie'
    SESSION_TYPE = 'memcached'
    SQLALCHEMY_DATABASE_URI = connect_database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_SESSION_FOR_NEXT = True