from blog.models.bbs import Question
from blog.models.user import User


def test_index(client):  # 测试首页展示
    response = client.get('/')
    assert response.status_code == 200


def test_login_succ(client):  # 测试登录成功页面
    response = client.post("/login/", data={
        "telephone": 11111111111,
        "password": "111111",
    })
    assert response.status_code == 302


def test_login_fail(client):  # 测试登录失败
    response = client.post("/login/", data={
        "telephone": "32222222222",
        "password": "111111",
    })
    assert response.status_code == 200
    assert b'html' in response.data


# def test_regist(client):
#     user = User(telephone=121314151, username='test', password='111111')
#     db.session.add(user)
#     db.session.commit()
#     response = client.post('/regist/', user)
#     assert response.status_code == 200


def test_logout(client):
    response = client.get('/logout/')
    assert response.status_code == 302


def test_bbs(client):
    response = client.get('/bbs/')
    assert response.status_code == 200


def test_release(client):
    response = client.post('/release/', data={
        'title': "1",
        'content': '2',
    })
    assert response.status_code == 302


def test_detail(client):
    response = client.get('/detail/2')
    assert b'username' in response.data
    assert response.status_code == 200


def test_replies(client):
    response = client.post('/replies/', data={
        'content': "1",
        'question_id': '1',
        'user_id': '1',
        'answer_name': '1'
    })
    assert response.status_code == 302


def test_search(client):
    response = client.get('/?search=new')
    assert response.status_code == 200


def test_write_blog(client):
    response = client.post('/write_blog/', data={
        'title': '1',
        'blog_content': '1',
        'user_id': 1
    })
    assert response.status_code == 302


def test_personal_center(client):
    response = client.get('/personal_center/')
    assert response.status_code == 302


'''
def test_index(client):
    response = client.get('/')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['state'] == 1
'''
