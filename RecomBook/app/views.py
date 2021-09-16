from flask import render_template, request, abort, redirect, url_for, Flask
from app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')