from flask import Blueprint, render_template, redirect
from models import db, Shop, PrintRequest

dashboard_routes = Blueprint("dashboard_routes", __name__)

@dashboard_routes.route("/dashboard/<int:shop_id>")
def dashboard(shop_id):
    shop = Shop.query.get(shop_id)
    if not shop:
        return "Shop not found", 404

    requests = PrintRequest.query.filter_by(shop_id=shop.id).order_by(PrintRequest.timestamp.desc()).all()
    return render_template("dashboard.html", shop=shop, requests=requests)

@dashboard_routes.route("/mark_completed/<int:req_id>")
def mark_completed(req_id):
    req = PrintRequest.query.get(req_id)
    if not req:
        return "Request not found", 404

    req.status = "Completed"
    db.session.commit()
    return redirect(f"/dashboard/{req.shop_id}")
