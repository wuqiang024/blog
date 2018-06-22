#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms impot StringField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class LoginForm(FlaskForm):
    # username = StringField('用户名',validators=[DataRequired(),Length(2,12)])
    email = StringField('邮箱',validators=[DataRequired(),Email(),Length(5,64)])
    password = StringField('密码',validators=[DataRequired(),Length(6,12)])