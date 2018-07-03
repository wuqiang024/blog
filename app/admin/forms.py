#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,TextAreaField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class AddArticleTypeForm(FlaskForm):
    name = StringField(u'分类名称', validators=[DataRequired(), Length(1, 64)])
    introduction = TextAreaField(u'分类介绍')
    setting_hide = SelectField(u'属性', coerce=int, validators=[DataRequired()])
    menus = SelectField(u'类型', coerce=int, validators=[DataRequired()])

class AddArticleNavTypeForm(FlaskForm):
    name = StringField(u'导航名称',validators=[DataRequired(),Length(1,64)])

class EditArticleNavTypeForm(AddArticleNavTypeForm):
    nav_id = StringField(validators=[DataRequired()])

class SortArticleNavTypeForm(AddArticleNavTypeForm):
    nav_id = StringField(validators=[DataRequired()])

class EditArticleTypeForm(AddArticleTypeForm):
    articleType_id = StringField(validators=[DataRequired()])

class SubmitArticlesForm(FlaskForm):
    title = StringField(u'标题',validators=[DataRequired(),Length(1,64)])
    content = TextAreaField(u'博文内容',validators=[DataRequired()])
    summary = TextAreaField(u'博文摘要',validators=[DataRequired()])
    source = SelectField(u'来源',coerce=int,validators=[DataRequired()])
    types = SelectField(u'类型',coerce=int,validators=[DataRequired()])

class AddArticleTypeNavForm(FlaskForm):
    name = StringField(u'导航名称',validators=[DataRequired()])

class ManageArticlesForm(FlaskForm):
    source = SelectField(u'来源',coerce=int,validators=[DataRequired()])
    types = SelectField(u'类型',coerce=int,validators=[DataRequired()])

class DeleteArticleForm(FlaskForm):
    articleId = StringField(validators=[DataRequired()])

class DeleteArticlesForm(FlaskForm):
    articleIds = StringField(validators=[DataRequired()])