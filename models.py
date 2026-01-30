from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.String(15), nullable = False)

    def __repr__(self):
        return f"<Shop {self.name}>"