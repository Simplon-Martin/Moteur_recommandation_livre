import pandas as pd
import numpy as np
from datetime import datetime

# netoyage des données :::
def format_data_caracteristiques(caracteristiques: pd.DataFrame):

    caracteristiques["atm"] = caracteristiques["atm"].apply(
        lambda x: pd.NA if x == -1 else x
    )
    caracteristiques["col"] = caracteristiques["col"].apply(
        lambda x: pd.NA if x == -1 else x
    )
    caracteristiques["date"] = caracteristiques.apply(
        lambda line: datetime(
            line["an"],
            line["mois"],
            line["jour"],
            int(line["hrmn"].split(":")[0]),
            int(line["hrmn"].split(":")[1]),
        ),
        axis=1,
    )

    caracteristiques = caracteristiques.rename(
        columns={
            "Num_Acc": "Num_Acc_id",
            "date": "Date_Acc",
            "lum": "Lumiere_Acc",
            "dep": "Departement_Acc",
            "com": "Commune_Acc",
            "agg": "Agglomeration_Acc",
            "int": "Intersection_Acc",
            "atm": "Meteo_Acc",
            "col": "Collision_Acc",
            "adr": "Addresse_Acc",
            "lat": "Latitude_Acc",
            "long": "Longitude_Acc",
        }
    )

    caracteristiques = caracteristiques.drop(columns={"jour", "mois", "an", "hrmn"})

    return caracteristiques