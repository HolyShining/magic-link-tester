from flask import Blueprint, render_template, session
from flask_login import login_required
from project.decorators import magic_token_required

from project import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Main page"""
    return render_template("index.html")


@main.route("/secret")
@magic_token_required
def secret():
    return render_template("secret.html")
