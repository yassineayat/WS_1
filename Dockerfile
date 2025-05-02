FROM python:3.10

# Installer git pour pouvoir cloner des dépôts si nécessaire
RUN apt-get update && apt-get install -y git

# Variables d'environnement pour optimiser la gestion des fichiers Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Créer un répertoire de travail dans le container
WORKDIR /WS_1

# Copier le fichier requirements.txt et installer les dépendances
COPY req_.txt .
RUN pip install --no-cache-dir -r req_.txt

# Copier tous les fichiers de l'application dans le container
COPY . .

# Commande pour démarrer Gunicorn avec le bon chemin vers le fichier wsgi.py
CMD ["gunicorn", "prjt.wsgi:application", "--bind", "0.0.0.0:8000"]
