FROM python:3.7

RUN mkdir -p /var/www/blog
WORKDIR /var/www/blog

COPY . /var/www/blog/
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

RUN python manage.py db init
RUN python manage.py db migrate
RUN python manage.py db upgrade

CMD ["python", "app.py"]
EXPOSE 5000
