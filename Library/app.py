from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from models import User, Uploader, Comment, Question, Answer
from exts import db
from functools import wraps
from sqlalchemy import or_, desc
import config
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 登录限制功能，如上传和下载时必须先登录才能继续操作
def login_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper


@app.route('/')
def index():
    context = {
        'contexts': Uploader.query.order_by(desc('upload_time')).all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            flash('手机号码或者密码错误！请重新登录！！！')
            return render_template('login.html')


@app.route('/regist/', methods = ['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 查看手机号码是否已经被注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            flash('该手机号码已经被注册！请更换手机号码或者登录！！！')
            return render_template('regist.html')
        else:
            # 两次密码必须相同才能成功注册
            if password1 != password2:
                flash('两次密码不相同！请重新输入!!!')
                return render_template('regist.html')
            else:
                user = User(telephone = telephone, username = username, password = password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # 注销只需要不是登录状态，即把session保存的user_id删除即可，也可直接删除session的内容
    session.clear()
    return redirect(url_for('login'))

#文件上传的格式
ALLOWED_EXTENSIONS = set(['pdf', 'docx'])

#限制文件上传的格式
def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 装饰器限制上传前必须先登录
@app.route('/upload/', methods = ['GET', 'POST'])  # 出现405错误，很多情况下加上method
@login_limit
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        f = request.files['file']
        if allow_file(f.filename):
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            upload_path = os.path.join(basepath, 'static/library',
                                       secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
        else:
            flash('书籍格式错误或者上传错误！！！！')
            return render_template('upload.html')

        # 获取并保存到数据库
        file_name = request.form.get('book_name')
        introduction = request.form.get('book_introduct')
        up_load = Uploader(file_name = file_name, Introduct = introduction)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        up_load.uploader = user
        db.session.add(up_load)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<book_id>')
def detail(book_id):
    visit = Uploader.query.filter(Uploader.id == book_id).first()
    count = Comment.query.filter(Comment.upload_id == book_id).count()
    return render_template('detail.html', up = visit, count = count)


# 图书评论
@app.route('/comment/', methods = ['POST'])
@login_limit
def add_comment():
    content = request.form.get('comment-content')
    comment_id = request.form.get('comment_id')
    comment = Comment(content = content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    upload = Uploader.query.filter(Uploader.id == comment_id).first()
    comment.file_list = upload
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', book_id = comment_id))


# 下载图书
@app.route("/download/<path:filename>")
@login_limit
def download(filename):
    dirpath = os.path.join(app.root_path, 'static/library')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    return send_from_directory(dirpath, filename, as_attachment = True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载


# 在线观看
@app.route('/online/<path:filename>')
def online(filename):
    dirpath = os.path.join(app.root_path, 'static/library')
    return send_from_directory(dirpath, filename, as_attachment = False)


@app.route('/search/')
def search():
    q = request.args.get('search')
    book = Uploader.query.filter(or_(Uploader.file_name.contains(q),
                                     Uploader.Introduct.contains(q))).order_by('upload_time')
    return render_template('index.html', contexts = book)


@app.route('/question/', methods = ['GET', 'POST'])
@login_limit  # 登录限制装饰器
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title = title, content = content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('ques_list'))


@app.route('/add_answer/', methods = ['POST'])
@login_limit
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content = content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('details', question_id = question_id))


@app.route('/details/<question_id>/')
def details(question_id):
    questions = Question.query.filter(Question.id == question_id).first()
    count = Answer.query.filter(Answer.question_id == question_id).count()
    return render_template('details.html', question = questions, count = count)


@app.route('/ques_list/')
def ques_list():
    context = {'questions': Question.query.order_by(desc('create_time')).all()}
    return render_template('ques_list.html', **context)


@app.route('/personal')
@login_limit
def personal():
    user_id = session['user_id']
    context = {'personal': Uploader.query.filter(Uploader.upload_id == user_id).all()}
    if context['personal'] != []:
        user = Uploader.query.filter(Uploader.upload_id == user_id).first()
        count = Uploader.query.filter(Uploader.upload_id == user_id).count()
        return render_template('personal.html', **context, user = user, count = count)
    else:
        return redirect(url_for('index'))


# 删除上传的书籍，首先获取书籍id，根据id先删除评论的内容，最后删除书籍
@app.route('/delete/<book_id>', methods = ['GET', 'POST'])
def delete(book_id):
    comment = Comment.query.filter(Comment.upload_id == book_id).first()
    while comment:
        db.session.delete(comment)
        db.session.commit()
        comment = Comment.query.filter(Comment.upload_id == book_id).first()
    upload = Uploader.query.filter(Uploader.id == book_id).first()
    db.session.delete(upload)
    db.session.commit()
    return redirect(url_for('personal'))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    if user:
        return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
