#!usr/bin/env python
# -*- encoding:utf-8 -*-
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return '404'