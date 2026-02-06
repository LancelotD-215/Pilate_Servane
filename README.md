# 📂 Gestionnaire de Séances Pilate

## 🎯 1. Objectif Global
Application web de gestion complète pour coach de Pilates permettant de :
- Remplacer le suivi papier par une base de données numérique
- Gérer les soldes de séances clients
- Suivre les habitudes et la fréquentation
- Planifier et visualiser les créneaux hebdomadaires
- Offrir une interface responsive (ordinateur/tablette/mobile)

## 🛠 2. Stack Technique
* **Backend :** Python 3.x + Flask
* **Base de Données :** SQLite (fichier `.db` local)
* **Frontend :** HTML5 + Bootstrap 5.3.0 + Jinja2
* **JavaScript :** jQuery + DataTables pour les tableaux interactifs
* **Architecture :** Monolithique simple

## 🗄 3. Structure des Données

### Table `clients`
* `id` (PK): Identifiant unique
* `prenom`, `nom`: Identité
* `email`, `telephone`: Contact (optionnel)
* `date_inscription`: Date d'ajout
* `seances_restantes`: Solde actuel
* `total_seances_faites`: Compteur total
* `abonnement`: Statut d'abonnement

### Table `semaine_type`
* `id` (PK): Identifiant du créneau
* `jour_semaine`: 0=Lundi, 1=Mardi, etc.
* `heure_debut`: Format "HH:MM"
* `duree`: Durée en minutes
* `type_seance`: "Pilates Fondamental", "Intermédiaire", etc.
* `actif`: Créneau actif/inactif

### Table `habitudes`
* `id` (PK): Identifiant
* `client_id` (FK): Lien vers client
* `creneau_id` (FK): Lien vers créneau type
* `date_debut`: Date d'ajout de l'habitude

### Table `historique_seances`
* `id` (PK): Identifiant
* `client_id` (FK): Client concerné
* `date_heure`: Timestamp de l'action
* `action`: "CHECK-IN", "ADD_SEANCES", "NEW_ACCOUNT"
* `nombre`: Variation du solde (+/-)

### Table `calendrier_seances` *(en préparation)*
* Planning des séances réelles avec statuts

## 💻 4. Fonctionnalités Implémentées

### 🏠 **Tableau de Bord (Accueil)**
* **Widgets configurables :**
  - Alertes clients à solde négatif
  - Alertes clients à solde zéro
  - Meilleur client du mois
  - Client avec le plus de séances restantes
  - Nombre total de clients
  - Séances données dans le mois
* **Actions rapides :** Régularisation des impayés

### 👥 **Gestion des Clients**
* **Liste complète** avec DataTables (tri, recherche, pagination)
* **Badges colorés** selon le solde (vert/orange/rouge)
* **Ajout rapide** de séances via modal
* **Recherche globale** dans la barre de navigation

### ✅ **Check-in / Présence**
* **Saisie simple** : Prénom + Nom
* **Validation automatique** avec décrément du solde
* **Historique automatique** de toutes les actions

### 📝 **Nouveau Client**
* **Formulaire complet :** identité, contact, solde initial
* **Sélection de créneau habituel** avec liste organisée par jour
* **Création automatique** des habitudes

### 💰 **Ajout de Séances**
* **Interface dédiée** pour recharger les comptes
* **Actions rapides** depuis la liste clients
* **Traçabilité complète** dans l'historique

### 📅 **Planning Hebdomadaire**
* **Vue visuelle** type Google Calendar
* **Navigation** semaine par semaine
* **Créneaux colorés** par type de séance
* **Mise en évidence** du jour actuel

### 👤 **Fiche Client Détaillée**
* **Informations complètes** : contact, solde, statistiques
* **Habitudes enregistrées** avec jours et horaires
* **Historique des 10 dernières actions**
* **Accès via recherche** ou navigation

## 📁 5. Architecture des Fichiers

```
Projet_Pilate/
├── app.py                    # Application Flask principale (7 routes)
├── app_lib.py               # Fonctions utilitaires (widgets, stats)
├── schema.sql               # Structure complète de la base
├── init_bdd.py              # Initialisation basique
├── simul_db_tes.py         # Générateur de données de test (100 clients)
├── database_clients_test.db # Base de données de test (SQLite)
├── TO_DO.md                 # Liste des tâches à venir
├── templates/               # Pages HTML (Bootstrap + Jinja2)
│   ├── layout.html          # Structure générale + navigation
│   ├── index.html           # Tableau de bord avec widgets
│   ├── gestion_clients.html # Liste des clients (DataTables)
│   ├── fiche_client.html    # Détail client avec habitudes
│   ├── ajout_client.html    # Formulaire nouveau client
│   ├── ajout_seances.html   # Recharge de séances
│   ├── presence.html        # Interface check-in
│   └── planning.html        # Planning hebdomadaire
└── static/
    └── style.css            # CSS personnalisé (optionnel)
```

## 🚀 6. Fonctionnalités en Développement

### 📋 **Prochaines Étapes**
- [ ] Pop-up détail des séances dans le planning
- [ ] Widget "clients absents depuis 1 mois"
- [ ] Configuration dynamique des widgets
- [ ] Ajout de séances depuis la fiche client
- [ ] Modification des habitudes clients
- [ ] Historique complet illimité
- [ ] Calcul automatique des habitudes récurrentes

### 🔮 **Évolutions Futures**
- [ ] Authentification et gestion des utilisateurs
- [ ] Statistiques avancées et graphiques
- [ ] Export PDF des rapports
- [ ] Notifications automatiques
- [ ] API REST pour applications mobiles
- [ ] QR Codes pour check-in automatique

## ⚙️ 7. Installation et Lancement

```bash
# Cloner le projet
git clone [votre-repo]
cd Projet_pilate_maman

# Installer les dépendances
pip install flask

# Initialiser la base de données
python init_bdd.py

# (Optionnel) Générer des données de test
python simul_db_tes.py

# Lancer l'application
python app.py

# Accéder à l'interface
# Navigateur : http://localhost:5000
```

## 📊 8. État du Projet
* **Version :** v1.5 (Février 2026)
* **Statut :** Fonctionnel pour un usage quotidien
* **Base de clients :** Testée avec 100+ clients
* **Performance :** Optimisée pour petits/moyens studios