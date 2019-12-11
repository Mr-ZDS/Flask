import click
from flask import Flask

app=Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!!!</h1>'

@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello,Flask!!</h1>'

@app.route('/greet')
@app.route('/greet/<name>')
def greet(name='Programmer'):
    return '<h1>hello, %s!!!</h1>' %name

#flask的自定义命令
@app.cli.command()
def hello():
    click.echo('Hello MAN')