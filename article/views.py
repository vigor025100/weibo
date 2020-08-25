from flask import Blueprint
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from libs.orm import db
import datetime

from article.models import Article

article_bp = Blueprint('article',__name__,url_prefix='/article')
article_bp.template_folder='./templates'


@article_bp.route('/home')
def home(): # 微博主页
    articles = Article.query.all()
    return render_template('home.html',articles=articles)

@article_bp.route('/push',methods=('POST','GET'))
def push(): # 发微博
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        date = datetime.datetime.now()

        article = Article(title=title,content=content,date=date,author=author)
        db.session.add(article)
        db.session.commit()
        return redirect('/article/home')

    else:
        return render_template('push.html')

@article_bp.route('/read')
def read():
    id = request.args.get('id')
    article = Article.query.filter_by(id=id).one()
    return render_template('read.html',article=article)

@article_bp.route('/modif',methods=('POST','GET'))
def modif(): # 修改微博
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        date = datetime.datetime.now()

        article = Article(title=title, content=content, date=date, author=author)
        db.session.add(article)
        db.session.commit()
        return redirect('/article/home')

    else:
        id = request.args.get('id')
        article = Article.query.filter_by(id=id).oen()
        return render_template('modif.html',article=article)

@article_bp.route('/delete')
def delete(): # 删除微博
    id = request.args.get('id')
    Article.query.filter_by(id=id).delete()  # 直接删除了微博
    db.session.commit()
    return redirect('/article/home')
