#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 09:36:18 2021

@author: simplon
"""


import pandas as pd
import numpy as np

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
        print(i,'est poussé...')

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


# on ajoute les df à la liste avec la base associée
df_to_sql.append(("books", books)) # books.iloc[:200] 200 premières lignes
df_to_sql.append(("booktags", book_tags))
df_to_sql.append(("ratings", ratings))
df_to_sql.append(("tags", tags))
df_to_sql.append(("toread", to_read))


# push des df dans la BD
with open('con.json') as json_data:
    data_dict = json.load(json_data)
    engine = create_engine(data_dict['sgbd']+"://"+data_dict['user']+":"+data_dict['pwd']+"@"+data_dict['base'])
    push_df_db(df_to_sql, engine)
    print('FIN de PUSH')

# title  original_title author authors vérifier la longueur des champs
# print(verify_elem(books, 'authors', 5000+1200))
