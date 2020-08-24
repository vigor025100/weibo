from libs.orm import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(128))
    gender = db.Column(db.Enum('男','女','保密'))
    city = db.Column(db.String(10))
    address = db.Column(db.String(64))
    phone = db.Column(db.String(16))
