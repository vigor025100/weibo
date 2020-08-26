import os
from hashlib import md5,sha256
from flask import redirect



# 创建密码密钥
def make_password(password):
    '''产生一个安全密码'''
    if not isinstance(password,bytes): # 判断 password 是不是后面 bytes 类型
        password = str(password).encode('utf8')

    # 计算哈希值
    hash_value = sha256(password).hexdigest() # sha256 只能处理二进制对象。hexdigest()将bytes转成16进制
    # sha256(password) --> <sha256 HASH object @ 0x000001B7D76AA120> 是一个对象
    # hash_value --> 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92 是一串值

    # 产生随机盐进，长度 32 字节
    salt = os.urandom(16).hex()  # random 产生的是伪随机；urandom 产生的是真实随机。hexd()将bytes转成16进制

    # 使用随机盐进行加密处理
    safe_password = salt + hash_value
    return safe_password


# 比对检查密码
def check_password(password,safe_password):
    if not isinstance(password,bytes):
        password = str(password).encode('utf8')

    hash_value = sha256(password).hexdigest()
    return hash_value == safe_password[32:]


# 判断是否登录状态
def login_required(vew_func):  # 传的参数是我们需要被装饰的函数，这里我们装饰的是视图函数
    def check_session(*args,**kwargs): # 我们是通过获取session值来判断用户是否登录
        username = session['username'] # 因为我在登录的时候通过session 给服务器传的就是username值
        if not username:
            return redirect('/user/login') # 如果没有取到session 就重定向到登录页面
        else:
            return vew_func() # 取到session值，就正常执行查看个人详细信息的代码
    return check_session