#!usr/bin/env python
# -*- encoding:utf-8 -*-
from . import auth
from . import LoginForm

@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit:
        return 'ok'
    return render_template('auth/login.html',form=form)