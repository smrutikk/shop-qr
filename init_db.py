from app import app
from models import db, Shop

with app.app_context():
    db.create_all()

    shop = Shop(name="ABC Xerox", phone="918888310308")
    db.session.add(shop)
    db.session.commit()

    print("Database initialized with sample shop")
