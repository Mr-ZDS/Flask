import os
import pymysql

DEBUG = True

SECRET_KEY = os.urandom(24)

# 'mysql+pymysql://用户名称:密码@localhost:端口/数据库名称'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost:3306/Library'
SQLALCHEMY_TRACK_MODIFICATIONS = True
