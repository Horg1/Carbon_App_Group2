from __future__ import annotations

from datetime import datetime

from capp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    transport = db.relationship(
        'Transport',
        primaryjoin='User.id == foreign(Transport.user_id)',
        back_populates='author',
        lazy=True,
    )

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"


class Transport(db.Model):
    __bind_key__ = 'transport'
    __tablename__ = 'transport_table'

    id = db.Column(db.Integer, primary_key=True)
    kms = db.Column(db.Float, nullable=False)
    transport = db.Column(db.String(40), nullable=False)
    fuel = db.Column(db.String(40), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    co2 = db.Column(db.Float, nullable=False)
    ch4 = db.Column(db.Float, nullable=False, default=0.0)
    total = db.Column(db.Float, nullable=False)
    seafood_kg = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, nullable=False)

    author = db.relationship(
        'User',
        primaryjoin='foreign(Transport.user_id) == User.id',
        back_populates='transport',
        lazy=True,
    )

    def __repr__(self) -> str:
        return (
            f"Transport('{self.transport}', kms={self.kms}, total={self.total}, user_id={self.user_id})"
        )
