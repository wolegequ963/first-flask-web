# -*- coding: utf-8 -*-

# 导入 click 库，用于支持命令行工具
import click

# 导入 app 和 db 对象，以及 User 和 Movie 模型
from watchlist import app, db
from watchlist.models import User, Movie


# 定义一个名为 initdb 的命令行命令
@app.cli.command()
# 添加一个名为 drop 的选项
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    # 如果 drop 选项被启用
    if drop:
        # 删除所有数据库表
        db.drop_all()
    # 创建所有数据库表
    db.create_all()
    # 在命令行中输出初始化数据库完成的信息
    click.echo('Initialized database.')


# 定义一个名为 forge 的命令行命令
@app.cli.command()
def forge():
    """Generate fake data."""
    # 创建所有数据库表
    db.create_all()

    # 生成一些虚假数据
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    # 创建一个名为 Grey Li 的用户，并添加到数据库中
    user = User(name=name)
    db.session.add(user)
    # 添加电影数据到数据库中
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    # 提交所有更改到数据库中
    db.session.commit()
    # 在命令行中输出虚假数据生成完成的信息
    click.echo('Done.')


# 定义一个名为 admin 的命令行命令
@app.cli.command()
# 添加两个选项：username 和 password
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    # 创建所有数据库表
    db.create_all()

    # 查询数据库中是否已经存在用户，如果存在就更新用户的信息，否则就创建用户
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    # 提交所有更改到数据库中
    db.session.commit()
    # 在命令行中输出创建用户完成的信息
    click.echo('Done.')
