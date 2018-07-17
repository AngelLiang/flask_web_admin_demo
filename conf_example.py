#coding=utf-8

SECRET_KEY = "hard to guess string and longer than 32 byte!"

###############################################################################
### database 
# SQLALCHEMY_DATABASE_URI = 

### sqlite
# SQLALCHEMY_DATABASE_URI = sqlite:///data.sqlite

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB_NAME = "flask_app"


################################################################################
### mysql
# format 'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}?charset=utf8'
SQLALCHEMY_DATABASE_URI =\
    "mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}".format(
    username = MYSQL_USERNAME,
    password = MYSQL_PASSWORD,
    host = MYSQL_HOST,
    port = MYSQL_PORT,
    dbname = MYSQL_DB_NAME,
)

