from flask import Blueprint, request, redirect, render_template
import urllib.parse
from models import db, Shop, PrintRequest

customer_routes = Blueprint("customer_routes", __name__)

@customer_routes.route("/print/<int:shop_id>")
def print_form(shop_id):
    shop = Shop.query.get(shop_id)
    if not shop:
        return "Shop not found", 404
    return render_template("print_form.html", shop_id=shop_id)

@customer_routes.route("/send/<int:shop_id>")
def send_whatsapp(shop_id):
    shop = Shop.query.get(shop_id)
    if not shop:
        return "Shop not found", 404

    copies = request.args.get("copies")
    color = request.args.get("color")
    paper = request.args.get("paper")

    # Save request in DB
    new_request = PrintRequest(
        shop_id=shop.id,
        copies=copies,
        color=color,
        paper_size=paper
    )
    db.session.add(new_request)
    db.session.commit()

    # Prepare WhatsApp message
    message = f"""Hi, I want to print documents.
Copies: {copies}
Color: {color}
Paper Size: {paper}
"""
    encoded = urllib.parse.quote(message)
    return redirect(f"https://wa.me/{shop.phone}?text={encoded}")
