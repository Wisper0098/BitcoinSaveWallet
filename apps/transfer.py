from flask import Blueprint, render_template, session, redirect, url_for, flash, request

from .cursor import get_nowtime, get_user_id, get_secure_key, get_user_balance, get_user_status, get_user_account, add_funds, make_transaction, withdraw_funds, get_transaction


transfer_bp = Blueprint("transfer_bp", __name__, static_folder="static", template_folder="templates")

@transfer_bp.route("/", methods=["GET", "POST"])
def transfer():
	if "user" in session and get_user_status(get_user_id(session["user"])) > 0:
		user = session["user"]
		id = get_user_id(user)
		status = get_user_status(id)
		balance = get_user_balance(id)
		secure_key = get_secure_key(id)

		if request.method == "POST":
			form_balance = request.form["amount"]
			form_id = request.form["receiver_addr"]

			if not (float(form_balance) <= float(balance) and float(form_balance) > 0):
				flash("Wrong Amount")

			if get_user_account(form_id):
					
					if (float(balance) >= float(form_balance) and status == 0):
						withdraw_funds(id, form_balance)
						add_funds(form_id, form_balance)
						make_transaction(id, form_id, form_balance)
					
					if (float(balance) >= float(form_balance) and status > 0):
						withdraw_funds(id, form_balance)
						add_funds(form_id, form_balance)
						make_transaction(id, form_id, form_balance)
			
			if get_user_account(form_id) != 1:
				flash("Wrong User ID")




		return render_template("finances/transfer_page.html", username=user, user_id=id, balance=balance, balance1=balance,
                               status=status, nowtime=get_nowtime())
	else:
		return redirect('/')

@transfer_bp.route("/history")
def transfer_history():
	if "user" in session and get_user_status(get_user_id(session["user"])) > 0:
		user = session["user"]
		id = get_user_id(user)
		balance = get_user_balance(id)
		transactions = get_transaction(id)
	return render_template("finances/transfer_history.html", username=user, user_id=id, balance=balance, transactions=transactions,nowtime=get_nowtime())
