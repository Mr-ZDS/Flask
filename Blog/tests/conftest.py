import pytest
from app import app


@pytest.fixture(scope='session')
def setup(request):
    def teardown():
        print('测试用例执行结束------------------')

    request.addfinalizer(teardown)
    print('测试用例执行开始----------------')


@pytest.fixture
def client():
    """Create a test client to send requests to"""
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

