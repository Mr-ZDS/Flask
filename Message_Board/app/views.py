from flask import flash,redirect,url_for,render_template
from app import app,db
from app.models import Message
from app.forms import HelloForm

@app.route('/',methods = ['GET','POST'])
def index():
    #order_by()过滤器对数据库记录排序
    messages=Message.query.order_by(Message.timestamp.desc()).all()
    form=HelloForm()
    if form.validate_on_submit():
        name=form.name.data
        body=form.body.data
        message=Message(body=body,name=name)     #实例化模型类，创建记录
        db.session.add(message)       #添加纪录到数据库会话
        db.session.commit()
        flash('Your Message have been send to orders!!!')
        return redirect(url_for('index'))    #重定向
    return render_template('index.html',form=form,messages=messages)