#!usr/bin/env python
# -*- encoding:utf-8 -*-
from .. import db

class ArticleTypeSetting(db.Model):
    __tablename__ = 'articleTypeSettings'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    protected = db.Column(db.Boolean,default=False)
    hide = db.Column(db.Boolean,default=False)
    types = db.relationship('ArticleType',backref='setting',lazy='dynamic')

    @staticmethod
    def insert_system_setting():
        system = ArticleTypeSetting(name='system',protected=True,hide=True)
        db.session.add(system)
        db.session.commit()

    @staticmethod
    def insert_default_setting():
        system_setting = ArticleTypeSetting(name='system',protected=True,hide=True)
        common_setting = ArticleTypeSetting(name='common',protected=False,hide=False)
        db.session.add(system_setting)
        db.session.add(common_setting)
        db.session.commit()

    @staticmethod
    def return_setting_hide():
        return[(2,u'公开'),(1,u'隐藏')]

    def __repr__(self):
        return '<ArticleTypeSetting %r>' % self.name