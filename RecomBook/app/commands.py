import click
import pandas as pd
from flask.cli import with_appcontext
from consolemenu import SelectionMenu
from app.db import db
from app.models import Books, Booktags, Tags,  Ratings, Goodreads_book, Toread
from app.helpers import (clean_books, clean_data_tags_booktags)


@click.command("insert-db")
@with_appcontext
def insert_db():
    """Insère les données nécessaire à l'utilisation de l'application"""

    tags = pd.read_csv("data/tags.csv")
    book_tags = pd.read_csv("data/book_tags.csv")
    to_read = pd.read_csv("data/to_read.csv")
    books = pd.read_csv("data/books.csv")
    ratings = pd.read_csv("data/ratings.csv")

    print(ratings)

    goodreads_book, tags, book_tags = clean_data_tags_booktags(tags, book_tags)
    books = clean_books(books)

    Tags.insert_from_pd(tags)
    Goodreads_book.insert_from_pd(goodreads_book)
    Booktags.insert_from_pd(book_tags)
    Books.insert_from_pd(books)
    Ratings.insert_from_pd(ratings)
    Toread.insert_from_pd(to_read)

    print("Données insérées !!")

