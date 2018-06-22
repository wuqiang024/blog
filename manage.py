#!usr/bin/env python
# -*- encoding:utf-8 -*-
from app import create_app,db
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
from app.models import *

def make_shell_context():
    return dict(db=db,
                User=User,
                Menu=Menu,
                Article=Article,
                ArticleTypeSetting=ArticleTypeSetting,
                ArticleType=ArticleType,
                Source=Source)

app = create_app()
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
manager.add_command('shell',Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()