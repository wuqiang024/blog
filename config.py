#!usr/bin/env python
# -*- encoding:utf-8 -*-

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:810805@localhost:3306/blog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'blog'
    PER_PAGE = 10
    FLASK_EMAIL_SENDER: '253071452@qq.com'
    FLASK_EMAIL_PWD:'zxmegzggvfvnbggh'

