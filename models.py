from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class PrintRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)

    customer_phone = db.Column(db.String(20), nullable=True)  # 👈 NEW

    copies = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    paper_size = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), default='Pending')

    timestamp = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    shop = db.relationship('Shop', backref=db.backref('requests', lazy=True))

