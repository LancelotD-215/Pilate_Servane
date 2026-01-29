# -*- coding: utf-8 -*-
"""
author: @lancelot
name : init_bdd.py
description : code d'initialisation de la base de données
date : 2026/01/20
"""

print("Début du programme.")

# import des modules
import sqlite3 # pour gérer la bdd SQLite
from datetime import datetime, timedelta

# connexion à la base de données (ou création si elle n'existe pas)
connection = sqlite3.connect('database_clients.db') # connexion à la bdd
print("Base de données connectée avec succès.")

# execution du shema de la base de données
with open('schema.sql') as f:
    connection.executescript(f.read()) # exécution du script SQL
print("Schéma de la base de données créé avec succès.")

# création d'un curseur
curseur = connection.cursor() # création d'un curseur (stylo pour écrire) pour exécuter des commandes SQL

# du planning type
planning_type = [
    # Exemple : Lundi à 18h00, cours collectif
    (0, '18:00', 60, 'Collectif'),
    
    # Exemple : Jeudi à 18h30, cours collectif
    (3, '18:30', 60, 'Collectif'),
    
    # Ajoute les autres lignes ici...
]

for seance in planning_type:
    curseur.execute("""
        INSERT INTO semaine_type (jour_semaine, heure_debut, duree, type_seance) 
        VALUES (?, ?, ?, ?)
    """, seance)

print(f"{len(planning_type)} créneaux types ajoutés au planning.")

# validation des changements et fermeture
connection.commit()
connection.close()

print("Connexion à la base de données fermée.")
print("Fin du programme.")