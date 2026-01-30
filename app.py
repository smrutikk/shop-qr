from flask import Flask
import os
from models import db, Shop
from routes.customer import customer_routes
from routes.dashboard import dashboard_routes

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Register blueprints
app.register_blueprint(customer_routes)
app.register_blueprint(dashboard_routes)

# Initialize DB
with app.app_context():
    db.create_all()
    if Shop.query.first() is None:
        shop = Shop(name="ABC Xerox", phone="918888310308")
        db.session.add(shop)
        db.session.commit()

if __name__ == "__main__":
    app.run()
