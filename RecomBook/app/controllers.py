from flask import Blueprint, render_template

main_controllers = Blueprint("main", __name__, url_prefix="/")


@main_controllers.route("/")
def index():
    return render_template('index.html')