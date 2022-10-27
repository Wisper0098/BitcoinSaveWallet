from flask import Blueprint, render_template, session, redirect, url_for

from .cursor import get_user_id

deposit_bp = Blueprint("deposit_bp", __name__, static_folder="static", template_folder="templates")

@deposit_bp.route("/", methods=["GET", "POST"])
def deposit():
    return render_template("finances/deposit_page.html")

