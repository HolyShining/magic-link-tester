from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from sqlalchemy import and_

from project import db
from project.models import User, Tokens
from project.handlers import EmailHandler, MagicTokenHandler

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    user_token = MagicTokenHandler.restore_token(request.args.get("token"))
    token = Tokens.query.filter(
        and_(Tokens.token == user_token, Tokens.is_valid == True)
    ).first()
    if not token:
        return "Oops"

    payload = MagicTokenHandler.fetch_payload(token)
    user = User.query.filter_by(email=payload.get("email", "")).first()
    if not user:
        return "Invalid token"

    user.login_count += 1
    db.session.commit()
    login_user(user, force=True)
    session["token_id"] = token.id
    flash("Successful log in")
    return redirect(url_for("main.index"))


@auth.route("/generate", methods=["GET"])
def generate_get():
    return render_template("generate.html")


@auth.route("/generate", methods=["POST"])
def generate_post():
    content = request.form
    email = content["email"]

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, login_count=0)
        db.session.add(user)
        db.session.flush()

    token = MagicTokenHandler.generate_token(user.email)
    db.session.add(token)
    db.session.commit()

    EmailHandler.send_email(
        user.email, "token_template.html", body={"token": token.token}
    )

    return render_template("generate.html", token=token.token, email=user.email)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/login_await", methods=["GET"])
def login_await():
    return "Please, review your email to log in"
