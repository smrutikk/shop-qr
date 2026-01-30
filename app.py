from flask import Flask, redirect, request, render_template_string
import urllib.parse
from models import db, Shop

app = Flask(__name__)

# DB config (SQLite for now)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Xerox Print</title>
</head>
<body>
    <h2>Print Details</h2>
    <form action="/send/{{shop_id}}" method="get">
        <label>Copies:</label><br>
        <input type="number" name="copies" required><br><br>

        <label>Color:</label><br>
        <select name="color">
            <option value="Black & White">Black & White</option>
            <option value="Color">Color</option>
        </select><br><br>

        <label>Paper Size:</label><br>
        <select name="paper">
            <option value="A4">A4</option>
            <option value="A3">A3</option>
        </select><br><br>

        <button type="submit">Send on WhatsApp</button>
    </form>
</body>
</html>
"""

@app.route("/print/<int:shop_id>")
def print_form(shop_id):
    shop = Shop.query.get(shop_id)
    if not shop:
        return "Shop not found", 404

    return render_template_string(FORM_HTML, shop_id=shop_id)

@app.route("/send/<int:shop_id>")
def send_whatsapp(shop_id):
    shop = Shop.query.get(shop_id)
    if not shop:
        return "Shop not found", 404

    copies = request.args.get("copies")
    color = request.args.get("color")
    paper = request.args.get("paper")

    message = f"""Hi, I want to print documents.
Copies: {copies}
Color: {color}
Paper Size: {paper}
"""

    encoded = urllib.parse.quote(message)
    return redirect(f"https://wa.me/{shop.phone}?text={encoded}")

if __name__ == "__main__":
    app.run()
