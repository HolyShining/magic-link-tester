from flask import Blueprint, request, redirect, url_for

from project.models import Tokens
from project.handlers import MagicTokenHandler
from project import db

tokens = Blueprint("tokens", __name__)


@tokens.route("/tokens/deactivate")
@tokens.route("/tokens/activate", endpoint="activate")
def deactivate():
    user_token = MagicTokenHandler.restore_token(request.args.get("token"))
    rule = request.url_rule
    token = Tokens.query.filter(Tokens.token == user_token).first()
    if not token:
        return "Oops"

    if "deactivate" in rule.rule:
        token.is_valid = False
    elif "activate" in rule.rule:
        token.is_valid = True

    db.session.commit()
    return redirect(url_for("monitoring.monitoring_get"))


@tokens.route("/tokens/delete")
def delete_token():
    user_token = MagicTokenHandler.restore_token(request.args.get("token"))
    token = Tokens.query.filter(Tokens.token == user_token).first()
    if not token:
        return "Oops"
    db.session.delete(token)
    db.session.commit()
    return redirect(url_for("monitoring.monitoring_get"))


@tokens.route("/tokens/remove_access/<user_email>")
def remove_access(user_email=None):
    if not user_email:
        return "User email is required"
    query = Tokens.__table__.delete().where(Tokens.email == user_email)
    db.session.execute(query)
    db.session.commit()
    return redirect(url_for("monitoring.monitoring_get"))
