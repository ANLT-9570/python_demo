from flask import session,redirect,url_for,g
from functools import wraps
import config


def login_required(func):

    @wraps(func)
    def inner(*args,**kwargs):
        if config.CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner

def permissions_required(permissions):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permissions(permissions):
                return func(*args, **kwargs)
            else:
                return redirect(url_for("cms.index"))
        return inner
    return outter