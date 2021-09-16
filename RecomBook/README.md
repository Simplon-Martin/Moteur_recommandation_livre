# Moteur_recommandation_livre
Développer un moteur de recommandation de livre, à partir d'une base de données d'avis d'utilisateurs.

## Installation

Suivre les indications ci-dessous :

```bash
git clone https://github.com/Simplon-Martin/Moteur_recommandation_livre
cd cd RecomBook/
```

Sous Windows : 

```bash
python -m venv venv
```

Sous Linux : 

```bash
source venv/bin/activate
```

Ensuite : 

```bash
pip install -r requirements.txt
```

## Configuration

Configuration
Ouvrir le fichier exemple_config.yml et remplacer les valeurs par défaut par celle de votre environnement. Copier ensuite ce fichier dans un dossier instance et le renommer config.yml.

```bash
mkdir instance
cp exemple_config.yml instance/config.yml
```

```bash
flask db upgrade
flask insert-db
```

Créer un utilisateur
Afin d'utiliser l'app, vous allez devoir vous connecter avec un utilisateur. Pour le créer :

```bash
flask create-user
```

Exécution
Pour lancer l'app, vous devrez taper la commande :

```bash
FLASK_APP=app.py FLASK_ENV=development flask run --port 8080
```


## Contribution
Mohamad, Remi, Martin

## License

