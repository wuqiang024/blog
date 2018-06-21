#!usr/bin/env python
# -*- encoding:utf-8 -*-

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:810805@localhost:3306/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'blog'

