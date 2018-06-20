#!usr/bin/env python
# -*- encoding:utf-8 -*-
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_moment import Moment
from config import Config

# db = SQLAlchemy()
# moment = Moment()

def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)
    # db.init_app(app)
    # moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app