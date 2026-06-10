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
    print(f"🚀 Démarrage de la simulation sur {DB_NAME}...")
    conn = get_db_connection()
    
    # 1. INIT DU SCHÉMA
    print("🧹 Réinitialisation de la structure...")
    with open('schema.sql') as f:
        conn.executescript(f.read())
    
    # 2. GÉNÉRATION DU PLANNING TYPE (Pour que la page Planning ne soit pas vide)
    print("📅 Création de la semaine type...")
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
    (1, '19:15', 45, 'Pilates Fondamental'),
    (1, '20:00', 45, 'Pilates Intermédiaire'),
    

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
    (3, '18:30', 45, 'Pilates Intermédiaire')
    
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
        
        # NOTE : On ne spécifie PAS 'abonnement', donc il sera à 0 par défaut (grâce au schéma)
        cur = conn.execute('''
            INSERT INTO clients (prenom, nom, seances_restantes, date_inscription, email, telephone, total_seances_faites) 
            VALUES (?, ?, ?, ?, ?, ?, 0)
        ''', (prenom, nom, 0, date_inscription.strftime('%Y-%m-%d'), email, telephone))
        
        client_id = cur.lastrowid
        
        # Initialisation des compteurs
        current_date = date_inscription
        solde = 10 
        total_seances = 0 
        
        # Historique Création
        conn.execute('''
            INSERT INTO historique_seances (client_id, action, nombre, date_heure) 
            VALUES (?, ?, ?, ?)
        ''', (client_id, 'NEW_ACCOUNT', 10, current_date.strftime('%Y-%m-%d %H:%M:%S')))

        while True:
            jours_ecoules = random.randint(2, 14) 
            current_date += timedelta(days=jours_ecoules)
            
            if current_date > DATE_FIN:
                break
            
            # Action : CHECK-IN
            solde -= 1
            total_seances += 1
            
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

        # Mise à jour finale
        conn.execute('''
            UPDATE clients 
            SET seances_restantes = ?, total_seances_faites = ? 
            WHERE id = ?
        ''', (solde, total_seances, client_id))
        
        clients_generes += 1

    # création de client a solde 0 pour tester les alertes
    conn.execute('''
        INSERT INTO clients (prenom, nom, seances_restantes, date_inscription, email, telephone, total_seances_faites) 
        VALUES (?, ?, ?, ?, ?, ?, 0)
    ''', ('Lancelot', 'Danesse', 0, DATE_DEBUT.strftime('%Y-%m-%d'), 'lancelot.12@example.com', '1212121212'))

    # création de client a solde -1 pour tester les alertes
    conn.execute('''
        INSERT INTO clients (prenom, nom, seances_restantes, date_inscription, email, telephone, total_seances_faites) 
        VALUES (?, ?, ?, ?, ?, ?, 0)
    ''', ('Juliette', 'Bouriant', -1, DATE_DEBUT.strftime('%Y-%m-%d'), 'juliette.14@example.com', '1010101010'))

    conn.commit()
    conn.close()
    print("\n✅ TERMINÉ ! Base de test prête.")

if __name__ == '__main__':
    main()