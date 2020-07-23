from flask import Blueprint, render_template, url_for
from flask_login import login_required

from project.models import User
from project import db

monitoring = Blueprint("monitoring", __name__)


@monitoring.route("/monitoring")
def monitoring_get():
    users = User.query.all()
    users_map = {user: user.tokens for user in users}
    return render_template("monitoring.html", users=users_map.items())
