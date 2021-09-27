from pandas import DataFrame
from app.db import db


class Ratings(db.Model):
    __tablename__ = 'Ratings'
    rating_id = db.Column("rating_id", db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column('book_id', db.Integer, db.ForeignKey('Books.book_id'), nullable=False)
    user_id = db.Column("user_id", db.Integer)
    rating = db.Column("rating", db.Integer)

    def insert_from_pd(ratings: DataFrame):
        ratings.to_sql("Ratings", db.engine, if_exists="append")


class Booktags(db.Model):
    __tablename__ = 'Booktags'
    booktags_id = db.Column("user_id", db.Integer, primary_key=True, autoincrement=True)
    goodreads_book_id = db.Column("goodreads_book_id", db.Integer, db.ForeignKey('Goodreads_book.goodreads_id'))
    tag_id = db.Column("tag_id", db.Integer, db.ForeignKey('Tags.tag_id'))
    count = db.Column("count", db.Integer)

    def insert_from_pd(booktags: DataFrame):
        booktags.to_sql("Booktags", db.engine, if_exists="append", index=False)


class Toread(db.Model):
    __tablename__ = 'Toread'
    to_read_id = db.Column("to_read_id", db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("user_id", db.Integer)
    book_id = db.Column("book_id", db.Integer, db.ForeignKey('Books.book_id'), nullable=False)

    def insert_from_pd(toread: DataFrame):
        toread.to_sql("Toread", db.engine, if_exists="append", index=False)


class Goodreads_book(db.Model):
    __tablename__ = 'Goodreads_book'
    goodreads_id = db.Column("goodreads_id", db.Integer, primary_key=True)

    def insert_from_pd(goodreads_book: DataFrame):
        goodreads_book.to_sql("Goodreads_book", db.engine, if_exists="append", index=False)


class Tags(db.Model):
    __tablename__ = 'Tags'
    tag_id = db.Column("tag_id", db.Integer, primary_key=True)
    tag_name = db.Column("tag_name", db.String(50))

    def insert_from_pd(tags: DataFrame):
        tags.to_sql("Tags", db.engine, if_exists="append", index=False)


class Books(db.Model):
    __tablename__ = 'Books'
    book_id = db.Column("book_id", db.Integer, primary_key=True)
    goodreads_book_id = db.Column("goodreads_book_id", db.Integer, db.ForeignKey('Goodreads_book.goodreads_id'))
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
    work_ratings_count = db.Column("work_ratings_count", db.Integer)
    work_text_reviews_count = db.Column("work_text_reviews_count", db.Integer)
    ratings_1 = db.Column("ratings_1", db.Integer)
    ratings_2 = db.Column("ratings_2", db.Integer)
    ratings_3 = db.Column("ratings_3", db.Integer)
    ratings_4 = db.Column("ratings_4", db.Integer)
    ratings_5 = db.Column("ratings_5", db.Integer)
    image_url = db.Column("image_url", db.String(150))
    small_image_url = db.Column("small_image_url", db.String(150))
    author = db.Column("author", db.String(50))

    def insert_from_pd(books: DataFrame):
        books.to_sql("Books", db.engine, if_exists="append", index=False)
