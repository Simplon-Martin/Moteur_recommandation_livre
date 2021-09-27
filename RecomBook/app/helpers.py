import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer
from datetime import datetime


# netoyage des données :::
def clean_books(books: pd.DataFrame):
    # transformer les isbn en str puis ajouter un 0 pour faire un nombre à 10 chiffres
    books['isbn'] = books['isbn'].apply(str)
    books['isbn'] = books['isbn'].apply(lambda x: '0' + x if len(x) == 9 else x)
    books['isbn'] = books['isbn'].apply(lambda x: '00' + x if len(x) == 8 else x)
    books['isbn'] = books['isbn'].apply(lambda x: '000' + x if len(x) == 7 else x)

    # transformer les isbn13 en str et enlever .0
    books['isbn13'] = books['isbn13'].apply(str)
    books['isbn13'] = books['isbn13'].apply(lambda x: x[:-2] if len(x) == 15 else x)
    books['isbn13'] = books['isbn13'].apply(lambda x: '0' + x[:-2] if len(x) == 14 else x)
    books['isbn13'] = books['isbn13'].apply(lambda x: '00' + x[:-2] if len(x) == 13 else x)
    # correction par élément
    books.loc[8173, 'isbn13'] = '0000195170342'  # set_value() deprecated use at iat
    books.dropna(inplace=True)
    books.reset_index(drop=True, inplace=True)
    # création d'une colonne author avec le premier membre de la liste authors
    author_sep = ', '
    mask = [author_sep in x for x in books['authors']]
    books_multi_author = books[mask]
    # 2079 livres ont des co-auteurs, on suppose que le premier est le principal
    books['author'] = books['authors'].apply(lambda x: x[:x.find(', ')] if x.find(', ') > 0 else x)
    return books


def clean_data_tags_booktags(tags: pd.DataFrame, book_tags: pd.DataFrame):
    porter = PorterStemmer()  # instanciation du stemmer
    # avant le lem on remplace les - par ' ' si lem strip
    tags['tag_lem'] = tags['tag_name'].apply(lambda x: x.replace('-', ' ').strip())
    tags['tag_lem'] = tags['tag_lem'].apply(porter.stem)  # lem ne strip pas

    l_amazon_book_tags = ['Children', 'Literature', 'Fiction', 'Religion', 'Spirituality', 'Reference', 'Health',
                          'Fitness', 'Dieting', 'Self-Help', 'Politics', 'Social', 'Christian', 'Bibles', 'Education',
                          'Teaching', 'Arts', 'Photography', 'Humor', 'Entertainment', 'Business', 'Money', 'Science',
                          'Math', 'Teen', 'Young Adult', 'Medical', 'Crafts', 'Hobbies', 'Home', 'History', 'Mystery',
                          'Thriller', 'Suspense', 'Biographies', 'Memoirs', 'Comics', 'Graphic Novels', 'Romance',
                          'Science Fiction', 'Fantasy', 'Cookbooks', 'Food', 'Wine', 'Parenting', 'Relationships',
                          'Test', 'Engineering', 'Transportation', 'Computers', 'Technology', 'Sports', 'Outdoors',
                          'Travel', 'Law', 'LGBTQ', 'Calendars', 'Manga']

    l_amazon_book_tags_stem = []
    for s in l_amazon_book_tags:
        l_amazon_book_tags_stem.append(porter.stem(s))  # porter ne fonctionne pas sur liste
    tags['amazon'] = tags['tag_lem'].apply(lambda x: 'amazon' if x in l_amazon_book_tags_stem else 'no')
    # TODO faire une fonction avec ''.find à la place de la lambda

    # Pour chaque tag unique on lui attribue un nouvel index
    dict_tags = {}
    l_tags_lem = (tags['tag_lem'][tags['amazon'] == 'amazon']).unique()
    new_index = 0
    for t in l_tags_lem:
        new_index += 1
        dict_tags[t] = new_index  # initialise le dico de tags
    tags['tag_name'] = tags['tag_lem']
    tags['tag_name'].replace(dict(zip(l_amazon_book_tags_stem, l_amazon_book_tags)), inplace=True)
    # on applique le dict aux valeurs de tag_lem
    tags['tag_lem'].replace(dict_tags, inplace=True)
    tags = tags[tags['amazon'] == 'amazon']  # on enlève les tags qui ne sont pas reconnus

    dict_tags = {}
    l_tag_id = tags['tag_id'].tolist()
    l_tag_id_new = tags['tag_lem'].tolist()
    for index in range(len(l_tag_id)):
        dict_tags[l_tag_id[index]] = l_tag_id_new[index]
    book_tags['new_tag_id'] = book_tags['tag_id'].apply(lambda x: x if x in l_tag_id else np.nan)
    book_tags['new_tag_id'].replace(dict_tags, inplace=True)
    book_tags.dropna(inplace=True)
    book_tags['tag_id'] = book_tags['new_tag_id']
    book_tags = book_tags.groupby(['goodreads_book_id', 'tag_id'])['count'].sum().reset_index()

    # Clean tags pour avoir que le nouvel index et les name d'Amazon
    tags = tags[['tag_lem', 'tag_name']].drop_duplicates()
    # puis renommer la colonne
    tags.rename(columns={'tag_lem': 'tag_id'}, inplace=True)
    goodreads_book = pd.DataFrame(book_tags['goodreads_book_id'].unique(), columns=['goodreads_id'])
    return goodreads_book, tags, book_tags
