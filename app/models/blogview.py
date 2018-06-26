#!usr/bin/env python
# -*- encoding:utf-8 -*-
from .. import db

class BlogView(db.Model):
    __tablename__ = 'blog_view'
    id = db.column(db.Integer,primary_key=True)
    num_of_view = db.Column(db.BigInteger,default=0)

    @staticmethod
    def insert_view():
        view = BlogView(num_of_view=0)
        db.session.add(view)
        db.session.commit()

    @staticmethod
    def add_view(db):
        view = BlogView.query.first()
        view.num_of_view += 1
        db.session.add(view)
        db.session.commit()