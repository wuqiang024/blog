#!usr/bin/env python
# -*- encoding:utf-8 -*-

from . import main

@main.route('/index')
def index():
    return 'main.index'