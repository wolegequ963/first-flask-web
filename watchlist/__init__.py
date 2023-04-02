# -*- coding: utf-8 -*-

# 导入所需的模块
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 判断操作系统类型
WIN = sys.platform.startswith('win')

# 根据操作系统类型设置 SQLite 数据库 URI
if WIN:
    prefix = 'sqlite:///'  # Windows 系统下的 SQLite URI 前缀
else:
    prefix = 'sqlite:////'  # 其他系统下的 SQLite URI 前缀

# 创建 Flask 应用程序实例
app = Flask(__name__)

# 配置应用程序
app.config['SECRET_KEY'] = 'dev'  # 设置用于生成密钥的字符串
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')  # 设置数据库 URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭追踪数据库修改

# 创建 SQLAlchemy 数据库实例
db = SQLAlchemy(app)

# 创建登录管理器实例
login_manager = LoginManager(app)

# 定义用户加载函数，用于从数据库中加载用户
@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User  # 导入用户模型类
    user = User.query.get(int(user_id))  # 从数据库中加载指定 ID 的用户
    return user

# 设置登录页面的端点
login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'

# 注入 user 变量到所有模板中，可以让模板中直接使用该变量
@app.context_processor
def inject_user():
    from watchlist.models import User  # 导入用户模型类
    user = User.query.first()  # 获取第一个用户
    return dict(user=user)

# 导入应用程序的视图、错误处理和命令处理
from watchlist import views, errors, commands
