# 📂 Gestion Studio S' — Gestionnaire de Séances Pilates

Application web de gestion pour studio de Pilates. Elle remplace le suivi papier
par une base de données numérique : soldes de séances, présences, planning
hebdomadaire et borne de check-in en libre-service.

> **Statut :** ✅ En production — déployée sur **PythonAnywhere** avec nom de
> domaine **OVH**. Utilisée quotidiennement par le studio.

---

## 🎯 1. Objectif

- Remplacer le suivi papier par une base de données numérique
- Gérer les soldes de séances de chaque client
- Suivre la fréquentation et les habitudes (créneaux récurrents)
- Visualiser le planning hebdomadaire et valider les présences
- Permettre aux clients de pointer eux-mêmes via une **borne**
- Interface responsive (ordinateur / tablette / mobile)

---

## 🛠 2. Stack technique

| Couche        | Technologie                                   |
|---------------|-----------------------------------------------|
| Backend       | Python 3 + **Flask 3.1**                      |
| Base de données | **SQLite** (`database_clients.db`)          |
| Templates     | Jinja2 + **Bootstrap 5.3**                     |
| JavaScript    | jQuery + **DataTables** (tableaux interactifs) |
| Icônes        | Font Awesome 6.4                               |
| Fuseau horaire | **pytz** (`Europe/Paris`)                     |
| Hébergement   | PythonAnywhere + domaine OVH                   |

Architecture : monolithique simple (`app.py` + `app_lib.py`).

---

## 🗄 3. Structure des données

Schéma complet dans [`schema.sql`](schema.sql).

### Table `clients`
`id`, `prenom`, `nom`, `date_inscription`, `telephone`, `email`,
`seances_restantes` (solde courant), `total_seances_faites`, `abonnement`.

### Table `semaine_type` (créneaux récurrents)
`id`, `jour_semaine` (0=Lundi … 6=Dimanche), `heure_debut` (`"HH:MM"`),
`duree` (minutes), `type_seance`, `actif`.

### Table `habitudes` (créneaux habituels d'un client)
`id`, `client_id` → `clients`, `creneau_id` → `semaine_type`, `date_debut`.

### Table `historique_seances`
`id`, `client_id`, `date_heure`, `action`, `nombre` (variation +/−), `seance_id`.
Valeurs d'`action` : `CHECK-IN`, `PRESENCE_VALIDEE`, `ADD_SEANCES`,
`NEW_ACCOUNT`, `IMPORT_INITIAL`.

### Table `calendrier_seances` *(créée, pas encore exploitée)*
Destinée au planning des séances réelles avec statuts.

---

## 💻 4. Fonctionnalités

### 🏠 Tableau de bord (`/`)
Widgets d'alerte et de suivi :
- Clients à solde **négatif** (régularisation rapide possible)
- Clients à solde **zéro**
- **Meilleur client** du mois (le plus de séances faites)
- Client avec le **plus de séances restantes**
- **Nombre total** de clients
- **Séances données** dans le mois
- Clients **pas venus depuis 30 jours**

### 👥 Gestion des clients (`/gestion_clients`)
Liste complète avec DataTables (tri, recherche, pagination), badges colorés
selon le solde (vert / orange / rouge), ajout rapide de séances en un clic.

### ✅ Présence / Check-in (`/presence`)
Saisie prénom + nom → décrément automatique du solde + entrée dans l'historique.

### 🖥️ Borne libre-service (`/borne`)
Check-in autonome par le client. Mémorise l'identité via **cookies** (60 jours)
pour un pointage en un clic les fois suivantes. Page de succès dédiée.

### 📝 Nouveau client (`/ajout_client`)
Formulaire complet (identité, contact, solde initial, abonnement) avec choix
d'un créneau habituel → création automatique de l'habitude associée.

### 💰 Ajout de séances (`/ajout_seances` et ajout rapide)
Recharge des comptes, depuis la page dédiée, la liste clients ou la fiche client.
Traçabilité complète dans l'historique.

### 📅 Planning hebdomadaire (`/planning`)
Vue calendrier (Lundi→Vendredi, 9h–21h), navigation semaine par semaine,
créneaux positionnés à l'heure, mise en évidence du jour courant.
Affiche les habitués attendus par créneau et leur **statut de présence**
(pointage détecté entre −30 min et la fin du cours). Validation manuelle
de présence directement depuis un créneau.

### 👤 Fiche client (`/client/<id>`)
Coordonnées, solde, statistiques, habitudes (créneaux récurrents),
10 dernières actions de l'historique, ajout de séances et **modification des
habitudes** via modale. Accessible aussi par la recherche globale (barre de nav).

---

## 📁 5. Architecture des fichiers

```
Pilate_Servane/
├── app.py                  # Application Flask : toutes les routes
├── app_lib.py              # Fonctions utilitaires (connexion DB, widgets, stats)
├── schema.sql              # Structure complète de la base
├── repair.py               # Scripts ponctuels de correction de données (one-shot)
├── requirements.txt        # Dépendances Python
├── database_clients.db     # Base SQLite (NON versionnée — voir .gitignore)
├── data/                   # Données clients locales (NON versionnées — RGPD)
├── archive/                # Scripts de développement, conservés à titre historique
│   ├── init_bdd.py         # Import initial depuis un CSV (obsolète)
│   └── simul_db_tes.py     # Générateur de données de test fictives
├── static/
│   ├── style.css           # Styles personnalisés
│   ├── logo-studio-s-pilates-1x.png
│   └── studioSfavicon.png
└── templates/              # Pages HTML (Bootstrap + Jinja2)
    ├── layout.html         # Structure générale + navigation
    ├── index.html          # Tableau de bord
    ├── gestion_clients.html
    ├── fiche_client.html
    ├── ajout_client.html
    ├── ajout_seances.html
    ├── presence.html
    ├── borne.html          # Borne de check-in
    ├── borne_succes.html
    └── planning.html       # Planning hebdomadaire
```

---

## ⚙️ 6. Installation et lancement (local)

```bash
# 1. Cloner le projet
git clone <votre-repo>
cd Pilate_Servane

# 2. Créer et activer un environnement virtuel (recommandé)
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Initialiser une base de données locale avec des données de test
python archive/simul_db_tes.py
# Ce script crée 'database_clients_test.db'. L'application lit 'database_clients.db' :
# renomme/copie le fichier pour qu'il soit pris en compte :
#   copy database_clients_test.db database_clients.db   (Windows)
#
# (archive/init_bdd.py servait à l'import initial depuis un CSV au lancement du
#  studio ; ce CSV n'est plus utilisé, le script est conservé à titre historique.)

# 5. Lancer l'application
python app.py
# → http://localhost:5000
```

Le mode `debug` s'active automatiquement en local et se désactive en
production (détection de la variable `PYTHONANYWHERE_DOMAIN`).

---

## 🔄 7. Workflow de déploiement

1. Développement et tests en **local** sur le poste.
2. `git push` du code une fois validé.
3. `git pull` côté serveur PythonAnywhere, puis rechargement de la web app.

> ⚠️ La base de données (`*.db`) **n'est pas versionnée** : la production possède
> ses propres données. Les corrections de données en prod se font via des scripts
> ponctuels (cf. [`repair.py`](repair.py)) exécutés directement sur le serveur.

---

## 📋 8. Suites prévues

Voir [`TO_DO.md`](TO_DO.md). Principaux chantiers en cours :
- Ajout / suppression de séances dans l'agenda (ponctuel et définitif)
- Sélecteur de widgets affichés sur le tableau de bord
- Suppression de client
- Affichage de l'historique complet dans la fiche client
