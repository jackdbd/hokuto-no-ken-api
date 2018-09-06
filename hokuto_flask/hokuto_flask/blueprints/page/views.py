from flask import Blueprint, render_template

bp = Blueprint(name="page", import_name=__name__, template_folder="templates")


@bp.route("/")
def home():
    return render_template("page/home.html")


@bp.route("/about")
def about():
    return render_template("page/about.html")
