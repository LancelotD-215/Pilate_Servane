import sqlite3

# Fixe 1 : Correction des accents corrompus et mise en forme de la casse
#def fix_corruption_and_casing(s):
#    if s is None or s == "":
#        return s
#    
#    # 1. Dictionnaire des remplacements (ordre optimisé)
#    replacements = {
#        'ã©': 'é', 'Ã©': 'é', 'é©': 'é',
#        'ã¨': 'è', 'Ã¨': 'è',
#        'ãª': 'ê', 'Ãª': 'ê',
#        'ã§': 'ç', 'Ã§': 'ç',
#        'à§': 'ç',              # Correction de l'erreur Franà§oise
#        'ãà': 'à', 'Ã ': 'à',
#        'ã¹': 'ù', 'Ã¹': 'ù',
#        'ã': 'à',
#        'Ï»¿': ''
#    }
#    
#    new_s = s
#    for corrupted, correct in replacements.items():
#        new_s = new_s.replace(corrupted, correct)
#    
#    # 2. Correction de la casse : Première lettre en Maj, le reste en Min
#    # On gère le cas des noms composés (ex: Jean-Pierre)
#    if '-' in new_s:
#        return '-'.join([part.strip().capitalize() for part in new_s.split('-')])
#    else:
#        return new_s.strip().capitalize()
#
#def fix_database():
#    db_path = 'database_clients.db' 
#    
#    try:
#        conn = sqlite3.connect(db_path)
#        cursor = conn.cursor()
#        
#        print(f"🔍 Analyse et normalisation de la base...")
#        cursor.execute("SELECT id, prenom, nom FROM clients")
#        rows = cursor.fetchall()
#        
#        updates = 0
#        for row in rows:
#            client_id, prenom, nom = row
#            
#            # On applique la correction d'accents + la mise en forme
#            new_prenom = fix_corruption_and_casing(prenom)
#            new_nom = fix_corruption_and_casing(nom)
#            
#            # Pour le NOM, on peut choisir soit Tout en Maj (UPPER), soit juste la 1ère (Capitalize)
#            # Ici on met juste la 1ère comme demandé
#            
#            if new_prenom != prenom or new_nom != nom:
#                cursor.execute(
#                    "UPDATE clients SET prenom = ?, nom = ? WHERE id = ?",
#                    (new_prenom, new_nom, client_id)
#                )
#                updates += 1
#                print(f"✨ Normalisé : {prenom} {nom} -> {new_prenom} {new_nom}")
#
#        conn.commit()
#        conn.close()
#        print(f"\n🎉 Terminé ! {updates} fiches clients ont été parfaitement remises en forme.")
#        
#    except Exception as e:
#        print(f"❌ Erreur : {e}")
#
#if __name__ == '__main__':
#    fix_database()

# Fixe 2 : 
#def apply_manual_updates():
#    db_path = 'database_clients.db'  # Vérifie bien le nom de ta base
#    conn = sqlite3.connect(db_path)
#    cursor = conn.cursor()
#
#    print("🚀 Début des mises à jour manuelles...")
#
#    # 1. Soustraction de séances
#    # Liste de tuples : (Prénom, Nom, Nb de séances à enlever)
#    reductions = [
#        ('Serge', 'Guermonprez', 6),
#        ('Francois', 'Carpentier', 10),
#        ('Isabelle', 'Cardon', 5),
#        ('Thierry', 'Cardon', 5)
#    ]
#
#    for prenom, nom, nb in reductions:
#        # On utilise UPPER() pour être sûr de matcher malgré la casse
#        cursor.execute("""
#            UPDATE clients 
#            SET seances_restantes = seances_restantes - ? 
#            WHERE UPPER(prenom) = UPPER(?) AND UPPER(nom) = UPPER(?)
#        """, (nb, prenom, nom))
#        
#        if cursor.rowcount > 0:
#            print(f"✅ {prenom} {nom} : -{nb} séances.")
#        else:
#            print(f"⚠️ Client non trouvé : {prenom} {nom}")
#
#    # 2. Corrections de noms
#    # Format : (Ancien Prénom, Ancien Nom, Nouveau Prénom, Nouveau Nom)
#    corrections = [
#        ('Stephanie', 'Delaplace', 'Stephanie', 'Delplace'),
#        ('Marc', 'Pannieu', 'Marc', 'Pannien'),
#        ('Benoit', 'Delassus', 'Anne Claire', 'Debarbieux') # Remplacement d'identité
#    ]
#
#    for old_p, old_n, new_p, new_n in corrections:
#        cursor.execute("""
#            UPDATE clients 
#            SET prenom = ?, nom = ? 
#            WHERE UPPER(prenom) = UPPER(?) AND UPPER(nom) = UPPER(?)
#        """, (new_p, new_n, old_p, old_n))
#        
#        if cursor.rowcount > 0:
#            print(f"✅ Identité mise à jour : {old_p} {old_n} -> {new_p} {new_n}")
#        else:
#            print(f"⚠️ Client non trouvé pour correction : {old_p} {old_n}")
#
#    conn.commit()
#    conn.close()
#    print("\n🎉 Toutes les modifications ont été appliquées.")


# Fixe 3 : 
#def clean_and_fix_db():
#    db_path = 'database_clients.db'  # Assure-toi que c'est le bon nom de fichier sur le serveur
#    
#    try:
#        conn = sqlite3.connect(db_path)
#        cursor = conn.cursor()
#        print(f"🔍 Connexion établie à la base de données : {db_path}")
#        print("⚡ Démarrage du nettoyage chirurgical...")
#
#        # --- 1. SUPPRESSION DE L'INTRUS ---
#        # On utilise UPPER() pour éviter les pièges de casse
#        cursor.execute("DELETE FROM clients WHERE UPPER(nom) = 'ZSWTFOKVOSL' OR UPPER(prenom) = 'MTVVNKLTHU'")
#        if cursor.rowcount > 0:
#            print(f"❌ Intrus 'Mtvvnklthu Zswtfokvsl' supprimé avec succès ({cursor.rowcount} ligne(s) impactée(s)).")
#        else:
#            print("⚠️ L'intrus 'Mtvvnklthu Zswtfokvsl' n'a pas été trouvé (peut-être déjà supprimé).")
#
#        # --- 2. SUPPRESSION DE CONSTANCE PAQUET ---
#        cursor.execute("SELECT id FROM clients WHERE UPPER(prenom) = 'CONSTANCE' AND UPPER(nom) = 'PAQUET'")
#        client_paquet = cursor.fetchone()
#        
#        if client_paquet:
#            client_id = client_paquet[0]
#            # On nettoie proprement ses habitudes et son historique avant de la supprimer (intégrité de la BDD)
#            cursor.execute("DELETE FROM habitudes WHERE client_id = ?", (client_id,))
#            cursor.execute("DELETE FROM historique_seances WHERE client_id = ?", (client_id,))
#            cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
#            print("❌ Fiche de 'Constance Paquet' ainsi que ses habitudes et son historique supprimés.")
#        else:
#            print("⚠️ 'Constance Paquet' introuvable dans la table des clients.")
#
#        # --- 3. CORRECTION ALEXANDRE -> ALEXANDRA THOMAS ---
#        cursor.execute("""
#            UPDATE clients 
#            SET prenom = 'Alexandra' 
#            WHERE UPPER(prenom) = 'ALEXANDRE' AND UPPER(nom) = 'THOMAS'
#        """)
#        if cursor.rowcount > 0:
#            print("✏️ Prénom corrigé avec succès : 'Alexandre Thomas' est devenu 'Alexandra Thomas'.")
#        else:
#            print("⚠️ Aucun client trouvé au nom de 'Alexandre Thomas' pour la correction.")
#
#        # Validation définitive des changements
#        conn.commit()
#        print("\n🎉 Nettoyage et corrections appliqués avec succès sur le serveur !")
#
#    except Exception as e:
#        print(f"❌ Une erreur est survenue, modifications annulées : {e}")
#        conn.rollback()
#    finally:
#        conn.close()
#        print("🔌 Connexion à la base de données fermée.")
#
#if __name__ == '__main__':
#    clean_and_fix_db()


#Fixe 3 :
def apply_batch_corrections():
    db_path = 'database_clients.db'  # Base de production
    
    try:
        conn = sqlite3.connect(db_path)
        print(f"🔍 Connexion à la base de données : {db_path}")
        print("⚡ Application des corrections d'identités...")

        # Liste des corrections d'identité précises
        # Format : (Ancien Prénom, Ancien Nom, Nouveau Prénom, Nouveau Nom)
        corrections = [
            # 1. Corrections des noms de famille
            ('Stephanie', 'Delaplace', 'Stephanie', 'Delplace'),
            ('Marc', 'Pannien', 'Marc', 'Pannien'),
            ('Marc', 'Panieu', 'Marc', 'Pannien'), # Double sécurité selon tes messages
            
            # 2. Remplacements et ajustements demandés aujourd'hui
            ('Christophe', 'Robbe', 'Christopher', 'Robbe'),
            ('Valerie', 'Crombet', 'Valerie', 'Crombé'),
            ('Marie', 'Verhaegen', 'Marie', 'Verhaeghe'),
            ('Celine', 'Martin', 'Cécile', 'Martin'),
            ('Laurence', 'Deconninck', 'Laurence', 'Dekoninck'),
            ('Jean Francois', 'Charvet', 'Jean-François', 'Charvet'),
            ('Edith', 'Meriaux', 'Edith', 'Meriau'),
            ('Babette', 'Van Ost', 'Babette', 'Van Oost'),
            
            # Gestion du cas Ducatez (Freund-Ducatez / Freins-Ducatez)
            # Dans le doute, j'applique Freund-Ducatez qui est ta demande principale
            # Si le prénom est connu (ex: Servane, Nathalie...), on cible. Sinon, on cherche sur le NOM.
        ]

        total_updates = 0

        # Application des couples Prénom/Nom stricts
        for old_p, old_n, new_p, new_n in corrections:
            cursor = conn.execute("""
                UPDATE clients 
                SET prenom = ?, nom = ? 
                WHERE UPPER(prenom) = UPPER(?) AND UPPER(nom) = UPPER(?)
            """, (new_p, new_n, old_p, old_n))
            
            if cursor.rowcount > 0:
                print(f"✅ Mis à jour : {old_p} {old_n} -> {new_p} {new_n}")
                total_updates += cursor.rowcount

        # Cas particulier pour "Ducatez" -> "Freund-Ducatez" (Recherche par nom uniquement car prénom non spécifié)
        cursor_ducatez = conn.execute("""
            UPDATE clients 
            SET nom = 'Freund-Ducatez' 
            WHERE UPPER(nom) = 'DUCATEZ'
        """)
        if cursor_ducatez.rowcount > 0:
            print(f"✅ Mis à jour : Famille DUCATEZ -> Freund-Ducatez ({cursor_ducatez.rowcount} ligne(s) modifiée(s))")
            total_updates += cursor_ducatez.rowcount

        # Validation des changements
        conn.commit()
        print(f"\n🎉 Opération terminée. {total_updates} fiches clients ont été corrigées avec succès.")

    except Exception as e:
        print(f"❌ Une erreur est survenue, rollback appliqué : {e}")
        conn.rollback()
    finally:
        conn.close()
        print("🔌 Connexion fermée.")

if __name__ == '__main__':
    apply_batch_corrections()