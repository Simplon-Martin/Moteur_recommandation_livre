from pandas import DataFrame
from app.db import db


class Ratings(db.Model):
    __tablename__ = 'ratings'
    rating_id = db.Column("rating_id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer)
    rating_book_id = db.Column("book_id", db.Integer, db.ForeignKey('books.book_id'))
    rating = db.Column("rating", db.Integer)


class Booktags(db.Model):
    __tablename__ = 'booktags'
    goodreads_book_id = db.Column("goodreads_book_id", db.Integer, primary_key=True)
    tag_id = db.Column("tag_id", db.Integer, db.ForeignKey('tags.tag_id'))
    count = db.Column("book_id", db.Integer)


class Toread(db.Model):
    __tablename__ = 'toread'
    user_id = db.Column("user_id", db.Integer, primary_key=True)
    toread_book_id = db.Column("toread_book_id", db.Integer, db.ForeignKey('books.book_id'))


class Tags(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column("tag_id", db.Integer, primary_key=True)
    tag_name = db.Column("tag_name", db.String(50))


class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column("book_id", db.Integer, primary_key=True)
    goodreads_book = db.Column("goodreads_book", db.Integer, db.ForeignKey('booktags.goodreads_book_id'))
    best_book_id = db.Column("best_book_id", db.Integer)
    work_id = db.Column("work_id", db.Integer)
    books_count = db.Column("books_count", db.Integer)
    isbn = db.Column("isbn", db.String(10))
    isbn13 = db.Column("isbn13", db.String(13))
    authors = db.Column("authors", db.String(750))
    original_publication_year = db.Column("original_publication_year", db.Integer)
    original_title = db.Column("original_title", db.String(200))
    title = db.Column("title", db.String(200))
    language_code = db.Column("language_code", db.String(10))
    average_rating = db.Column("average_rating", db.Float)
    ratings_count = db.Column("ratings_count", db.Integer)
    work_text_reviews_count = db.Column("work_text_reviews_count", db.Integer)
    ratings_1 = db.Column("ratings_1", db.Integer)
    ratings_2 = db.Column("ratings_2", db.Integer)
    ratings_3 = db.Column("ratings_3", db.Integer)
    ratings_4 = db.Column("ratings_4", db.Integer)
    ratings_5 = db.Column("ratings_5", db.Integer)
    image_url = db.Column("image_url", db.String(150))
    small_image_url = db.Column("small_image_url", db.String(150))
    author = db.Column("author", db.String(50))
