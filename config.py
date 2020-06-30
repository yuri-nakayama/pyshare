#config.py holds the credentials of the database and used to connect to .env file
import os
from os.path import join,dirname
from dotenv import load_dotenv

dot_env = join(dirname(__file__),'.env') # this is for finding the .env file

class DevelopmentConfig():
    # DEBUG = True
    DEBUG = False
    
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/pyshare?charset=utf8'.format(**{
    #     'user':os.environ.get('MYSQL_USER','root'),
    #     'password':os.environ.get('MYSQL_PASSWORD','root'), #root
    #     'host':os.environ.get('DB_HOST','db:3306'), #localhost:8888
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bc95752d80a241:203e79b0@us-cdbr-east-02.cleardb.com/heroku_516b2e90deb450f?reconnect=true'.format(**{
        'user':os.environ.get('MYSQL_USER','root'),
        'password':os.environ.get('MYSQL_PASSWORD','root'), #root
        'host':os.environ.get('DB_HOST','db:3306'), #localhost:8888

    })

    SQLALCHEMY_TRACK_MODIFICATIONS = False #our lucky charm
    SQLALCHEMY_ECHO = False

Config = DevelopmentConfig #creating an object for DevelopmentConfig class

