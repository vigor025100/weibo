# 对 main 进行配置
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from libs.orm import db

# 定义 app 对象
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://vigoryu:123456@119.45.191.60:3306/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True # 每次结束请求后，都会自动提交数据库的变动
db.init_app(app)

# 绑定命令
manger = Manager(app)

# 初始化 db 迁移工具
migrate = Migrate(app,db)
manger.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manger.run()
