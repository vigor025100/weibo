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
def home():
    '''微博首页'''
    articles=Article.query.order_by(Article.updated.desc()).all()
    return render_template('home.html', articles=articles)

@article_bp.route('/push',methods=('POST','GET'))
@login_required
def push():
    '''发微博'''
    if request.method == 'POST':
        content = request.form.get('content','').strip()
        uid = session.get('id')  # 用户发微博的时候必须是登录的状态，登录就会有用户的id,所以写的那个登录检查装饰器又排上用场了
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
    '''阅读微博'''
    id = request.args.get('wid')
    article = Article.query.filter_by(id=id).one()
    return render_template('read.html',article=article) # 我们传过去的是啥，是一个 article 实例

@article_bp.route('/modif',methods=('POST','GET'))
@login_required
def modif():
    '''修改微博'''
    if request.method == 'POST':
        wid = request.form.get('wid')
        content = request.form.get('content')
        updated = datetime.datetime.now()

        # 检查微博内容是否为空
        if not content :
            return render_template('modif.html',err='微博内容不允许为空')

        Article.query.filter_by(id=wid).update({'content':content,'updated':updated})
        db.session.commit()
        return redirect(f'/article/read?wid={wid}')

    else:
        wid = request.args.get('wid')
        article = Article.query.get(wid)
        return render_template('modif.html',article=article)

@article_bp.route('/delete')
@login_required
def delete(): # 删除微博
    wid = request.args.get('wid')
    article=Article.query.get(wid)
    id = session.get('id')
    if article.uid == id :
        db.session.delete(article)
        db.session.commit()
        return redirect('/article/home')
    else:
        return render_template('login.html', err='请登录')
