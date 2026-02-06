# -*- coding: utf-8 -*-
"""
author: @lancelot
name :  app_lib.py
description : bibliothèque de fonctions pour l'application Flask de gestion des clients de Pilates
date : 2026/01/21
"""


# imports des modules
import sqlite3
from datetime import datetime, timedelta


# création des fonctions utilitaires
def get_db_connection():
    """
    Fonction de connexion à la base de données.
    Appelée à chaque requête pour lire ou écrire des données.
    Args:j
        None
    Returns:
        sqlite3.Connection: lien de connexion à la base de données.
    """
    # connection à la base de données
    connection = sqlite3.connect('database_clients_test.db')

    # pour accéder aux colonnes par nom et non par index
    connection.row_factory = sqlite3.Row
    return connection



def get_best_clients(since_date, until_date):
    """
    Fonction pour récupérer le meilleur client depuis une date donnée. (celui qui a utilisé le plus de séances)
    Args:
        since_date (str): date au format 'YYYY-MM-DD' pour filtrer le début des actions.
        until_date (str): date au format 'YYYY-MM-DD' pour filtrer la fin des actions.
    Returns:
        list: liste des clients avec le nombre de séances utilisées.
    """
    connection = get_db_connection()

    query = """
        SELECT c.prenom, c.nom, COUNT(h.id) AS seances_utilisees
        FROM historique_seances h
        JOIN clients c ON h.client_id = c.id
        WHERE h.action = 'CHECK-IN' 
        AND DATE(h.date_heure) BETWEEN ? AND ?
        GROUP BY c.id
        ORDER BY seances_utilisees DESC
        LIMIT 1;  
    """

    result = connection.execute(query, (since_date, until_date)).fetchone()
    connection.close()
    return result




def get_client_most_remaining():
    """
    Fonction pour récupérer le client avec le plus de séances restantes.
    Args:
        None
    Returns:
        sqlite3.Row: ligne contenant les informations du client.
    """
    connection = get_db_connection()

    query = """
        SELECT prenom, nom, seances_restantes
        FROM clients
        ORDER BY seances_restantes DESC
        LIMIT 1;
    """

    result = connection.execute(query).fetchone()
    connection.close()
    return result




def get_number_seances(since_date, until_date):
    """
    Fonction pour récupérer le nombre total de séances donnée par le prof depuis une date donnée.
    Compte les créneaux de semaine_type qui ont eu au moins un CHECK-IN.
    Args:
        since_date (str): date au format 'YYYY-MM-DD' pour filtrer le début des actions.
        until_date (str): date au format 'YYYY-MM-DD' pour filtrer la fin des actions.
    Returns:
        int: nombre total de séances données.
    """
    connection = get_db_connection()

    # Récupérer tous les CHECK-IN dans la période avec date/heure détaillée
    query_checkins = """
        SELECT date_heure
        FROM historique_seances
        WHERE action = 'CHECK-IN'
        AND DATE(date_heure) BETWEEN ? AND ?
    """
    
    checkins = connection.execute(query_checkins, (since_date, until_date)).fetchall()
    
    if not checkins:
        connection.close()
        return 0

    # Récupérer tous les créneaux actifs
    query_creneaux = """
        SELECT id, jour_semaine, heure_debut, duree
        FROM semaine_type
        WHERE actif = 1
    """
    
    creneaux = connection.execute(query_creneaux).fetchall()
    connection.close()

    # Set pour éviter les doublons de créneaux
    seances_donnees = set()
    
    for checkin in checkins:
        # Convertir le CHECK-IN en datetime Python
        date_str = checkin['date_heure'].replace('T', ' ')  # Gérer le format ISO avec T
        checkin_dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        jour_semaine = checkin_dt.weekday()  # 0=lundi, 1=mardi, etc.
        heure_checkin = checkin_dt.time()
        
        # Trouver le créneau correspondant
        for creneau in creneaux:
            if creneau['jour_semaine'] == jour_semaine:
                # Parser l'heure de début du créneau
                heure_debut = datetime.strptime(creneau['heure_debut'], '%H:%M').time()
                
                # Calculer l'heure de fin (début + durée)
                debut_dt = datetime.combine(checkin_dt.date(), heure_debut)
                fin_dt = debut_dt + timedelta(minutes=creneau['duree'])
                heure_fin = fin_dt.time()
                
                # Vérifier si le CHECK-IN est dans cette plage horaire
                if heure_debut <= heure_checkin <= heure_fin:
                    seances_donnees.add(creneau['id'])
                    break  # On a trouvé le bon créneau, pas besoin de chercher plus
    
    return len(seances_donnees)


def get_negative_seances_clients():
    """
    Fonction pour récupérer la liste des clients avec un solde négatif de séances.
    Args:
        None
    Returns:
        list: liste des clients avec un solde négatif de séances.
    """
    connection = get_db_connection()

    query = """
        SELECT id, prenom, nom, seances_restantes
        FROM clients
        WHERE seances_restantes < 0
        ORDER BY seances_restantes ASC
    """

    results = connection.execute(query).fetchall()
    connection.close()
    return results


def get_zero_clients():
    """
    Fonction pour récupérer la liste des clients avec un solde de séances à zéro.
    Args:
        None
    Returns:
        list: liste des clients avec un solde de séances à zéro.
    """
    connection = get_db_connection()

    query = """
        SELECT id, prenom, nom, seances_restantes
        FROM clients
        WHERE seances_restantes = 0
        ORDER BY nom ASC, prenom ASC
    """

    results = connection.execute(query).fetchall()
    connection.close()
    return results