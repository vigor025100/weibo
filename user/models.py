import random
from libs.orm import db
from libs.utils import random_zh_str
from libs.utils import make_num

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(128))
    gender = db.Column(db.Enum('男','女','保密'))
    birthday = db.Column(db.DateTime)
    city = db.Column(db.String(10))
    address = db.Column(db.String(64))
    phone = db.Column(db.String(16))

    # 为什么要在这里创建 创造用户的函数  我现在还不是很清楚呢，但创建的是一个类方法
    @classmethod
    def fake_users(cls,num):
        users=[]
        # 下面就要开始创建用户信息了，创建多少个我们用for循环来控制
        for i in range(num):
            year = random.randint(1980,2002)
            month = random.randint(1,12)
            day = random.randint(1,28)

            username = random_zh_str(3)
            password = '123'
            gender = random.choice(['男','女','保密'])
            birthday ='%04d-%02d-%02d' % (year, month,day)
            city = random.choice(['上海','北京','广州','深圳','池州','安庆','马鞍山'])
            address = random_zh_str(6)
            #phone = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6)
            phone = make_num()

            user = cls(username=username,password=password,gender=gender,birthday=birthday,city=city,address=address,phone=phone)
            users.append(user)

        # 执行添加数据
        db.session.add_all(users)
        db.session.commit()
        return users


