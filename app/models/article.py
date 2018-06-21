#!usr/bin/env python
# -*- encoding:utf-8 -*-
from datetime import datetime
from .. import db

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64),unique=True)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    create_time = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    update_time = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    num_of_view = db.Column(db.Integer,default=0)
    articleType_id = db.Column(db.Integer,db.ForeignKey('articleTypes.id'))
    source_id = db.Column(db.Integer,db.ForeignKey('sources.id'))
    comments = db.relationship('Comment',backref='article',lazy='dynamic')

    @staticmethod
