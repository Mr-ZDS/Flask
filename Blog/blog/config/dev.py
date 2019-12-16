import os

import psycopg2


class DevConfig(object):
    "dev config class"
    DEBUG = True
    SECRET_KEY = os.urandom(24)

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:111111@ip:5432/blog"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
