from market import app
from flask import render_template, redirect, url_for, request, flash
from market.models import Item, User
from market.forms import RegistrationField, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


# Route to the home page
@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


# Route to the market page (read)
@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    # To avoid the confirm form resubmission popup
    if request.method == "POST":
        # purchase item logic
        # Access the item using the input's name
        purchased_item = request.form.get("purchased_item")
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for ${p_item_object.price}.", category="success")
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category="danger")
        # sell item logic
        sold_item = request.form.get("sold_item")
        s_item_object = Item.query.filter_by(name=sold_item).first()
        # Check if the object exists
        if s_item_object:
            # Does the user really own this item
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name}!", category="success")
            else:
                flash(f"Sorry! Something went wrong while selling {s_item_object.name}", category="danger")

        return redirect(url_for("market_page"))
    # Display only items without an owner
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
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
@login_required
def logout_page():
    logout_user()
    flash(f"Logged out successfully!", category="info")
    return redirect(url_for("home_page"))