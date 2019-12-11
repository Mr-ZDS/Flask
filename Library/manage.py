from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import User, Uploader

# 模型数据库映射
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
