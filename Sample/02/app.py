from flask import Flask, request, redirect, url_for, abort, make_response, session
import os
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


# 重定向路由
@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')  # 从cookie中获取name值
        response = '<h1>Hello , %s!!!</h1>' % name
        # 根据用户认证状态返回不同的内容
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
    return response


@app.route('/goback/<int:year>')  # <转换器：变量名>
def go_back(year):
    return '<p>Welcome to %d!!!</p>' % (2019 - year)


# any转换器需要在转换器后添加括号来给出可选值，如果不是可选值，会获得404错误响应
@app.route('/colors/<any(blue,white,red):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


'''
# 请求钩子
@app.before_request
def do_something():
    pass
'''


# 使用abort（）函数手动返回错误响应,被调用后，之后的代码不会被执行
@app.route('/404')
def not_found():
    abort(404)


'''
# 使用非默认HTML类型的其他MIME类型
@app.route('/foo')
def foo():
    response = make_response('Hello,World!!!')
    response.mimetype = 'text/plain'
    return response
'''


# 设置cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True  # 写入session
    return redirect(url_for('hello'))


# 模拟后台管理
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page'


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">点击返回</a>' % url_for('do_something', next = request.full_path)


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something</a>' % url_for('do_something', next = request.full_path)


@app.route('/do_something')
def do_something():
    return redirect(request.args.get('next', url_for('hello')))


def redirect_back(default = 'hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target:
            return redirect(target)
    return redirect(url_for(default, **kwargs))


# 验证url安全性
def is_safe_url(targer):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, targer))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# 显示虚拟文章
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n = 2)  # 生成两段随机文本
    return '''
<h1>A very long post</h1>
<div class="body">%s<div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more', // 目标URL
            type: 'get', // 请求方法
            success: function(data){ // 返回2XX响应后触发的回调函数
                $('.body').append(data); // 将返回的响应插入到页面中
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n = 1)
