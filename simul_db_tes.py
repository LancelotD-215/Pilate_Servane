import sqlite3
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
DB_NAME = 'database_clients_test.db'
NB_CLIENTS = 100
DATE_DEBUT = datetime(2025, 1, 1)
DATE_FIN = datetime.now() # Date d'aujourd'hui simulée


# Listes pour générer des données aléatoires
PRENOMS = [
    "Emma", "Gabriel", "Léo", "Louise", "Raphaël", "Jade", "Louis", "Ambre", "Lucas", "Arthur",
    "Alice", "Jules", "Maël", "Liam", "Lina", "Adam", "Chloé", "Sacha", "Mia", "Hugo",
    "Noah", "Tiago", "Rose", "Anna", "Mila", "Lancelot", "Merlin", "Guenièvre", "Perceval", "Karadoc"
]

NOMS = [
    "Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois", "Moreau", "Laurent",
    "Simon", "Michel", "Lefebvre", "Leroy", "Roux", "David", "Bertrand", "Morel", "Fournier", "Girard",
    "Bonnet", "Dupont", "Lambert", "Fontaine", "Rousseau", "Vincent", "Muller", "Lefevre", "Faure", "Andre"
]

DOMAINES = ["gmail.com", "yahoo.fr", "hotmail.com", "orange.fr", "outlook.com"]


# fonctions utilitaires
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def generer_date_random(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generer_telephone():
    return f"06{random.randint(10, 99)}{random.randint(10, 99)}{random.randint(10, 99)}{random.randint(10, 99)}"

def generer_email(prenom, nom):
    return f"{prenom.lower()}.{nom.lower()}@{random.choice(DOMAINES)}"


# fonction principale de génération de données
def main():
    print(f"🚀 Démarrage de la simulation corrigée sur {DB_NAME}...")
    conn = get_db_connection()
    
    # 1. INIT DU SCHÉMA
    print("🧹 Réinitialisation de la structure...")
    with open('schema.sql') as f:
        conn.executescript(f.read())
    
    # 2. GÉNÉRATION DU PLANNING TYPE
    print("📅 Création de la semaine type...")
    planning_reel = [
        (0, '18:00', 60, 'Collectif'), 
        (1, '10:00', 60, 'Solo'),      
        (1, '18:00', 60, 'Collectif'), 
        (3, '18:30', 60, 'Collectif'), 
        (5, '10:00', 60, 'Duo')        
    ]
    for creneau in planning_reel:
        conn.execute("INSERT INTO semaine_type (jour_semaine, heure_debut, duree, type_seance) VALUES (?, ?, ?, ?)", creneau)

    # 3. GÉNÉRATION DES CLIENTS
    print(f"👥 Génération de {NB_CLIENTS} clients...")
    clients_generes = 0

    for _ in range(NB_CLIENTS):
        prenom = random.choice(PRENOMS)
        nom = random.choice(NOMS)
        email = generer_email(prenom, nom)
        telephone = generer_telephone()
        date_inscription = generer_date_random(DATE_DEBUT, DATE_FIN)
        
        # On insère le client
        cur = conn.execute('''
            INSERT INTO clients (prenom, nom, seances_restantes, date_inscription, email, telephone, total_seances_faites) 
            VALUES (?, ?, ?, ?, ?, ?, 0)
        ''', (prenom, nom, 0, date_inscription.strftime('%Y-%m-%d'), email, telephone))
        
        client_id = cur.lastrowid
        
        # Initialisation des compteurs pour ce client
        current_date = date_inscription
        solde = 10 
        total_seances = 0 # <--- NOUVEAU COMPTEUR
        
        # Historique Création
        conn.execute('''
            INSERT INTO historique_seances (client_id, action, nombre, date_heure) 
            VALUES (?, ?, ?, ?)
        ''', (client_id, 'CREATION_COMPTE', 10, current_date.strftime('%Y-%m-%d %H:%M:%S')))

        while True:
            jours_ecoules = random.randint(2, 14) 
            current_date += timedelta(days=jours_ecoules)
            
            if current_date > DATE_FIN:
                break
            
            # Action : CHECK-IN
            solde -= 1
            total_seances += 1 # <--- ON INCRÉMENTE ICI
            
            conn.execute('''
                INSERT INTO historique_seances (client_id, action, nombre, date_heure) 
                VALUES (?, ?, ?, ?)
            ''', (client_id, 'CHECK-IN', -1, current_date.strftime('%Y-%m-%d %H:%M:%S')))
            
            # Action : RECHARGEMENT
            if solde <= 1:
                recharge = random.choice([5, 10, 20])
                solde += recharge
                conn.execute('''
                    INSERT INTO historique_seances (client_id, action, nombre, date_heure) 
                    VALUES (?, ?, ?, ?)
                ''', (client_id, 'ADD_SEANCES', recharge, current_date.strftime('%Y-%m-%d %H:%M:%S')))

        # --- MISE À JOUR FINALE AVEC LE TOTAL ---
        # On sauvegarde le solde ET le total des séances faites
        conn.execute('''
            UPDATE clients 
            SET seances_restantes = ?, total_seances_faites = ? 
            WHERE id = ?
        ''', (solde, total_seances, client_id))
        
        clients_generes += 1
        if clients_generes % 20 == 0:
            print(f"   ... {clients_generes} clients traités")

    conn.commit()
    conn.close()
    print("\n✅ TERMINÉ ! Les compteurs de séances sont maintenant corrects.")

if __name__ == '__main__':
    main()