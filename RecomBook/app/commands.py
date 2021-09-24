import click
import pandas as pd
from flask.cli import with_appcontext
from consolemenu import SelectionMenu
from app.db import db
from app.models import Books, Booktags, Tags, Toread, Ratings
from app.helpers import (
    format_data_caracteristiques,
    # format_data_lieux,
    # format_data_usagers,
    # format_data_vehicules,
)


@click.command("insert-db")
@with_appcontext
def insert_db():
    """Insère les données nécessaire à l'utilisation de l'application"""


    """
     # On récupère les données du fichier CSV dans un dataframe
    caracteristiques = pd.read_csv(
        "data/caracteristiques.csv", delimiter=";", decimal=","
    )
    lieux = pd.read_csv("data/lieux.csv", delimiter=";", decimal=",")
    usagers = pd.read_csv("data/usagers.csv", delimiter=";", decimal=",")
    vehicules = pd.read_csv("data/vehicules.csv", delimiter=";", decimal=",")
    # On format les données (int64 pour les champs) afin de les préparer à l'insertion
    caracteristiques = format_data_caracteristiques(caracteristiques)
    lieux = format_data_lieux(lieux)
    vehicules = format_data_vehicules(vehicules)
    usagers = format_data_usagers(usagers)
    # On insère les données dans la table
    Caracteristique.insert_from_pd(caracteristiques)
    Lieux.insert_from_pd(lieux)
    Vehicule.insert_from_pd(vehicules)
    Usager.insert_from_pd(usagers)
    print("Données dans la BDD insérées")

    # On crée les roles Admin et Membre avec des permissions différentes
    roles = [
        UserRole(
            name="Admin",
            permissions=[
                "admin.read",
                "admin.write",
                "admin.update",
                "user.read",
                "user.write",
                "user.update",
            ],
        ),
        UserRole(name="Membre", permissions=["user.read"]),
    ]
    # On ajoute chaque rôle à la BDD
    for role in roles:
        db.session.add(role)
    print("Roles ajoutées")

    # On confirme tous les changements pour la transaction
    db.session.commit()
    print("Tout a été inséré dans la base de données !")
    """
