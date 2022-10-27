from flask import Blueprint, render_template, session, redirect, url_for, request, flash

from .cursor import get_secure_key, get_user_balance, get_user_id, check_btc_adrr_validity

withdraw_bp = Blueprint("withdraw_bp", __name__, static_folder="static", template_folder="templates")

@withdraw_bp.route("/", methods=["GET", "POST"])
def withdraw():
    if "user" in session:  
        user = session["user"] 
        balance = get_user_balance(get_user_id(user))
        secure_key = get_secure_key(get_user_id(user))
        if request.method == "POST":
            form_amount = request.form["amount"]
            form_addr = request.form["receiver_addr"]
            form_securekey = request.form["secure_key"]

            try:
                if int(form_amount) <= balance:
                    pass
                elif int(form_amount) > balance:
                    flash("Wrong amount")
                elif check_btc_adrr_validity(form_addr):
                    pass
                elif check_btc_adrr_validity(form_addr) == False:
                    flash("Wrong BTC address")
                if str(secure_key) == str(form_securekey):
                    pass
                if str(secure_key) != str(form_securekey):
                    flash("Wrong Secure Key")
            except:
                pass
        
        return render_template("finances/withdraw_page.html", balance=balance)        
        
    else: 
        return redirect(url_for("login"))
