import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer
from app.db import db
from sklearn.metrics.pairwise import cosine_similarity


# netoyage des données :::
def clean_books(books: pd.DataFrame):
    """

    :param books:
    :return: books
    """
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
    """

    :param tags:
    :param book_tags:
    :return:
    """
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


def reco_by_user_id(user_id):
    """
    Identification des livres les plus noté en fonction d'un utilisateur et des similaritées des notes des autres utilisateurs
    :param user_id:
    :return: df
    """
    books = pd.read_sql_query('SELECT * FROM Books', db.engine, )
    ratings = pd.read_sql_query('SELECT * FROM Ratings', db.engine, )

    # Count per user
    ratings_per_user = (
        ratings.groupby(by=['user_id'])['rating'].count().reset_index().rename(columns={'rating': 'rating_count'}))

    # Count per book
    ratings_per_book = (
        ratings.groupby(by=['book_id'])['rating'].count().reset_index().rename(columns={'rating': 'rating_count'}))

    new_ratings = pd.merge(ratings_per_book, ratings, left_on='book_id', right_on='book_id', how='left')

    # Creation de mapping pour les ids
    # Comme on a filtré les données, les id ne sont pas continus, mais keras fonctionne avec des id continus

    userId_map, inverse_userId_map = generate_id_mappings(new_ratings.user_id.unique())
    bookId_map, inverse_bookId_map = generate_id_mappings(new_ratings.book_id.unique())

    new_ratings['m_user_id'] = new_ratings['user_id'].map(inverse_userId_map)
    new_ratings['m_book_id'] = new_ratings['book_id'].map(inverse_bookId_map)

    liked_books = new_ratings.query('user_id ==' + str(user_id) + ' and rating == 5')['book_id']
    df = books.query('book_id in @liked_books')
    return df


def generate_id_mappings(ids_list):
    """

    :param ids_list:
    :return: userId_map, inverse_userId_map
    """
    # Dictionnaires qui vont faire coincider des identifiants qui commencent à 0 et qui sont continus, avec les identifiants qui commencent à 1 et qui ne sont pas continus
    userId_map = {new_id: old_id for new_id, old_id in enumerate(ids_list)}
    inverse_userId_map = {old_id: new_id for new_id, old_id in enumerate(ids_list)}
    return userId_map, inverse_userId_map


def filter_by_gender(df):
    """

    :param df:
    :return: l_df_gender, most_gender
    """
    tags = pd.read_sql_query('SELECT * FROM Tags', db.engine, )
    book_tags = pd.read_sql_query('SELECT * FROM Booktags', db.engine, )

    new_books_likeds = pd.merge(df, book_tags, left_on='goodreads_book_id', right_on='goodreads_book_id',
                                how='left')
    new_books_likeds_gender = pd.merge(new_books_likeds, tags, left_on='tag_id', right_on='tag_id', how='left')
    gb_tg = new_books_likeds_gender.groupby(by=['tag_name'])['book_id'].count()
    l_count = []
    for i in gb_tg:
        l_count.append(i)

    t1 = pd.DataFrame(gb_tg.index, columns=['tag_name'])
    t1['counts'] = l_count

    most_gender = t1[t1['counts'] >= 10]

    if len(most_gender) < 4:
        most_gender = t1[t1['counts'] >= 8]
    elif len(most_gender) < 2:
        most_gender = t1[t1['counts'] >= 5]

    l_df_gender = []
    for tag in most_gender['tag_name']:
        l_df_gender.append(new_books_likeds_gender[new_books_likeds_gender['tag_name'] == tag])

    return l_df_gender, most_gender


def filter_by_most_recent_gender(most_gender):
    """
    Pa rapport aux livres préféré par genre, recroiser les genres les plus notés et recupérer, via ces genres,
     sur l'ensemble des livres les plu recents.
    :param l_df_gender:
    :param most_gender:
    :return: df_final
    """
    tags = pd.read_sql_query('SELECT * FROM Tags', db.engine, )
    book_tags = pd.read_sql_query('SELECT * FROM Booktags', db.engine, )
    books = pd.read_sql_query('SELECT * FROM Books', db.engine, )

    t4 = pd.merge(tags, book_tags, left_on='tag_id', right_on='tag_id', how='left')
    t5 = pd.merge(t4, books, left_on='goodreads_book_id', right_on='goodreads_book_id', how='left')

    l_df_gender = []
    for tag in most_gender['tag_name']:
        l_df_gender.append(t5[t5['tag_name'] == tag])

    l_df_test = []
    for df in l_df_gender:
        l_df_test.append(df['original_publication_year'].sort_values(ascending=False)[:3].index)

    l_df_final = []
    for df_final in l_df_test:
        l_df_final.append(t5.iloc[df_final])
    df_final = pd.concat(l_df_final)
    return df_final


def filter_content_base_by_author(book_id):
    ratings = pd.read_sql_query('SELECT * FROM Ratings', db.engine, )
    ratings_per_book = (
        ratings.groupby(by=['book_id'])['rating'].count().reset_index().rename(columns={'rating': 'rating_count'}))

    books = pd.read_sql_query('SELECT * FROM Books', db.engine, )
    books = books[['book_id', 'goodreads_book_id', 'best_book_id', 'work_id', 'books_count', 'isbn', 'isbn13',
                   'original_publication_year', 'original_title', 'title', 'language_code', 'average_rating',
                   'ratings_count', 'work_ratings_count', 'work_text_reviews_count', 'ratings_1', 'ratings_2',
                   'ratings_3', 'ratings_4', 'ratings_5', 'image_url', 'small_image_url', 'authors']]

    new_ratings = pd.merge(ratings_per_book, ratings, left_on='book_id', right_on='book_id', how='left')

    userId_map, inverse_userId_map = generate_id_mappings(new_ratings.user_id.unique())
    bookId_map, inverse_bookId_map = generate_id_mappings(new_ratings.book_id.unique())

    new_ratings['m_user_id'] = new_ratings['user_id'].map(inverse_userId_map)
    new_ratings['m_book_id'] = new_ratings['book_id'].map(inverse_bookId_map)

    books_authors = books.join(books['authors'].str.get_dummies(","))
    books_authors["m_book_id"] = books_authors['book_id'].map(inverse_bookId_map)

    books_authors.set_index("m_book_id", inplace=True)  # Les mMovieId sont les index
    books_authors = books_authors.loc[books_authors.index.dropna()]

    cos_sim = cosine_similarity(books_authors.iloc[:, 23:])

    m_book_id = inverse_bookId_map[book_id]
    top_books = np.argsort(cos_sim[m_book_id])[-10:][::2]
    top_books_bookid = [bookId_map[x] for x in top_books]

    df_best_authors = books.query('book_id in @top_books_bookid')
    return df_best_authors


def get_by_id(book_id):
    book = pd.read_sql_query("SELECT original_title, authors, image_url FROM Books WHERE book_id={0}".format(book_id),
                             db.engine, )
    return book
