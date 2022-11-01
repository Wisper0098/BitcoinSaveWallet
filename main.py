from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from apps.user import user_bp
from apps.invest import invest_bp
from apps.deposit import deposit_bp
from apps.withdraw import withdraw_bp
from apps.transfer import transfer_bp
from apps.cursor import *


SECRET_KEY = "DxRPbsaCnQ4ntFmq"

app = Flask(__name__, static_folder='static')
app.register_blueprint(user_bp, url_prefix="/profile")
app.register_blueprint(invest_bp, url_prefix="/invest")
app.register_blueprint(deposit_bp, url_prefix="/deposit/")
app.register_blueprint(withdraw_bp, url_prefix="/withdraw")
app.register_blueprint(transfer_bp, url_prefix="/transfer")

app.secret_key = SECRET_KEY


@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_user_existence(username, password) != 0 and len(str(username)+str(password)) > 0:
            
            session["user"] = username
            return redirect(url_for("user_bp.profile"))

        else:
            flash("Wrong login or password")
            #session["_flashes"].clear()
    
    else:
        if "user" in session:
            username = session["user"]
            return redirect(url_for("user_bp.profile"))


    return render_template('signing/login.html')


@app.route('/signup', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        btc_wallet = request.form["btc_wallet"]
        password = request.form["password"]
        confirmed_pswd = request.form["confirmed_pswd"]
        secure_key = request.form["secure_key"]
        confirmed_secure_key = request.form["confirmed_secure_key"]

        check_usr = check_user_existence(username, password)
        chck_email = check_email(email)

        if check_usr == 0:
            
            if chck_email != 0:
                pass
            else:
                create_new_user(username, email, phone, btc_wallet, password, secure_key)
                session["user"] = username
                return redirect(url_for('user_bp.profile'))
        else:
            pass
            
        
    return render_template('register_old.html')


@app.route('/logout')
def logout():
    session.pop("user", 0)
    return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.register_error_handler(404, page_not_found)
    app.run(debug=True)