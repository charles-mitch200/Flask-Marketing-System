from market import app
from flask import render_template, redirect, url_for, request, flash
from market.models import Item, User
from market.forms import RegistrationField, LoginForm,PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required


# Route to the home page
@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


# Route to the market page (read)
@app.route("/market")
@login_required
def market_page():
    items = Item.query.all()
    purchase_form = PurchaseItemForm()
    return render_template("market.html", **locals())


# Route to the registration page (create)
@app.route("/register", methods=["GET", "POST"])
def registration_page():
    form = RegistrationField()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        # flash a new message and login the user
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")

        return redirect(url_for("market_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error in creating user: {err_msg}", category="danger")
    return render_template("register.html", **locals())


# Route to the login page
@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    # Check if form has been submitted with valid information
    if form.validate_on_submit():
        # Check if user exists and the password matches the one provided during registration
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f"Success! You are logged in as: {attempted_user.username}", category="success")
            return redirect(url_for("market_page"))
        else:
            flash(f"Username and password do not match!", category="danger")

    return render_template("login.html", **locals())


# Route to log out a user
@app.route("/logout")
def logout_page():
    logout_user()
    flash(f"Logged out successfully!", category="info")
    return redirect(url_for("home_page"))