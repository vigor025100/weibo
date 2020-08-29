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
    n_thumb = db.Column(db.Integer, nullable=False, default=0)

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


# 点赞
# 点赞是什么关系呀，是用户给另一个用户的微博，应该是说一个用户对另一个用户的一些东西进行了一些操作呢
# 写了这么多天，可以总结一下，就是每当我们要进行一定的操作的时候，都会创建一个表格，创建表格当然是用于存放数据的，我么
# 进行了一定操作的记录，是对操作的记录，之后就是要考虑表结构，表的结构，也是要根据你的业务需求来确定
# 点赞是一个 一对多 的关系结构，一 是一个用户，多是多条微博
# 对于点赞的行为，我们需要记录一些什么数据，谁给谁的微博点赞了，这里需要记录是谁的微博吗，其实不需要记录发这条微博的uid，
# 我们课题通过微博的wid 找到这条微博是谁发的，因此我么创建点赞数据记录表只需要记录 uid 和 wid
class Thumb(db.Model):
    '''点赞表'''
    __tablename__ = 'thumb'
    uid = db.Column(db.Integer, primary_key=True)
    wid = db.Column(db.Integer, primary_key=True)
    # 联合主键唯一，当再次插入相同数据的时候会报错，我们可以使用这个实现点赞和取消点赞
