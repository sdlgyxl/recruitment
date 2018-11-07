import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_DATABASE_URI = "mssql+pymssql://rtx:C814794AACE44A4B@115.182.7.247/ExampleDb"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:JinMao80&@115.182.7.247/cleanblog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp@126.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'sdlgyxl'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Yang#xl$1973'
    ADMINS = ['2290497836@qq.com']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or '115.182.7.247'
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    POSTS_PER_PAGE = 5