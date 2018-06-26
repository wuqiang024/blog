#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField,ValidationError
from wtforms.validators import DataRequired,Length,Email,EqualTo
from ..models import User

class LoginForm(FlaskForm):
    # username = StringField('用户名',validators=[DataRequired(),Length(2,12)])
    email = StringField('邮箱',validators=[DataRequired(),Email(message=u'邮件格式不正确'),Length(6,64,message=u'邮件长度要在6和64位之间')])
    password = StringField('密码',validators=[DataRequired(),Length(6,12)])
    remember_me = BooleanField(label=u'记住密码',default=False)
    submit = SubmitField(u'登录')

class RegisterForm(FlaskForm):
    username = StringField(u'用户名',validators=[DataRequired(),Length(2,12)])
    email = StringField(u'邮箱',validators=[DataRequired(),Email()])
    password = PasswordField(u'密码',validators=[DataRequired(),EqualTo('password2')])
    password2 = PasswordField(u'密码',validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱地址已被注册')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被注册')
