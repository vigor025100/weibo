import datetime
from flask import Blueprint
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from libs.orm import db

from article.models import Article
from libs.utils import login_required

article_bp = Blueprint('article',__name__,url_prefix='/article')
article_bp.template_folder='./templates'


@article_bp.route('/home')
def home(): # 微博主页
    # articles = Article.query.all().order_by('date')
    # return render_template('home.html',articles=articles)
    articles = Article.query.all()
    arts = []
    for art in articles: # 遍历是按顺序遍历的
        arts.append(art)
    arts_new = arts[::-1]  # 列表的切片，使其倒序
    return render_template('home.html',arts_new=arts_new)

@article_bp.route('/push',methods=('POST','GET'))
@login_required
def push(): # 发微博
    if request.method == 'POST':
        content = request.form.get('content','').strip()
        uid = session.get('id')  # 用户发微博的时候必须是登录的状态，所以写的那个登录检查装饰器又排上用场了
        now = datetime.datetime.now()

        # 检查微博的内容是否为空
        if not content:
            return render_template('push.html',err='微博内容不允许为空')

        article = Article(uid=uid,content=content,created=now,updated=now)
        db.session.add(article)
        db.session.commit()

        return redirect(f'/article/read?wid={article.id}') # 直接跳转到刚刚发布的那条微博
    else:
        return render_template('push.html')

@article_bp.route('/read')
def read():
    id = request.args.get('wid')
    article = Article.query.filter_by(id=id).one()
    return render_template('read.html',article=article)

@article_bp.route('/modif',methods=('POST','GET'))
def modif(): # 修改微博
    if request.method == 'POST':
        id = request.form.get('id')
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        date = datetime.datetime.now()

        article = Article(title=title, content=content, date=date, author=author)
        db.session.add(article)
        Article.query.filter_by(id=id).delete()   # 删除原本的微博
        db.session.commit()
        return redirect('/article/home')

    else:
        id = request.args.get('id')
        article = Article.query.filter_by(id=id).one()
        return render_template('modif.html',article=article)

@article_bp.route('/delete')
def delete(): # 删除微博
    id = request.args.get('id')
    Article.query.filter_by(id=id).delete()  # 直接删除了微博
    db.session.commit()
    return redirect('/article/home')
