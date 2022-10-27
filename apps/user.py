from flask import Blueprint, render_template, session, redirect, url_for

from .cursor import get_nowtime, get_user_id, get_user_balance, get_user_status

user_bp = Blueprint("user_bp", __name__, static_folder="static", template_folder="templates")


@user_bp.route("/")
def profile():
    if "user" in session:
        user = session["user"]

        return render_template("profile/profile_page.html", 
                username=user, nowtime=get_nowtime(), user_id=get_user_id(user), 
                balance=get_user_balance(get_user_id(user)), status=get_user_status(get_user_id(user)))
        
    else: 
        return redirect(url_for("login"))


