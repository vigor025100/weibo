import datetime

from math import ceil
from flask import Blueprint
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from libs.orm import db

from article.models import Article
from article.models import Comment
from libs.utils import login_required

article_bp = Blueprint('article',__name__,url_prefix='/article')
article_bp.template_folder='./templates'


@article_bp.route('/home')
def home():
    '''微博首页'''
    page = int(request.args.get('page',1))
    per_page = 6 # 每页数量
    offset_page = per_page * (page-1) # 跳过前多少页

    max_page = ceil(Article.query.count()/per_page)

    # 需要在底部展示7个页码
    if page <= 3:
        start,end = 1,min(7,max_page)
    elif page > (max_page-3) :
        start,end =(max_page-6),max_page
    else:
        start,end = (page-3),(page+3)
    pages = range(start,end+1)

    articles=Article.query.order_by(Article.updated.desc()).limit(per_page).offset(offset_page)
    return render_template('home.html', articles=articles,pages=pages,page=page)

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

    # 根据 wid 取出相应的评论
    comments = Comment.query.filter_by(wid=id).order_by(Comment.created.desc())

    return render_template('read.html',article=article, comments=comments)

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


@article_bp.route('/push_comment', methods=('POST',))
@login_required
def push_comment():
    '''发表评论'''
    uid = session['id']
    wid = request.form.get('wid')
    content = request.form.get('content')
    now = datetime.datetime.now()

    comment = Comment(uid=uid, wid=wid, content=content, created=now)
    db.session.add(comment)
    db.session.commit()

    return redirect(f'/article/read?wid={wid}')

@article_bp.route('/reply', methods=('POST',))
@login_required
def reply():
    '''回复评论'''
    uid = session['id']
    wid = request.form.get('wid')
    cid = request.form.get('cid') # 这里为啥会有 cid 因为我们是对别人的评论进行了回复，所以才会有啊，那通过这个 cid 是不是也可以找到 这条评论的作者呀
    content = request.form.get('content')
    now = datetime.datetime.now()

    comment = Comment(uid=uid, wid=wid, cid=cid, content=content, created=now)
    db.session.add(comment)
    db.session.commit()

    return redirect(f'/article/read?wid={wid}')