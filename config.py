#!usr/bin/env python
# -*- encoding:utf-8 -*-

class Config():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:810805'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'blog'