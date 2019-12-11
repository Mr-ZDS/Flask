from blog.extensions import db
from blog.models.user import User, Blog

'''
def test_add():
    user = User(telephone=121314151, username='test', password='111111')
    blog = Blog(id=5, blog_title='1', blog_content='1',
                create_time='2019.11.11', blogger_id=1)
    db.session.add_all(user, blog)
    db.session.commit()
    assert user is not None
    assert blog.id == 5


def test_search():
    # 测试正确搜索到数据
    test = User.query.filter(User.username == 'zhang').first()
    assert test is not None
    blog = Blog.query.filter(Blog.blog_title == '1').first()
    assert blog is not None
    # 测试错误搜索
    test = User.query.filter(User.username == '1').first()
    assert test is None
    blog = Blog.query.filter(Blog.blog_tite == '2').first()
    assert blog is None
'''
