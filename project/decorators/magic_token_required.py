from flask import session, abort, redirect, url_for
from flask_login import login_required, logout_user

import functools

from project.models import Tokens


def magic_token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = Tokens.query.filter_by(id=session['token_id']).first()
        if token.is_valid is False:
            logout_user()
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)

    return login_required(decorated_function)
