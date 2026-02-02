from app import app
from models import db, Shop

with app.app_context():
    db.create_all()

    shop = Shop(name="Jai Bajrang Auto Xerox", phone="919226864086")
    db.session.add(shop)
    db.session.commit()

    print("Database initialized with sample shop")
