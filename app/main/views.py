#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask import render_template,request,current_app
from flask_login import current_user
from ..models import Article,ArticleType,Source
from . import main
from .. import db

@main.route('/index')
def index():
    page = request.args.get('page', 1,type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(
        page,10,error_out=False
    )
    articles = pagination.items
    return render_template('index.html',articles=articles,pagination=pagination,endpoint='.index')

@main.route('/article-types/<int:id>/')
def articleTypes(id):
    page = request.args.get('page',1,type=int)
    pagination = ArticleType.query.get_or_404(id).articles.order_by(Article.create_time.desc()).paginate(
        page,10,error_out=False
    )
    articles = pagination.items
    return render_template('index.html',articles=articles,pagination=pagination,endpoint='.articleTypes',id=id)

@main.route('/article-details/<int:id>',methods=['GET','POST'])
def articleDetails(id):
    article = Article.query.get_or_404(id)
    # article.add_view(article,db)
    return render_template('article_details.html',article=article,id=article.id,endpoint='.articleDetails')
    return 'test'

@main.route('/article-sources/<int:id>')
def articleSources(id):
    page = request.args.get('page',1,type=int)
    pagination = Source.query.get_or_404(id).articles.order_by(
        Article.create_time.desc()).paginate(page,10,error_out=False)
    articles = pagination.items
    return render_template(
        'index.html',
        articles=articles,
        pagination=pagination,
        endpoint='.articleSources',
        id=id)