from flask import Blueprint
from flask import redirect
from flask import render_template

from user.models import User  #  这个在 models 模块还未写

user_bp = Blueprint('user',__name__,url_prefix='/user') # 定义一个蓝图实例对象
usre_bp.template_folder='./templates'  # 当前蓝图模板文件存放的位置

@user_bp.route('/register')
def register():
    return render_template('register.html')

@user_bp.route('/login')
def login():
    return render_template('login.html')

@user_bp.route('/info')
def info():
    return render_template('info.html')

@user_bp.route('/logout')
def logout():
    return redirect('/user/login')