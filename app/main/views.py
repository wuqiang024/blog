#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask import render_template,request,current_app
from ..models import Article
from . import main

@main.route('/index')
def index():
    page = request.args.get('page', 1,type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(
        page,10,error_out=False
    )
    articles = pagination.items
    return render_template('index.html',articles=articles,pagination=pagination,endpoint='.index')
