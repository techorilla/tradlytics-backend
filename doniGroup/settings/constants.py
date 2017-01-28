from .environment import *

SESSION_COOKIE_AGE = 60*60*2

if ENV == 'DEV':
    MYSQL_ENGINE = 'django.db.backends.mysql'
    MYSQL_HOST = '127.0.0.1'
    MYSQL_DB = 'doniGroup'
    MYSQL_PORT = '3306'
    MYSQL_USER = 'doniGroup'
    MYSQL_PASSWORD = 'Giki1990????'
    REDIS_HOST = ''
