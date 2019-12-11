import markdown

from flask import (
    render_template, request, redirect, url_for, session, Blueprint
)
from flask_login import LoginManager, login_required, login_user

from sqlalchemy import desc, or_

# from blog.decorators.login_limit import login_limit
from blog.extensions import db
from blog.models.bbs import Answer, Question
from blog.models.user import User, Blog

index_router = Blueprint("index", __name__)
login_manager = LoginManager()
login_manager.login_view = "index.login"


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user:
        return user
    else:
        return None


@index_router.route('/')
def index():
    context = {'questions': Question.query.order_by(desc('ques_time')).all(),
               'blog': Blog.query.order_by(desc('create_time')).all()}
    return render_template('index.html', **context)


@index_router.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        login_user(user)
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            print('login succeed!!!')
            return redirect(url_for('index.index'))
        else:
            print('The username or password error!!!')
            return render_template('login.html')


@index_router.route('/regist/', methods=['GET', 'POST'])
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
            print('该手机号码已经被注册！请更换手机号码或者登录！！！')
            return render_template('regist.html')
        else:
            # 两次密码必须相同才能成功注册
            if password1 != password2:
                print('两次密码不相同！请重新输入!!!')
                return render_template('regist.html')
            else:
                user = User(telephone=telephone, username=username,
                            password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('index.login'))


# # 上下文管理器，把当前用户传给html
# @index_router.context_processor
# def my_context_processor():
#     user_id = session.get('user_id')
#     user = User.query.filter(User.id == user_id).first()
#     if user:
#         return {'user': user}
#     else:
#         return {}


@index_router.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index.login'))


# 论坛首页
@index_router.route('/bbs/')
def bbs():
    context = {'questions': Question.query.order_by(desc('ques_time')).all()}
    return render_template('bbs.html', **context)


@index_router.route('/release/', methods=['GET', 'POST'])
@login_required
def release():
    if request.method == 'GET':
        return render_template('release.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.blogger = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index.bbs'))


@index_router.route('/detail/<question_id>')
def detail(question_id):
    questions = Question.query.filter(Question.id == question_id).first()
    count = Answer.query.filter(Answer.question_id == question_id).count()
    return render_template('detail.html', question=questions, count=count)


@index_router.route('/replies/', methods=['POST'])
@login_required
def replies():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.answer_name = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('index.detail', question_id=question_id))


@index_router.route('/search/')
def search():
    search_content = request.args.get('search')
    question = Question.query.filter(
        or_(Question.title.contains(search_content),
            Question.content.contains(search_content))).order_by('ques_time')
    blog = Blog.query.filter(or_(Blog.blog_title.contains(search_content),
                                 Blog.blog_content.contains(
                                     search_content))).order_by('create_time')
    return render_template('index.html', questions=question, blog=blog)


@index_router.route('/write_blog/', methods=['GET', 'POST'])
@login_required
def write_blog():
    if request.method == 'GET':
        return render_template('write_blog.html')
    else:
        title = request.form.get('title')
        blog_content = request.form.get('TextContent')
        html = markdown.markdown(blog_content)
        blog = Blog(blog_title=title, blog_content=html)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        blog.blogger = user
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('index.bbs'))


@index_router.route('/personal_center/')
@login_required
def personal_center():
    user_id = session.get('user_id')
    context = {'blog': Blog.query.filter(Blog.blogger_id == user_id).all()}
    blogger = Blog.query.filter(Blog.blogger_id == user_id).first()
    count = Blog.query.filter(Blog.blogger_id == user_id).count()
    return render_template('personal_center.html', **context, blogger=blogger,
                           count=count)


@index_router.route('/blog_detail/')
def blog_detail(blog_id):
    blogs = Blog.query.filter(Blog.id == blog_id).first()
    return render_template('personal_center.html', blogs=blogs)
