from market import app
from flask import render_template, redirect, url_for, request
from market.models import Item, User
from market.forms import RegistrationField
from market import db


# Route to the home page
@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


# Route to the market page (read)
@app.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", **locals())


# Route to the registration page (create)
@app.route("/register", methods=["GET", "POST"])
def registration_page():
    form = RegistrationField()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("market_page"))
    return render_template("register.html", **locals())