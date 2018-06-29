#!usr/bin/env python
# -*- encoding:utf-8 -*-

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:810805@localhost:3306/blog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SECRET_KEY = 'blog'
    PER_PAGE = 10

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    FLASK_MAIL_SUBJECT_PREFIX = 'subject:'
    MAIL_USERNAME = '253071452@qq.com'
    MAIL_PASSWORD = 'zxmegzggvfvnbggh'
    FLASK_MAIL_SENDER = 'wuqiang<253071452@qq.com>'

