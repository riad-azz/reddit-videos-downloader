# Flask modules
from flask import (
    render_template,
    flash,
    request,
    url_for,
    redirect,
    Blueprint,
)
from flask_login import login_user, logout_user, current_user

# App modules
from app import db, bcrypt
from app.models import User
from app.forms import RegisterForm, LoginForm


auth_bp = Blueprint(
    "auth", __name__, template_folder="templates", static_folder="static"
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("views.pages.home_page"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            redirect_url = request.args.get("next", url_for("views.pages.home_page"))
            flash(
                f'Success, you are signed in as "{user.username}".', category="success"
            )
            return redirect(redirect_url)
        else:
            flash("Invalid username or password", category="danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for("views.pages.home_page"))

    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash(
            f'Success, your account has been created. You are now signed in as "{new_user.username}"',
            category="success",
        )
        return redirect(url_for("views.pages.home_page"))

    return render_template("auth/signup.html", form=form)


@auth_bp.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("views.pages.home_page"))

    logout_user()
    flash("You have been logged out.", category="info")
    return redirect(url_for("views.pages.home_page"))
