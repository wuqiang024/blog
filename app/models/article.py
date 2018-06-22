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
    def add_view(article,db):
        article.num_of_view += 1
        db.session.add(article)
        db.session.commit()

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed,randint
        import forgery_py

        seed()
        articleType_count = ArticleType.query.count()
        source_count = Source.query.count()
        for i in range(count):
            aT = ArticleType.query.offset(randint(0,articleType_count-1)).first()
            s = Source.query.offset(randint(0,source_count-1)).first()
            a = Article(title=forgery_py.lorem_ipsum.title(randint(3,5)),
                        content=forgery_py.lorem_ipsum.sentence(randint(15,35)),
                        summary=forgery_py.lorem_ipsum.sentence(randint(2,5)),
                        num_of_view=randint(100,15000),
                        articleType=aT,sourceo=s)
            db.session.add(a)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Article %r>' % self.title
