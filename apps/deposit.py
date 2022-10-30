from flask import Blueprint, render_template, session, redirect, url_for, request, flash

from .cursor import get_user_id, get_user_balance, get_user_status, add_funds

deposit_bp = Blueprint("deposit_bp", __name__, static_folder="static", template_folder="templates")

@deposit_bp.route("/", methods=["GET", "POST"])
def deposit():
    if "user" in session:
        user = session["user"]
        id = get_user_id(user)
        if request.method == "POST":
            txid = request.form["TXID"]
            if len(txid) != 64:
                flash("Wrong TXID Format")
            else:
                flash("You will receive our answer on your email")
        return render_template("finances/deposit_page.html", username=user, user_id=id, balance=get_user_balance(id),
                               status=get_user_status(id))#username=usr_info["username"],
                               #user_id=usr_info["user_id"], balance=usr_info["balance"], status=usr_info["status"])
    else:
        return redirect('/')

