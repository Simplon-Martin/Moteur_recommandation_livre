#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 09:36:18 2021

@author: simplon
"""


import pandas as pd
import numpy as np

# traitement tags par lemme
from nltk.stem import PorterStemmer # moins aggressif que le LancasterStemmer

import json
from sqlalchemy import create_engine

def push_df_db(l_df, engine):
    """ Push le df dans la table
    Parameters
    ----------
    l_df: liste
         liste de pd.DataFrame.
    engine : objet engine
        xpath du xml.

    Returns
    -------
    Nothing.
    """
    for i in l_df:
        # if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
        i[1].to_sql(i[0], if_exists='append', con=engine, index=False)
        print(i[0],'est poussé...')

def verify_elem(df, column_name, no_line=0):
    """ Verify the element and its len at row no_line, column_name
    Parameters
    ----------
    df: pd.DataFrame\n
    column_name: str\n
    no_line: row number\n

    Returns
    -------
    String for display.
    """
    var = df.iloc[no_line][column_name]
    return 'len='+str(len(var))+' => '+str(var)

df_to_sql = []


books = pd.read_csv('books.csv')
book_tags = pd.read_csv('book_tags.csv')
ratings = pd.read_csv('ratings.csv')
tags = pd.read_csv('tags.csv')
to_read = pd.read_csv('to_read.csv')


# transformer les isbn en str puis ajouter un 0 pour faire un nombre à 10 chiffres
books['isbn'] = books['isbn'].apply(str)
books['isbn'] = books['isbn'].apply(lambda x: '0'+x if len(x)==9 else x)
books['isbn'] = books['isbn'].apply(lambda x: '00'+x if len(x)==8 else x)
books['isbn'] = books['isbn'].apply(lambda x: '000'+x if len(x)==7 else x)

# transformer les isbn13 en str et enlever .0
books['isbn13'] = books['isbn13'].apply(str)
books['isbn13'] = books['isbn13'].apply(lambda x: x[:-2] if len(x)==15 else x)
books['isbn13'] = books['isbn13'].apply(lambda x: '0'+x[:-2] if len(x)==14 else x)
books['isbn13'] = books['isbn13'].apply(lambda x: '00'+x[:-2] if len(x)==13 else x)
# correction par élément
books.loc[8173, 'isbn13'] = '0000195170342' # set_value() deprecated use at iat


# certains livres ont isbn=nan et/ou isbn13=nan

# création d'une colonne author avec le premier membre de la liste authors
author_sep = ', '
mask = [author_sep in x for x in books['authors']]
books_multi_author = books[ mask ]
# 2079 livres ont des co-auteurs, on suppose que le premier est le principal
books['author'] = books['authors'].apply(lambda x: x[:x.find(', ')] if x.find(', ')>0 else x)


book_desc = pd.DataFrame(books.describe())
books_na = books[books.isnull()['original_publication_year']] # original_publication_year 21 nan


# Travail sur tags
porter = PorterStemmer()
# avant le lem on remplace les - par ' ' si lem strip
tags['tag_lem'] = tags['tag_name'].apply(lambda x: x.replace('-', ' ').strip())
tags['tag_lem'] = tags['tag_lem'].apply(porter.stem) # lem ne strip pas
l_amazon_book_tags = ["Children", 'Literature', 'Fiction', 'Religion', 'Spirituality',
                      'Reference', 'Health', 'Fitness', 'Dieting', 'Self-Help', 
                      'Politics', 'Social', 'Christian', 'Bibles', 'Education', 'Teaching'
                      'Arts', 'Photography', 'Humor', 'Entertainment', 'Business', 'Money'
                      'Science', 'Math', 'Teen', 'Young Adult', 'Medical', 'Crafts',
                      'Hobbies', 'Home', 'History', 'Mystery', 'Thriller', 'Suspense',
                      'Biographies', 'Memoirs', 'Comics', 'Graphic Novels', 'Romance',
                      'Science Fiction', 'Fantasy', 'Cookbooks', 'Food', 'Wine',
                      'Parenting', 'Relationships', 'Test', 'Engineering', 'Transportation',
                      'Computers', 'Technology', 'Sports', 'Outdoors', 'Travel',
                      'Law', 'LGBTQ', 'Calendars', 'Manga']
""" Amazon US book tags
Children's Books
Literature & Fiction
Religion & Spirituality
Reference
Health, Fitness & Dieting
Self-Help
Politics & Social Sciences
Christian Books & Bibles
Education & Teaching
Arts & Photography
Humor & Entertainment
Business & Money
Science & Math
Teen & Young Adult
Medical Books
Crafts, Hobbies & Home
History
Mystery, Thriller & Suspense
Biographies & Memoirs
Comics & Graphic Novels
Romance
Science Fiction & Fantasy
Cookbooks, Food & Wine
Parenting & Relationships
Test Preparation
Engineering & Transportation
Computers & Technology
Sports & Outdoors
Travel
Law
LGBTQ+ Books
Calendars 
"""
l_amazon_book_tags_stem = []
for s in l_amazon_book_tags:
    l_amazon_book_tags_stem.append(porter.stem(s)) # porter ne fonctionne pas sur liste
tags['amazon'] = tags['tag_lem'].apply(lambda x: 'amazon' if x in l_amazon_book_tags_stem else 'no')
# TODO faire une fonction avec ''.find à la place de la lambda


# Pour chaque tag unique on lui attribue un nouvel index
dict_tags = {}
l_tags_lem = (tags['tag_lem'][tags['amazon']=='amazon']).unique()
new_index = 0
for t in l_tags_lem:
    new_index += 1
    dict_tags[t] = new_index # initialise le dico de tags
tags['tag_name'] = tags['tag_lem']
tags['tag_name'].replace(dict(zip(l_amazon_book_tags_stem, l_amazon_book_tags)), inplace=True)
# on applique le dict aux valeurs de tag_lem
tags['tag_lem'].replace(dict_tags, inplace=True)
tags = tags[tags['amazon']=='amazon'] # on enlève les tags qui ne sont pas reconnus


dict_tags = {}
l_tag_id = tags['tag_id'].tolist()
l_tag_id_new = tags['tag_lem'].tolist()
for index in range(len(l_tag_id)):
    dict_tags[l_tag_id[index]] = l_tag_id_new[index]
book_tags['new_tag_id'] = book_tags['tag_id'].apply(lambda x: x if x in l_tag_id else np.nan)
book_tags['new_tag_id'].replace(dict_tags, inplace=True)
book_tags.dropna(inplace=True)
book_tags['tag_id'] = book_tags['new_tag_id']
book_tags = book_tags.groupby(['goodreads_book_id','tag_id'])['count'].sum().reset_index()

# Clean tags pour avoir que le nouvel index et les name d'Amazon
tags = tags[['tag_lem', 'tag_name']].drop_duplicates()
# puis renommer la colonne
tags.rename(columns={'tag_lem':'tag_id'}, inplace=True)


# on ajoute les df à la liste avec la base associée
df_to_sql.append(("books", books)) # books.iloc[:200] 200 premières lignes
df_to_sql.append(("booktags", book_tags))
df_to_sql.append(("ratings", ratings))
df_to_sql.append(("tags", tags))
df_to_sql.append(("toread", to_read))


# push des df dans la BD
import_datas_DB = True
if import_datas_DB:
    with open('con.json') as json_data:
        data_dict = json.load(json_data)
        engine = create_engine(data_dict['sgbd']+"://"+data_dict['user']+":"+data_dict['pwd']+"@"+data_dict['base'])
        push_df_db(df_to_sql, engine)
        print('=== FIN de PUSH ===')
else:
    print("=== Don't want to import datas ===")

# title  original_title author authors vérifier la longueur des champs
# print(verify_elem(books, 'authors', 5000+1200))
