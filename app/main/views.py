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


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@main.route('/ckupload/', methods=['POST'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    res = """

<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>
""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response