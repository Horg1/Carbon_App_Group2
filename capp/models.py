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

# Sample data
def seed_sample_data() -> None:
    if User.query.first():
        return

    sample_users = [
        User(username='Bjørk', email='bjork@example.com', password='seed-password'),
        User(username='Fjell', email='fjell@example.com', password='seed-password'),
        User(username='Aurora', email='aurora@example.com', password='seed-password'),
    ]
    db.session.add_all(sample_users)
    db.session.commit()

    transports = [
        Transport(kms=10, transport='Car', fuel='Petrol', co2=1.8, ch4=0.1, total=1.9, user_id=sample_users[0].id),
        Transport(kms=15, transport='Bus', fuel='Diesel', co2=1.2, ch4=0.05, total=1.25, user_id=sample_users[0].id),
        Transport(kms=5, transport='Train', fuel='Electric', co2=0.2, ch4=0.01, total=0.21, user_id=sample_users[1].id),
        Transport(kms=7, transport='Car', fuel='Hybrid', co2=0.8, ch4=0.02, total=0.82, user_id=sample_users[1].id),
        Transport(kms=18, transport='Flight', fuel='Jet fuel', co2=6.0, ch4=0.3, total=6.3, user_id=sample_users[2].id),
    ]
    db.session.add_all(transports)
    db.session.commit()
    
