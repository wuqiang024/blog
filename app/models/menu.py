#!usr/bin/env python
# -*- encoding:utf-8 -*-
from .. import db

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    types = db.relationship('ArticleType',backref='menu',lazy='dynamic')
    order = db.Column(db.Integer,default=0,nullable=False)

    def sort_delete(self):
        for menu in Menu.query.order_by(Menu.order).offset(self.order).all():
            menu.order -= 1
            db.session.add(menu)

    @staticmethod
    def insert_menu():
        menus = ['web开发','数据库','网络技术','爱生活，爱自己','Linux世界','开发语言']
        for name in menus:
            menu = Menu(name=name)
            db.session.add(menu)
            db.session.commit()
            menu.order = menu.id
            db.session.add(menu)
            db.session.commit()

    @staticmethod
    def return_menus():
        menus = [(m.id,m.name) for m in Menu.query.all()]
        menus.append((-1,u'不选择导航(该分类将单独成一导航'))
        return menus

    def __repr__(self):
        return '<Menu %r>'.format(self.name)