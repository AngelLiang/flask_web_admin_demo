# coding=utf-8

###############################################################################
HOST = "127.0.0.1"
PORT = 5000

###############################################################################
SECRET_KEY = "hard to guess string and longer than 32 byte!"

###############################################################################
# database
# SQLALCHEMY_DATABASE_URI =

# sqlite
# SQLALCHEMY_DATABASE_URI = sqlite:///data.sqlite


# mysql
# format 'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}?charset=utf8'
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/flask_app?charset=utf8"

################################################################################
