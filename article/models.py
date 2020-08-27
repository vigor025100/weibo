import random
from libs.orm import db
from user.models import User
from libs.utils import random_zh_str

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    content = db.Column(db.Text,nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)

    @property
    def author(self): # 我这定义的是啥 是个实例方法
        '''获取微博的作者'''
        return User.query.get(self.uid) # 谁调用 self 就指谁
        # 返回的是一个 Basequery 对象
    # 凭什么在这里可以去到用户名，因为微博在创建的时候写入了 作者的uid,我们用 实例.uid 可以获得用户的id
    # 再拿这个id 去用户的信息，进而能取到用户的名字

    @classmethod
    def fake_weibos(cls, uid_list, num):
        wb_list = []
        for i in range(num):
            year = random.randint(2010, 2019)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date = '%04d-%02d-%02d' % (year, month, day)

            uid = random.choice(uid_list)
            content = random_zh_str(random.randint(70, 140))
            wb = cls(uid=uid, content=content, created=date, updated=date)
            wb_list.append(wb)

        db.session.add_all(wb_list)
        db.session.commit()

class Comment(db.Model):
    '''创建评论表'''
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer,nullable=False, index=True)
    wid = db.Column(db.Integer, nullable=False, index=True)
    cid = db.Column(db.Integer, nullable=False, index=True, default=0)
    content = db.Column(db.Text,nullable=False)
    created = db.Column(db.DateTime,nullable=False)

    @property
    def author(self): # 我这定义的是啥 是个实例方法
        '''获取微博的作者'''
        return User.query.get(self.uid) # 谁调用 self 就指谁

    @property
    def upper(self):
        '''上一级评论'''
        if self.cid == 0:
            return None
        else:
            return Comment.query.get(self.cid)