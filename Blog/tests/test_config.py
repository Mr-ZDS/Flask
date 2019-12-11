from app import app
from blog.models.user import User


def test_password_hash(setup):  # 测试密码加密
    user = User(telephone='11111111111', password='111111')
    assert user.check_password('111111') is True
    assert user.check_password('11') is False


def test_config(setup):  # 测试配置信息
    assert app.config['DEBUG'] == True
    assert app.config[
               'SQLALCHEMY_DATABASE_URI'] == \
           "postgresql+psycopg2://postgres:111111@localhost:5432/blog"
