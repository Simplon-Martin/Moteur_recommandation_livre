from flask import Blueprint, render_template, request
from app.db import db
from app.helpers import (reco_by_user_id, filter_by_gender, filter_by_most_recent_gender)
import pandas as pd

main_controllers = Blueprint("main", __name__, url_prefix="/")


@main_controllers.route("/")
def index():
    books_1 = pd.read_sql_query('SELECT original_title, authors, image_url FROM Books LIMIT 4', db.engine, )
    books_2 = pd.read_sql_query('SELECT original_title, authors, image_url FROM Books LIMIT 4, 4', db.engine, )
    books_3 = pd.read_sql_query('SELECT original_title, authors, image_url FROM Books LIMIT 8, 4', db.engine, )
    # print(books_1.to_dict())
    # books_1 = books_1.to_dict()
    return render_template('index.html', books_1=books_1, books_2=books_2, books_3=books_3)


@main_controllers.route("/test", methods=['GET', 'POST'])
def test():
    books_1 = pd.read_sql_query('SELECT original_title, authors, image_url FROM Books LIMIT 15', db.engine, )
    # print(request.form['user_id'])
    return render_template('test.html', books_1=books_1)


@main_controllers.route("/reco_user", methods=['GET', 'POST'])
def reco_user():
    user_id = request.form['user_id']
    df = reco_by_user_id(user_id)
    l_df_gender, most_gender = filter_by_gender(df)
    df_final = filter_by_most_recent_gender(l_df_gender, most_gender)
    # print(l_df_final)
    # print(l_most_gender)
    return render_template('reco_user.html', data=df, list_gender=l_df_gender, most_recent=df_final)