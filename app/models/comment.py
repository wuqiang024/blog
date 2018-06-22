#!usr/bin/env python
# -*- encoding:utf-8 -*-
from .. import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    author_name = db.Column(db.String(64))
    author_email = db.Column(db.String(64))
    article_id = db.Column(db.Integer,db.ForeignKey('articles.id'))
    disabled = db.Column(db.Boolean,default=False)
    comment_type = db.Column(db.String(64),default='comment')
    replyTo = db.Column(db.String(128),default='noReply')