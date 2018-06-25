#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_required,logout_user,login_user,current_user
from . import auth
from .. import admin
from .forms import LoginForm,RegisterForm
from ..models import User

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.strip(),
                    email=form.email.data.strip(),
                    password=form.password.data.strip())
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
    return render_template('auth/register.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.manager'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(u'登录成功!欢迎回来,%s' % user.username,'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash(u'登录失败！用户名或密码错误，请重新登录','danger')

    if form.errors:
        flash(u'登录失败，请尝试重新登录','danger')

    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'你已退出登录','success')
    return redirect(url_for('main.index'))