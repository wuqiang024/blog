#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask import render_template,url_for,redirect,request,current_app,jsonify,flash
from flask_login import login_required,current_user
from . import admin
from .forms import SubmitArticlesForm
from ..models import Article,Source,ArticleType
from .. import db

@admin.route('/')
@admin.route('/index')
@login_required
def manager():
    # return redirect(url_for('admin.custom_blog_info'))
    return redirect(url_for('admin.submitArticles'))

@admin.route('/submit-articles',methods=['GET','POST'])
@login_required
def submitArticles():
    form = SubmitArticlesForm()
    sources = [(s.id,s.name) for s in Source.query.all()]
    form.source.choices = sources
    types = [(t.id,t.name) for t in ArticleType.query.all()]
    form.types.choices = types

    if form.validate_on_submit():
        title = form.title.data
        source_id = form.source.data
        content = form.content.data
        type_id = form.types.data
        summary = form.summary.data

        source = Source.query.get(source_id)
        articleType = ArticleType.query.get(type_id)

        print('success1')

        if source and articleType:
            article = Article(title=title,content=content,summary=summary,source=source,articleType=articleType)
            db.session.add(article)
            db.session.commit()
            flash(u'博文发布成功','success')
            article_id = Article.query.filter_by(title=title).first().id
            return redirect(url_for('main.articleDetails',id=article_id))
            print('success2')
    else:
        print(form.errors)
        flash(u'发表博文失败','danger')

    return render_template('admin/submit_articles.html',form=form)

@admin.route('/edit-articles/<int:id>',methods=['GET','POST'])
@login_required
def editArticles(id):
    article = Article.query.get_or_404(id)
    form = SubmitArticlesForm()
    sources = [(s.id,s.name) for s in Source.query.all()]
    form.source.choices = sources
    types = [(t.id,t.name) for t in ArticleType.query.all()]
    form.types.choices = types

    if form.validate_on_submit():
        articleType = ArticleType.query.get_or_404(int(form.types.data))
        article.articleType = articleType
        source = Source.query.get_or_404(int(form.source.data))
        article.source = source
        article.title = form.title.data
        article.content = form.content.data
        article.summary = form.summary.data
        article.update_time = datetime.utcnow()
        db.session.add(article)
        db.session.commit()
        flash(u'博文更新成功','success')
        return redirect(url_for('main.articleDetails',id=article.id))
    form.source.data = article.source_id
    form.title.data = article.title
    form.content.data = article.content
    form.types.data = article.articleType_id
    form.summary.data = article.summary
    return render_template('admin/submit_articles.html',form=form)


@admin.route('/manager-articleTypes/nav',methods=['GET','POST'])
@login_required
def manage_articleTypes_nav():
    form = AddArticleTypeNavForm()
    form2 = EditArticleNavTypeForm()
    form3 = SortArticleNavTypeForm()

    page = request.args.get('page',1,type=int)
    if form.validate_on_submit():
        name = form.name.data
        menu = Menu.query.filter_by(name=name).first()
        if menu:
            page = page
            flash(u'添加导航失败！该导航名已经存在','danger')
        else:
            menu_count = Menu.query.count()
            menu = Menu(name=name,order=menu_count+1)
            db.session.add(menu)
            db.session.commit()
            page = -1
            flash(u'添加导航成功!','success')
            return redirect(url_for('admin.manage_articleTypes_nav',page=page))

    if page == -1:
        page = (Menu.query.count()-1)//current_app.config['PER_PAGE'] + 1

    pagination = Menu.query.order_by(Menu.order.asc()).paginate(
        page,
        per_page=current_app.config['PER_PAGE'],
        error_out=False)
    menus = pagination.items
    return render_template('admin/manage_articleTypes_nav.html',menus=menus,
                           pagination=pagination,endpoint='.manage_articleTypes_nav',
                           page=page,form=form,form2=form2,form3=form3)