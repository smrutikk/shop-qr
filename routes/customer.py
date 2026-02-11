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
    
    phone = request.args.get("phone")
    #copies = request.args.get("copies") or "1"
    #color = request.args.get("color") or "Not Specified"
    #paper = request.args.get("paper") or "Not Specified"

    if not phone:
        return "Customer phone is required", 400

    #if not all([copies, color, paper]):
     #   return "Missing print details", 400
    
    # Prepend +91 for India
    phone = phone.strip()
    if len(phone) == 10 and phone.isdigit():
        phone = f"+91{phone}"
    else:
        return "Invalid Indian phone number", 400

    new_request = PrintRequest(
        shop_id=shop.id,
        customer_phone=phone,
        #copies=int(copies),
        #color=color,
        #paper_size=paper
    )

    db.session.add(new_request)
    db.session.commit()

    message = f"""Hi, I want to print documents."""
    encoded = urllib.parse.quote(message)
    return redirect(f"https://wa.me/{shop.phone}?text={encoded}")