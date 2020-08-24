from flask import Blueprint
from flask import redirect
from flask import request
from flask import render_template
from flask import session

from user.models import User  #  这个在 models 模块还未写

user_bp = Blueprint('user',__name__,url_prefix='/user') # 定义一个蓝图实例对象
usre_bp.template_folder='./templates'  # 当前蓝图模板文件存放的位置

@user_bp.route('/register',methods=('POST','GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        city = request.form.get('city')
        address = request.form.get('address')
        phone = request.form.get('phone')

        user = User(username=username,password=password,gender=gender,city=city,address=address,phone=phone)
        db.session.add(user) # 往表内插入数据
        db.session.commit() # 提交数据

        return redirect('/user/login')  # 注册好了就要到登录页面呀

    else:
        return render_template('register.html')

@user_bp.route('/login',methods=('POST','GET'))
def login():
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        # 判断用户名是否正确
        try:
            user=User.query.filter_by(username=username).one()
        except Exception: # 如果是个不存在的用户名，那么取数据的时候肯定会报错的
            db.session.rollback
            return render_template('eu.html')
        # 判断密码是否正确
        if password and user.password == password:
            # 要携带用户信息给到浏览器
            session['username']=user.username  # 这里直接写 username 也是可以的，是从表格里获取的
            return redirect('/user/info')
        else:
            return render_template('ep.html')
    else:
        return render_template('login.html')

@user_bp.route('/info')
def info():
    return render_template('info.html')

@user_bp.route('/logout')
def logout():
    return redirect('/user/login')