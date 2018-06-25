#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask import Flask,g
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config

db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
config = Config()
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_object(config)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    # print(app.config)

    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint,url_prefix='/admin')

    @app.before_request
    def before_request():
        pass

    @app.before_first_request
    def before_first_request():
        pass

    # @app.teardown_request
    # def teardown_request():
    #     pass
    print(app.config)
    return app