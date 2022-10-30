from flask import Blueprint, render_template, session, redirect, url_for, request, flash

from .cursor import get_secure_key, check_btc_adrr_validity

from .cursor import get_user_id, get_user_balance, get_user_status


withdraw_bp = Blueprint("withdraw_bp", __name__, static_folder="static", template_folder="templates")

@withdraw_bp.route("/", methods=["GET", "POST"])
def withdraw():
    if "user" in session:  
        user = session["user"]
        id = get_user_id(user)
        balance = get_user_balance(id)
        secure_key = get_secure_key(id)

        if request.method == "POST":
            form_amount = request.form["amount"]
            form_addr = request.form["receiver_addr"]
            form_securekey = request.form["secure_key"]

            try:
                if int(form_amount) <= balance:
                    pass
                if int(form_amount) > balance:
                    flash("Wrong amount")
                if check_btc_adrr_validity(form_addr):
                    pass
                if not check_btc_adrr_validity(form_addr):
                    flash("Wrong BTC address")
                if str(secure_key) == str(form_securekey):
                    pass
                if str(secure_key) != str(form_securekey):
                    flash("Wrong Secure Key")
            except:
                pass
        
        return render_template("finances/withdraw_page.html", balance1=balance, username=user, user_id=id, balance=get_user_balance(id),
                               status=get_user_status(id))
        
    else: 
        return redirect(url_for("login"))
