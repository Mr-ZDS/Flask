## 简易blog

本项目实现了一个简易的blog<br/>
提供的功能有**登录、注册、论坛markdown发帖，个人中心**等

--------------------------------------------------------------


### 部署运行
1、安装virtualenv
```
pip install virtualenv
```
2、创建虚拟环境
```
python -m venv venv
```
3、激活虚拟环境
```
venv\scripts\activate
```
4、更新依赖   
```
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

5、启动项目
```
flask run
```


### 使用`docker-compose`部署
```
docker-compose up -d --build
```
