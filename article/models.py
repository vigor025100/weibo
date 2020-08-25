from libs.orm import db

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(20),nullable=False)
    date = db.Column(db.DateTime)
