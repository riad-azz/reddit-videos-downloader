# Flask modules
from flask import flash, request, url_for, redirect

# App modules
from app import login_manager
from app.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must sign in first before you continue", category="info")
    target = request.url_rule.rule[1:]
    redirect_url = url_for("auth.login_page") + f"?next=%2F{target}"
    return redirect(redirect_url)
