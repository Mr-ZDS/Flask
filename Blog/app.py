import os

from blog import create_app

config_name = "dev"
app = create_app(config_name)
