#!usr/bin/env python
# -*- encoding:utf-8 -*-
from .. import db
from .articleTypeSetting import ArticleTypeSetting

class ArticleType(db.Model):
    __tablename__ = 'articleTypes'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    introduction = db.Column(db.Text,default=None)
    articles = db.relationship('Article',backref='articleType',lazy='dynamic')
    menu_id = db.Column(db.Integer,db.ForeignKey('menus.id'),default=None)
    setting_id = db.Column(db.Integer,db.ForeignKey('articleTypeSettings.id'))

    @staticmethod
    def insert_system_articleType():
        articleType = ArticleType(name=u'未分类',
                                  introduction=u'系统默认分类，不可删除',
                                  setting=ArticleTypeSetting.query.filter_by(protected=True).first())
        db.session.add(articleType)
        db.session.commit()

    @staticmethod
    def insert_articleType():
        articleTypes = ['Python','Javascript','Flask','MySQL','Redis','MongoDB','Node',u'Linux运维实战',
                        u'生活那些事',u'其他']
        for name in articleTypes:
            articleType = ArticleType(name=name,
                                       setting=ArticleTypeSetting(name=name))
            db.session.add(articleType)

            db.session.commit()

