# 📦 archive/ — Scripts de développement

Ce dossier regroupe les scripts qui ont servi pendant la mise en place du site
mais qui ne font **pas** partie du fonctionnement quotidien de l'application en
production. Ils sont conservés à titre historique / de référence.

| Script | Rôle | Statut |
|--------|------|--------|
| `init_bdd.py` | Import initial de la base depuis le CSV clients au lancement du studio | ⛔ Obsolète (le CSV source a été supprimé, la prod est déjà initialisée) |
| `simul_db_tes.py` | Génère une base `database_clients_test.db` remplie de ~100 clients **fictifs** | ✅ Utilisable pour des tests sur données factices |

## Lancer le générateur de données de test

À exécuter **depuis la racine du projet** (les scripts utilisent des chemins
relatifs vers `schema.sql`) :

```bash
python archive/simul_db_tes.py
```

Cela crée `database_clients_test.db`. Pour que l'application l'utilise, copiez-la
sous le nom attendu :

```bash
copy database_clients_test.db database_clients.db   # Windows
```
