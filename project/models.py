from sqlalchemy.orm import relationship

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    login_count = db.Column(db.Integer)

    tokens = relationship("Tokens")

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True


class Tokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), db.ForeignKey(User.email))
    token = db.Column(db.String(65))
    is_valid = db.Column(db.Boolean())
