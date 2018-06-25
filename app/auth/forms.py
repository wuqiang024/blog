#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class LoginForm(FlaskForm):
    # username = StringField('用户名',validators=[DataRequired(),Length(2,12)])
    email = StringField('邮箱',validators=[DataRequired(),Email(message=u'邮件格式不正确'),Length(6,64,message=u'邮件长度要在6和64位之间')])
    password = StringField('密码',validators=[DataRequired(),Length(6,12)])
    remember_me = BooleanField(label=u'记住密码',default=False)
    submit = SubmitField(u'登录')