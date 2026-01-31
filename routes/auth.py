from flask import Blueprint, render_template, request, redirect, session
from models import Shop

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")

        shop = Shop.query.filter_by(phone=phone).first()

        if not shop or shop.password != password:
            return render_template("login.html", error="Invalid credentials")

        session["shop_id"] = shop.id
        return redirect(f"/dashboard/{shop.id}")

    return render_template("login.html")


@auth_routes.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
