#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class SubmitArticlesForm(FlaskForm):
    title = StringField(u'标题',validators=[DataRequired(),Length(1,64)])
    content = TextAreaField(u'博文内容',validators=[DataRequired()])
    summary = TextAreaField(u'博文摘要',validators=[DataRequired()])
    source = SelectField(u'来源',coerce=int,validators=[DataRequired()])
    types = SelectField(u'类型',coerce=int,validators=[DataRequired()])

class AddArticleTypeForm(FlaskForm):
    articleType_id = StringField(validators=[DataRequired()])

class AddArticleTypeNavForm(FlaskForm):
    name = StringField(u'导航名称',validators=[DataRequired()])