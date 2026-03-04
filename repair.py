import sqlite3

def fix_corruption_and_casing(s):
    if s is None or s == "":
        return s
    
    # 1. Dictionnaire des remplacements (ordre optimisé)
    replacements = {
        'ã©': 'é', 'Ã©': 'é', 'é©': 'é',
        'ã¨': 'è', 'Ã¨': 'è',
        'ãª': 'ê', 'Ãª': 'ê',
        'ã§': 'ç', 'Ã§': 'ç',
        'à§': 'ç',              # Correction de l'erreur Franà§oise
        'ãà': 'à', 'Ã ': 'à',
        'ã¹': 'ù', 'Ã¹': 'ù',
        'ã': 'à',
        'Ï»¿': ''
    }
    
    new_s = s
    for corrupted, correct in replacements.items():
        new_s = new_s.replace(corrupted, correct)
    
    # 2. Correction de la casse : Première lettre en Maj, le reste en Min
    # On gère le cas des noms composés (ex: Jean-Pierre)
    if '-' in new_s:
        return '-'.join([part.strip().capitalize() for part in new_s.split('-')])
    else:
        return new_s.strip().capitalize()

def fix_database():
    db_path = 'database_clients.db' 
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"🔍 Analyse et normalisation de la base...")
        cursor.execute("SELECT id, prenom, nom FROM clients")
        rows = cursor.fetchall()
        
        updates = 0
        for row in rows:
            client_id, prenom, nom = row
            
            # On applique la correction d'accents + la mise en forme
            new_prenom = fix_corruption_and_casing(prenom)
            new_nom = fix_corruption_and_casing(nom)
            
            # Pour le NOM, on peut choisir soit Tout en Maj (UPPER), soit juste la 1ère (Capitalize)
            # Ici on met juste la 1ère comme demandé
            
            if new_prenom != prenom or new_nom != nom:
                cursor.execute(
                    "UPDATE clients SET prenom = ?, nom = ? WHERE id = ?",
                    (new_prenom, new_nom, client_id)
                )
                updates += 1
                print(f"✨ Normalisé : {prenom} {nom} -> {new_prenom} {new_nom}")

        conn.commit()
        conn.close()
        print(f"\n🎉 Terminé ! {updates} fiches clients ont été parfaitement remises en forme.")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == '__main__':
    fix_database()