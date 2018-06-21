#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
config = Config()

def create_app():
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_object(config)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    # print(app.config)

    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app