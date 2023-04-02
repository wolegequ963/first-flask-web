# -*- coding: utf-8 -*-
from flask_login import UserMixin # 导入 UserMixin 类，为 Flask-Login 提供用户认证功能
from werkzeug.security import generate_password_hash, check_password_hash # 导入加密和解密函数
from watchlist import db # 导入数据库实例

# 继承 UserMixin 类并继承 db.Model 类（Model 是 SQLAlchemy 中的基类，代表数据库表）
class User(db.Model, UserMixin):
    # 定义数据库表字段
    id = db.Column(db.Integer, primary_key=True) # 数据库表的 ID 字段，作为主键
    name = db.Column(db.String(20)) # 用户名
    username = db.Column(db.String(20)) # 用户的登录账号
    password_hash = db.Column(db.String(128)) # 密码的哈希值

    # 定义一个方法，用来设置用户的密码，参数是密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) # 使用 generate_password_hash 函数生成密码哈希值

    # 定义一个方法，用来校验用户密码，参数是密码
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password) # 使用 check_password_hash 函数校验密码是否匹配

# 定义电影类
class Movie(db.Model):
    # 定义数据库表字段
    id = db.Column(db.Integer, primary_key=True) # 数据库表的 ID 字段，作为主键
    title = db.Column(db.String(60)) # 电影标题
    year = db.Column(db.String(4)) # 电影年份
