from flask import Blueprint, render_template, redirect, session, abort
from models import db, Shop, PrintRequest
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

dashboard_routes = Blueprint("dashboard_routes", __name__)

@dashboard_routes.route("/dashboard/<int:shop_id>")
def dashboard(shop_id):
    # 🔐 Check login
    if "shop_id" not in session or session["shop_id"] != shop_id:
        return redirect("/login")

    shop = Shop.query.get(shop_id)
    if not shop:
        abort(404)


    requests = PrintRequest.query.filter_by(
        shop_id=shop.id
    ).order_by(PrintRequest.id.asc()).all()

    for r in requests:
        r.ist_time = r.timestamp.astimezone(IST)


    return render_template(
        "dashboard.html",
        shop=shop,
        requests=requests
    )


@dashboard_routes.route("/mark_completed/<int:req_id>")
def mark_completed(req_id):
    if "shop_id" not in session:
        return redirect("/login")

    req = PrintRequest.query.get(req_id)
    if not req:
        abort(404)

    if session["shop_id"] != req.shop_id:
        abort(403)

    req.status = "Completed"
    db.session.commit()

    return redirect(f"/dashboard/{req.shop_id}")


@dashboard_routes.route("/open_whatsapp/<int:req_id>")
def open_whatsapp(req_id):
    if "shop_id" not in session:
        return redirect("/login")

    req = PrintRequest.query.get(req_id)
    if not req:
        abort(404)

    if session["shop_id"] != req.shop_id:
        abort(403)

    # ✅ Mark as completed automatically
    req.status = "Completed"
    db.session.commit()

    # ✅ Open WhatsApp chat
    phone = req.customer_phone  # must be in international format
    whatsapp_url = f"https://wa.me/{phone}"

    return redirect(whatsapp_url)
