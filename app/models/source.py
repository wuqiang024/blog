#!usr/bin/env python
# -*- encoding:utf-8 -*-
from .. import db

class Source(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    articles = db.relationship('Article',backref='source',lazy='dynamic')

    @staticmethod
    def insert_source():
        sources = (u'原创',u'转载',u'翻译')
        for s in sources:
            source = Source.query.filter_by(name=s).first()
            if source is None:
                source = Source(name=s)
            db.session.add(source)
            db.session.commit()

    def __repr__(self):
        return '<Source %人>' % self.name