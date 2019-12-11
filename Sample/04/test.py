from forms import LoginForm
from flask import Flask,render_template

app=Flask(__name__)



@app.route('/basic')
def basic():
    form=LoginForm()
    return render_template('basic.html',form=form)



@app.route('/')
def index():
    return render_template('index.html')

