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

# création du planning type
planning_reel = [
    # --- LUNDI ---
    (0, '09:00', 45, 'Pilates Intermédiaire'),
    (0, '09:45', 45, 'Pilates Fondamental'),
    (0, '10:45', 45, 'Pilates Fondamental'),
    (0, '12:30', 45, 'Pilates Intermédiaire'),
    (0, '18:30', 45, 'Pilates Intermédiaire'),
    (0, '19:15', 45, 'Pilates Fondamental'),
    (0, '20:00', 45, 'Pilates Intermédiaire'),

    # --- MARDI (Les 2 derniers du mercredi décalés ici) ---
    (1, '19:15', 45, 'Pilates Intermédiaire'),
    (1, '20:00', 45, 'Pilates Avancé'),

    # --- MERCREDI ---
    (2, '09:00', 45, 'Pilates Intermédiaire'),
    (2, '10:00', 60, 'Yoga Doux'), # Attention durée 1h
    (2, '12:30', 45, 'Pilates Fondamental'),
    (2, '18:30', 45, 'Pilates Fondamental'),
    # Les créneaux de 19:15 et 20:00 ont été déplacés au Mardi comme demandé

    # --- JEUDI ---
    (3, '09:30', 45, 'Pilates Fondamental'),
    (3, '10:30', 60, 'Mobilité et respiration'), # Durée 1h
    (3, '18:30', 45, 'Pilates Intermédiaire'),
    (3, '19:15', 45, 'Pilates Fondamental'),
    (3, '20:00', 45, 'Pilates Intermédiaire')
]

for seance in planning_reel:
    curseur.execute("""
        INSERT INTO semaine_type (jour_semaine, heure_debut, duree, type_seance) 
        VALUES (?, ?, ?, ?)
    """, seance)

print(f"{len(planning_reel)} créneaux types ajoutés au planning.")

# validation des changements et fermeture
connection.commit()
connection.close()

print("Connexion à la base de données fermée.")
print("Fin du programme.")