from flask import Blueprint
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from libs.orm import db
from libs.utils import make_password
from libs.utils import check_password
from libs.utils import login_required
from sqlalchemy.exc import IntegrityError

from user.models import User

user_bp = Blueprint('user',__name__,url_prefix='/user') # 定义一个蓝图实例对象，user 为当前蓝图本身的名称
user_bp.template_folder='./templates'  # 当前蓝图模板文件存放的位置

# 注册
@user_bp.route('/register',methods=('POST','GET'))
def register():
    # 新用户注册信息提交
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password1 = request.form.get('password1','').strip()
        password2 = request.form.get('password2', '').strip()
        gender = request.form.get('gender','').strip()
        city = request.form.get('city','').strip()
        address = request.form.get('address','').strip()
        phone = request.form.get('phone','').strip()
        birthday = request.form.get('birthday','').strip()

        # 验证两次输入的密码是否一致
        if not password1 or password1 != password2 :
            return render_template('register.html',err='两次输入密码不相符')

        user = User(username=username,password=make_password(password1),gender=gender,city=city,address=address,phone=phone,birthday=birthday)
        # username 设置了唯一的属性，当用户名重复的时候，注册信息添加到数据库会报错
        try:
            db.session.add(user) # 用户信息写入数据库
            db.session.commit() # 提交数据
            return redirect('/user/login')
        except IntegrityError:
            db.session.rollback
            return render_template('register.html',err='用户名已被占用')

    # 拉起注册页面
    else:
        return render_template('register.html')

# 登录
@user_bp.route('/login',methods=('POST','GET'))
def login():
    # 登录信息提交
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')


        # 判断用户名
        try:
            user=User.query.filter_by(username=username).one()
        except Exception: # 如果是个不存在的用户名，那么取数据的时候肯定会报错的
            db.session.rollback
            return render_template('eu.html')

        # 判断密码
        if check_password(password,user.password):
            # 在 Session 中记录用户的登录状态
            session['username']=user.username
            session['id']=user.id
            return redirect('/user/info')
        else:
            return render_template('ep.html')
     # 登录页面拉起
    else:
        return render_template('login.html')

# 用户信息详情
@user_bp.route('/info')
@login_required # 增加了装饰器，判断用户是否登录
def info():
    username = session.get('username') # response 给浏览器返回的 session['username']
    user = User.query.filter_by(username=username).one()
    return render_template('info.html',user=user)

# 用户退出登录
@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/user/login')