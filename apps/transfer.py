from flask import Blueprint, render_template, session, redirect, url_for, flash, request

from .cursor import get_user_id, get_secure_key, get_user_balance, get_user_status


transfer_bp = Blueprint("transfer_bp", __name__, static_folder="static", template_folder="templates")

@transfer_bp.route("/", methods=["GET", "POST"])
def transfer():
	if "user" in session:
		user = session["user"]
		id = get_user_id(user)
		balance = get_user_balance(id)
		secure_key = get_secure_key(id)

		if request.method == "POST":
			form_balance = int(request.form["amount"])
			form_securekey = request.form["secure_key"]
			if not (form_balance <= balance and form_balance > 0):
				flash("Wrong Amount")
			if str(secure_key) != str(form_securekey):
				flash("Wrong Secure Key")

		return render_template("finances/transfer_page.html", username=user, user_id=id, balance=balance, balance1=balance,
                               status=get_user_status(id))
	else:
		return redirect('/')

@transfer_bp.route("/history")
def transfer_history():

	return
