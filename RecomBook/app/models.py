from pandas import DataFrame
from app.db import db


class Ratings(db.Model):
    rating_id = db.Column("rating_id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer)
    book_id = db.Column("book_id", db.Integer)
    rating = db.Column("rating", db.Integer)
