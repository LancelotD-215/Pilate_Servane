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
import csv

# création du planning
planning_reel = [
    # --- LUNDI ---
    (0, '09:00', 45, 'Pilates Intermédiaire'),
    (0, '09:45', 45, 'Pilates Fondamental'),
    (0, '10:45', 45, 'Pilates Fondamental'),
    (0, '12:30', 45, 'Pilates Intermédiaire'),
    (0, '18:30', 45, 'Pilates Intermédiaire'),
    (0, '19:15', 45, 'Pilates Fondamental'),
    (0, '20:00', 45, 'Pilates Intermédiaire'),

    # --- MARDI ---
    (1, '18:30', 45, 'Pilates Fondamental'),
    (1, '19:30', 45, 'Pilates Intermédiaire'),
    

    # --- MERCREDI ---
    (2, '09:00', 45, 'Pilates Intermédiaire'),
    (2, '10:00', 60, 'Yoga Doux'), # Attention durée 1h
    (2, '12:30', 45, 'Pilates Fondamental'),
    (2, '18:30', 45, 'Pilates Fondamental'),
    (2, '19:15', 45, 'Pilates Intermédiaire'),
    (2, '20:00', 45, 'Pilates Avancé'),

    # --- JEUDI ---
    (3, '09:30', 45, 'Pilates Fondamental'),
    (3, '10:30', 60, 'Mobilité et respiration'), # Durée 1h    
]

def init_db(csv_path):
    print("Initialisation de la base de données à partir du fichier CSV")

    # Connection a la base de données
    connection = sqlite3.connect('database_clients.db')
    
    # Permet d'accéder aux résultats des requêtes sous forme de dictionnaires
    connection.row_factory = sqlite3.Row

    # création des tables à partir du fichier SQL
    with open('schema.sql', 'r', encoding='utf-8') as f:
        connection.executescript(f.read())
    print("Tables créées avec succès.")

    # insertion des créneaux types dans la table semaine_type
    for seance in planning_reel:
        connection.execute("""
            INSERT INTO semaine_type (jour_semaine, heure_debut, duree, type_seance) 
            VALUES (?, ?, ?, ?)
        """, seance)

    print(f"{len(planning_reel)} créneaux types ajoutés au planning.")

    # dictionnaire des jours 
    jours_map = {'Lundi': 0, 'Mardi': 1, 'Mercredi': 2, 'Jeudi': 3, 'Vendredi': 4, 'Samedi': 5, 'Dimanche': 6}

    # lecture du fichier CSV
    with open(csv_path, mode='r', encoding='latin-1') as f:
        reader = csv.reader(f, delimiter=';')

        for row in reader:
            # Ignorer les lignes vides ou celles dont la première colonne est vide
            if not row or not row[0].strip():
                continue

            # Nettoyage du nom pour retirer les caractères parasites éventuels
            nom_brut = row[0].strip()
            # On retire les caractères parasites du début s'ils sont présents
            nom_nettoye = nom_brut.encode('latin-1', errors='ignore').decode('utf-8-sig', errors='ignore')
            if not nom_nettoye: # Si la conversion échoue, on garde le brut sans les 3 premiers caractères
                nom_nettoye = nom_brut.replace('ï»¿', '').replace('Ï»¿', '')

            # Récupération et nettoyage des données
            nom = nom_nettoye.title()
            prenom = row[1].strip().title()
            solde = int(row[2].strip() if row[2].strip() else 0) # On utilise 0 par défaut si la case est vide
            telephone = row[3].strip() if row[3] else None
            email = row[4].strip() if row[4] else None

            # insertion dans la base de données
            cursor = connection.execute('''
                    INSERT INTO clients (prenom, nom, seances_restantes, telephone, email)
                    VALUES (?, ?, ?, ?, ?)
                ''', (prenom, nom, solde, telephone, email))
            
            client_id = cursor.lastrowid # Récupère l'ID du client inséré
            print(f"Client ajouté : {prenom} {nom} (ID: {client_id})")

            # insertion dans l'historique des séances
            connection.execute('''
                    INSERT INTO historique_seances (client_id, action, nombre, date_heure)
                    VALUES (?, ?, ?, ?)
                ''', (client_id, 'IMPORT_INITIAL', solde, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            for i in [5, 6, 7]:
                if i < len(row) and row[i].strip():
                    valeur_cours = row[i].strip()
                    # Format attendu : "Jour HH:MM" (ex: "Lundi 10:00")
                    parts = valeur_cours.split(' ')
                    
                    if len(parts) >= 2:
                        j_nom = parts[0].capitalize()
                        h_raw = parts[1].upper().replace('H', ':') # Gère "10h30" ou "10:30"
                        
                        if ':' in h_raw:
                            h_parts = h_raw.split(':')
                            if len(h_parts[0]) == 1:
                                h_parts[0] = '0' + h_parts[0]
                            h_debut = f"{h_parts[0]}:{h_parts[1]}"
                        else:
                            h_debut = h_raw

                        # Recherche du créneau existant dans 'semaine_type'
                        creneau = connection.execute('''
                            SELECT id FROM semaine_type 
                            WHERE jour_semaine = ? AND heure_debut = ?
                        ''', (jours_map.get(j_nom), h_debut)).fetchone()
                        
                        if creneau:
                            connection.execute('''
                                INSERT INTO habitudes (client_id, creneau_id) 
                                VALUES (?, ?)
                            ''', (client_id, creneau['id']))

    # validation des changements et fermeture
    connection.commit()
    connection.close()

    print("Connexion à la base de données fermée.")



print("Fin du programme.")

if __name__ == '__main__':
    # Vérifie bien que le nom du fichier est correct
    init_db(r'data\liste_clients_fevrier.csv')