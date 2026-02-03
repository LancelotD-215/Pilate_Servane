# -*- coding: utf-8 -*-
"""
author: @lancelot
name : app.py
description : code principal de l'application Flask pour la gestion des clients de Pilates
date : 2026/01/20
"""

# imports des modules
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from app_lib import get_db_connection, get_best_clients, get_client_most_remaining, get_number_seances, get_negative_seances_clients

# création de l'application Flask
app = Flask(__name__) # création du site web




# création des routes pour le site web (pages)
@app.route('/')
def index():
    """
    Fonction exécutée lors de l'accès à la page d'accueil ('/').
    Args:
        None
    Returns:
        str: rendu HTML de la page d'accueil.
    """
    # connexion à la base de données
    connection = get_db_connection()

    # CONFIGURATION DES WIDGETS
    widgets_config = {
        'negative_balance': True,
        'best_client_month': True,
        'best_client_all_time': False,
        'most_remaining': True,
        'total_clients': True,
        'seances_month': True
    }

    # initialisation des données des widgets
    negative_clients = []
    best_clients_month = None
    best_clients_all_time = None
    client_most_remaining = None
    total_clients = None
    number_seances_month = None

    # récupération des variables
    actual_date = datetime.now().strftime('%Y-%m-%d')
    first_day_of_month = actual_date[:8] + '01' # premier jour du mois courant

    # création des données pour les widgets
    if widgets_config['negative_balance']:
        negative_clients = get_negative_seances_clients()
    if widgets_config['best_client_month']:
        best_clients_month = get_best_clients(first_day_of_month, actual_date) # du mois courant
    if widgets_config['best_client_all_time']:
        best_clients_all_time = get_best_clients('2000-01-01', actual_date) # depuis le début
    if widgets_config['most_remaining']:
        client_most_remaining = get_client_most_remaining()
    if widgets_config['total_clients']:
        total_clients = connection.execute('SELECT COUNT(*) AS total FROM clients').fetchone()['total']
    if widgets_config['seances_month']:
        number_seances_month = get_number_seances(first_day_of_month, actual_date) # du mois courant


    # fermeture de la connexion à la base de données
    connection.close()

    # envoi des données à la page HTML index.html
    return render_template('index.html', 
                           widgets=widgets_config,
                           negative_clients=negative_clients,
                           best_clients_month=best_clients_month,  
                           client_most_remaining=client_most_remaining, 
                           total_clients=total_clients, 
                           number_seances_month=number_seances_month)


@app.route('/gestion_clients')
def gestion_clients():
    """
    Fonction exécutée lors de l'accès à la page gestion_clients ('/gestion_clients').
    Args:
        None
    Returns:
        str: rendu HTML de la page gestion_clients.
    """
    # connexion à la base de données
    connection = get_db_connection()

    # requête SQL pour récupérer tous les clients de la table 'clients'
    clients = connection.execute('SELECT * FROM clients').fetchall()

    # fermeture de la connexion à la base de données
    connection.close()

    # envoi des données à la page HTML gestion_clients.html
    return render_template('gestion_clients.html', clients=clients)




@app.route('/presence', methods=['GET', 'POST']) # pour accepter les requêtes GET et POST
def presence():
    """
    Fonction exécutée lors de l'accès à la page '/presence'.
    Args:
        None
    Returns:
        str: rendu HTML de la page de présence.
    """
    # connexion à la base de données
    connection = get_db_connection()

    if request.method == "POST": # si l'utilisateur a soumis le formulaire (POST)
        # récupération de l'ID du client depuis le formulaire
        prenom = request.form['prenom']
        nom = request.form['nom']

        # nettoyage des entrées
        prenom = prenom.strip().title()
        nom = nom.strip().title() 

        # recherche du client dans la base de données
        client = connection.execute('SELECT * FROM clients WHERE prenom = ? AND nom = ?', (prenom, nom)).fetchone()
        
        if client:
            # récupération de l'ID du client
            client_id = client['id']

            # mise à jour de la présence du client dans la base de données
            connection.execute('UPDATE clients SET seances_restantes = seances_restantes - 1 WHERE id = ?', (client_id,))

            # ajout dans historique seances
            connection.execute('INSERT INTO historique_seances (client_id, action, nombre) VALUES (?, ?, ?)', (client_id, "CHECK-IN", -1))

            # commit des changements
            connection.commit() 
            connection.close()

            # renvoie l'utilisateur vers l'accueil
            return redirect(url_for('index'))
        
        else:
            # client non trouvé
            connection.close()
            return (f"<h1>Erreur : Le client '{prenom} {nom}' est introuvable.</h1><p>Vérifiez l'orthographe et réessayez.</p><a href='/presence'>Réessayer</a>")

    if request.method == "GET" :
        # affichage de la liste des clients
        clients = connection.execute('SELECT * FROM clients').fetchall()
        connection.close()
        return render_template('presence.html', clients=clients)




@app.route('/ajout_client', methods=['GET', 'POST'])
def ajout_client():
    """
    Fonction exécutée lors de l'accès à la page '/ajout_client'.
    Args:
        None
    Returns:
        str: rendu HTML de la page d'ajout de client.
    """
    # connexion à la base de données
    connection = get_db_connection()
    
    if request.method == "POST": # si l'utilisateur a soumis le formulaire (POST)
        # récupération des données du formulaire
        prenom = request.form['prenom'].strip().title()
        nom = request.form['nom'].strip().title() 
        seances_initiales = int(request.form['seances_initiales'])

        email = request.form.get('email') # .get pour champ optionnel
        telephone = request.form.get('telephone')

        abonnement = 1 if request.form.get('abonnement') else 0

        # vérification si le client existe déjà
        existing_client = connection.execute('SELECT * FROM clients WHERE prenom = ? AND nom = ?', (prenom, nom)).fetchone()

        if existing_client:
            connection.close()
            return (f"<h1>Erreur : Le client '{prenom} {nom}' existe déjà.</h1><p>Veuillez vérifier les informations et réessayer.</p><a href='/ajout_client'>Réessayer</a>")
        
        else:
            # curseur pour récupérer l'ID du nouveau client
            curseur = connection.execute('INSERT INTO clients (prenom, nom, seances_restantes, email, telephone, abonnement) VALUES (?, ?, ?, ?, ?, ?)',(prenom, nom, seances_initiales, email, telephone, abonnement))
            
            # récupération de l'ID du nouveau client
            nouveau_client_id = curseur.lastrowid

            # ajout dans historique seances
            connection.execute('INSERT INTO historique_seances (client_id, action, nombre) VALUES (?, ?, ?)',(nouveau_client_id, 'NEW_ACCOUNT', seances_initiales))

            # commit des changements
            connection.commit() 
            connection.close()

            # renvoie de l'utilisateur vers l'accueil
            return redirect(url_for('index'))

    if request.method == "GET" :
        connection.close()
        # affichage du formulaire d'ajout de client
        return render_template('ajout_client.html')




@app.route('/ajout_seances', methods=['GET', 'POST'])
def ajout_seances():
    """
    Fonction exécutée lors de l'accès à la page '/ajout_seances'.
    Args:
        None
    Returns:
        str: rendu HTML de la page d'ajout de séances.
    """
    # connexion à la base de données
    connection = get_db_connection()
    
    if request.method == "POST":
        # récupération des données du formulaire
        prenom = request.form['prenom'].strip().title()
        nom = request.form['nom'].strip().title() 
        seances_ajoutees = int(request.form['seances_ajoutees'])

        # recherche du client dans la base de données
        client = connection.execute('SELECT * FROM clients WHERE prenom = ? AND nom = ?', (prenom, nom)).fetchone()

        if client:
            client_id = client['id']

            # mise à jour du nombre de séances restantes pour le client
            connection.execute('UPDATE clients SET seances_restantes = seances_restantes + ? WHERE id = ?', (seances_ajoutees, client_id))

            # ajout dans historique seances
            connection.execute('INSERT INTO historique_seances (client_id, action, nombre) VALUES (?, ?, ?)', (client_id, "ADD_SEANCES", seances_ajoutees))

            # commit des changements
            connection.commit() 
            connection.close()

            # renvoie l'utilisateur vers l'accueil
            return redirect(url_for('index'))

    if request.method == "GET" :
        # affichage de la liste des clients
        clients = connection.execute('SELECT * FROM clients').fetchall()
        connection.close()
        return render_template('ajout_seances.html', clients=clients)



@app.route('/ajout_seances_rapide', methods=['POST'])
def ajout_seances_rapide():
    """
    Fonction exécutée lors de l'accès à la page '/ajout_seances_rapide'.
    Args:
        None
    Returns:
        str: redirection vers la page de gestion des clients.
    """
    # connexion à la base de données
    connection = get_db_connection()
    
    if request.method == "POST":
        # récupération des données du formulaire
        client_id = int(request.form['client_id'])
        seances_ajoutees = int(request.form['seances_ajoutees'])

        # mise à jour du nombre de séances restantes pour le client
        connection.execute('UPDATE clients SET seances_restantes = seances_restantes + ? WHERE id = ?', (seances_ajoutees, client_id))

        # ajout dans historique seances
        connection.execute('INSERT INTO historique_seances (client_id, action, nombre) VALUES (?, ?, ?)', (client_id, "ADD_SEANCES", seances_ajoutees))

        # récupération de l'origine de la requête
        origine = request.form.get('origine')

        # commit des changements
        connection.commit() 
        connection.close()

        # renvoie l'utilisateur vers la page de gestion des clients
        # selon l'origine du formulaire
        if origine == 'index':
            # Si le formulaire contenait <input name="origine" value="index">
            return redirect(url_for('index'))
        else:
            # Sinon (comportement par défaut pour la page gestion_clients)
            return redirect(url_for('gestion_clients'))



@app.route('/recherche_client', methods=['GET'])
def recherche_client():
    """
    Fonction exécutée lors de l'accès à la page '/recherche_client'.
    Args:
        None
    Returns:
        str: rendu HTML de la page de résultats de recherche de client.
    """
    # récupération du terme de recherche depuis les paramètres GET
    query = request.args.get('q', '').strip().title()

    # découpage en prénom et nom
    parts = query.split(' ')

    # suppose que le format est "Prénom Nom"
    prenom_recherche = parts[0].title()
    nom_recherche = parts[1].title()

    # connexion à la base de données
    connection = get_db_connection()

    # recherche des clients correspondant au terme de recherche
    client = connection.execute('SELECT id FROM clients WHERE prenom = ? AND nom = ?', (prenom_recherche, nom_recherche)).fetchone()

    # fermeture de la connexion à la base de données
    connection.close()

    # envoi des résultats à la page HTML recherche_client.html
    return redirect(url_for('fiche_client', client_id=client['id']))



@app.route('/client/<int:client_id>')
def fiche_client(client_id):
    """
    Fonction exécutée lors de l'accès à la page '/client/<client_id>'.
    Args:
        client_id (int): ID du client à afficher.
    Returns:
        str: rendu HTML de la fiche du client.
    """
    # connexion à la base de données
    connection = get_db_connection()

    # récupération des informations du client
    client = connection.execute('SELECT * FROM clients WHERE id = ?', (client_id,)).fetchone()

    # récupération des habitudes du client
    habitudes = connection.execute('''
        SELECT s.jour_semaine, s.heure_debut, s.type_seance 
        FROM habitudes h
        JOIN semaine_type s ON h.creneau_id = s.id
        WHERE h.client_id = ?
    ''', (client_id,)).fetchall()

    # récupération de l'historique des séances du client (10 dernières actions)
    historique = connection.execute('''
        SELECT date_heure, action, nombre 
        FROM historique_seances 
        WHERE client_id = ? 
        ORDER BY date_heure DESC 
        LIMIT 10
    ''', (client_id,)).fetchall()

    # fermeture de la connexion à la base de données
    connection.close()

    # pour affichage des jours
    jours_semaine = {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi', 5: 'Samedi', 6: 'Dimanche'}

    # envoi des données à la page HTML fiche_client.html
    return render_template('fiche_client.html', 
                           client=client, 
                           habitudes=habitudes, 
                           historique=historique,
                           jours=jours_semaine)



@app.route('/planning')
def planning():
    """
    Fonction exécutée lors de l'accès à la page '/planning'.
    Args:
        None
    Returns:
        str: rendu HTML de la page de planning.
    """
    # récupération du paramètre 'semaine' pour décaler l'affichage du planning
    try:
        offset = int(request.args.get('semaine', 0))
    except ValueError:
        offset = 0

    # calcul des dates de début et fin de la semaine affichée
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=offset)
    end_of_week = start_of_week + timedelta(days=6)
    start_date_str = start_of_week.strftime('%Y-%m-%d')
    end_date_str = end_of_week.strftime('%Y-%m-%d')

    # récupération du squellette du planning
    connection = get_db_connection()
    planning_squelett = connection.execute('SELECT * FROM semaine_type').fetchall()
    connection.close()

    # construction du planning hebdomadaire
    semaine_fr = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    semaine_data = []

    for i in range(7):
        jour_date = start_of_week + timedelta(days=i)

        creneaux_jour = []
        for creneau in planning_squelett:
            if creneau['jour_semaine'] == i:
                creneaux_jour.append(creneau)
        semaine_data.append({
            'jour_nom': semaine_fr[i],
            'date': jour_date.strftime('%Y-%m-%d'),
            'creneaux': creneaux_jour
        })
        
    # envoi des données à la page HTML planning.html
    return render_template('planning.html',
                            semaine=semaine_data,
                            start_date=start_date_str,
                            end_date=end_date_str,
                            offset=offset)


# lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)