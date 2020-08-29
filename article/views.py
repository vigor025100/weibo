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
from article.models import Thumb
from user.models import Follow
from libs.utils import login_required
from sqlalchemy.exc import IntegrityError

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
    session['page'] = page

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
    id = request.args.get('wid') # 微博的id
    fid = request.args.get('fid')
    article = Article.query.filter_by(id=id).one()

    # 根据 wid 取出相应的评论
    comments = Comment.query.filter_by(wid=id).order_by(Comment.created.desc())

    uid = session.get('id')  # 取当前登录用户的id
    page = session.get('page',1)  # 得到这条微博在home的第几页
    # 判断是否点赞
    if uid : # 如果取到了uid
        if Thumb.query.filter_by(uid=uid, wid=id).count():
            is_liked=True
        else:
            is_liked=False
    else:
        is_liked=False

    return render_template('read.html',article=article, comments=comments, is_liked=is_liked, page=page)

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

@article_bp.route('/delete_comment')
def delete_comment():
    '''删除评论'''
    # 在 read.html 页面已经做了判断，不是本人登录的情况下，微博的删除和修改按钮不展示
    # 这个删除指令是从前端浏览上传过来，是一个请求，我们在服务器上去接收
    id = int(request.args.get('id'))
    wid = int(request.args.get('wid'))
    comment = Comment.query.get(id)
    # 修改数据
    comment.content = '该条评论已删除'
    # 提交数据
    db.session.commit()

    return redirect(f'/article/read?wid={wid}')


@article_bp.route('/like')
@login_required
def like():
    '''点赞'''
    uid = session['id']  # 只要我登录了就能取到，session 括号里面填什么，那要看你在 login 环节推送的时候是怎么命名的了
    wid = request.args.get('wid') # 这里我们就是需要这个数据，那么在写页面的时候就要注意要把这个数据传给服务器

    thumb = Thumb(uid=uid, wid=wid)
    try: # 没有错误的情况下会执行的语句
        db.session.add(thumb)
        Article.query.filter_by(id=wid).update({'n_thumb':Article.n_thumb + 1 }) # 点赞的数量+1
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        Article.query.filter_by(id=wid).update({'n_thumb': Article.n_thumb - 1})  # 点赞的数量-1
        Thumb.query.filter_by(uid=uid, wid=wid).delete()
        db.session.commit()

    return redirect(f'/article/read?wid={wid}')
    # 几乎每天都写这句，这是个啥有没有仔细思考过啊？
# redirect()重定向函数，在这里重定向之前是read页面，重定向还是到read页面，为什么要这么做？
# 重定向：在客户端提交请求以后，本来是访问的A页面，结果，后台给了B页面，因为B页面才是我在客服端提交请求后需要的信息
# 在这里重定向以后还是read页面，只是有执行了一次read视图函数以后才得以展示的read页面
# 为什么重定向是要再执行一次read视图函数，那么read视图函数，以及我们写这些视图函数又是为了干啥的
# 在每个视图函数的最后，不是redirect()重定向函数，就是render_template()函数，后者是为了展示页面
# 为什么要展示页面，页面是为了展示我们想要展示的信息，那我们想要展示的信息从哪里来，视图函数就是处理的过程，把我们想要的信息处理好，传给前端页面
# 视图函数里面写的是一系列处理我们想要的信息的逻辑，虽然我们重定向的到的页面还是我们想要的页面，但是我们既然在客户端提交了请求以后
# 还想得到这个页面，那么肯定是我们想在这个页面的上信息有所变化，这样就是要再走一遍视图函数里的每一行代码，传到页面的信息也会更新
# 页面的上信息的展示必须要有有这个也免得视图函数进行处理，传给页面才能进行展示
# 下面一个就要解决当用户给某一条微博点赞以后，点赞要变成取消点赞

