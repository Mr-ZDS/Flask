from flask import Flask, render_template, Markup, flash, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

user = {'username': 'Zhang',
        'dashuai': 'A boy who loves movies and music.', }
movies = [{'name': 'One', 'year': '2000'},
          {'name': 'Two', 'year': '2001'},
          {'name': 'Three', 'year': '2002'},
          {'name': 'Four', 'year': '2003'},
          {'name': 'Five', 'year': '2004'},
          {'name': 'Six', 'year': '2005'},
          {'name': 'Seven', 'year': '2006'},
          {'name': 'Eight', 'year': '2007'},
          {'name': 'Nine', 'year': '2008'},
          {'name': 'Ten', 'year': '2009'}, ]


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/')
def index():
    return render_template('index.html')


# 自定义上下文
@app.context_processor
def inject_info():
    foo = 'I am foo.'
    return dict(foo=foo)


# 自定义全局函数
@app.template_global()
def bar():
    return 'I am bar.'


# 注册自定义过滤器
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')


# 自定义测试器
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


'''
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False
'''

@app.route('/watch')
def watch():
    return render_template('watch.html', user = user, movies = movies)


# 消息闪现
@app.route('/flash')
def just_flash():
    flash('I am flash,who is looking for me')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500



@app.route('/hello')
def hello():
    text = Markup('<h1>Hello,Flask!!!</h1>')
    return render_template('index.html', text = text)