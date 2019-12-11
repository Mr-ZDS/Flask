# -*- coding: utf-8 -*-
import importlib

from flask import Flask, render_template

from blog.views.index import login_manager
from blog.extensions import db, migrate
from blog.urls import routers


def load_config_class(config_name):
    """导入config配置"""
    config_class_name = "%sConfig" % config_name.capitalize()
    print(config_class_name)
    app_name = __name__
    mod = importlib.import_module('%s.config.%s' % (app_name, config_name))
    config_class = getattr(mod, config_class_name, None)
    return config_class


def create_app(config_name):
    """创建app"""
    app = Flask(__name__)
    config_class = load_config_class(config_name)
    app.config.from_object(config_class)
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_blueprint(app)
    login_manager.init_app(app)
    return app


def configure_blueprint(app):
    for blueprint, url_prefix in routers:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def configure_extensions(app):
    db.init_app(app)


def configure_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(
            "errors/{0}.html".format(error_code),
            error=error
        ), error_code

    for errcode in [401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
