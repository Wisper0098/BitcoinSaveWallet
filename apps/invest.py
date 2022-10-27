from flask import Blueprint, render_template, session, redirect, url_for, flash, request

from .cursor import get_nowtime, check_btc_adrr_validity, get_user_id, get_user_status, get_user_balance

invest_bp = Blueprint("invest_bp", __name__, static_folder="static", template_folder="templates")

@invest_bp.route("/")
def invest():
    if "user" in session:
        user = session["user"]
        return render_template("profile/invest_page.html", username=user, nowtime=get_nowtime(), 
                                user_id=get_user_id(user), balance=get_user_balance(get_user_id(user)),vip_status=get_user_status(get_user_id(user)), status=get_user_status(get_user_id(user)))


@invest_bp.route('/<sum>', methods=["GET", "POST"])
def deposit(sum):

    AVAILABLE_PAYMENTS = [0.005, 0.05, 0.08, 0.10, 0.20, 0.50]

    try:
        if float(sum) in AVAILABLE_PAYMENTS:
            sum = sum
        else:
            sum = 0.005
    except:
        sum = 0.005

    if request.method == "POST":
        if check_btc_adrr_validity(request.form["TXID"]):
            return redirect(url_for("invest_bp.invest"))
        else:
            flash("Wrong TXID format")
    
    return render_template("finances/invest_pay.html", sum=sum, user=session["user"])