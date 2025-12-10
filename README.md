# 🚗 TAWSILA24 - Plateforme de Covoiturage

**توصيلة 24** - Connecter les 24 gouvernorats tunisiens

Une plateforme moderne et professionnelle de covoiturage développée avec Django, couvrant l'ensemble du territoire tunisien.

## 🌟 Fonctionnalités

- 👤 **Gestion des utilisateurs** : Inscription, connexion, profils personnalisés
- 🚗 **Publication de trajets** : Les conducteurs peuvent publier leurs trajets
- 🔍 **Recherche avancée** : Recherche par ville de départ, arrivée et date
- 📅 **Réservation de places** : Système de réservation en temps réel
- 💬 **Messagerie** : Communication entre conducteurs et passagers
- ⭐ **Système d'évaluation** : Notation et commentaires après chaque trajet
- 📱 **Interface responsive** : Compatible mobile, tablette et desktop

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Étapes d'installation

1. **Cloner le projet**
```bash
cd couvoituragee
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
- Windows :
```bash
venv\Scripts\activate
```
- Mac/Linux :
```bash
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Configurer les variables d'environnement**
```bash
copy .env.example .env
```
Puis éditer `.env` avec vos propres valeurs.

6. **Créer les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

8. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

9. **Accéder à l'application**
Ouvrir votre navigateur à l'adresse : http://127.0.0.1:8000/

## 📁 Structure du projet

```
TAWSILA24/
├── apps/
│   ├── users/          # Gestion des utilisateurs
│   ├── trips/          # Gestion des trajets
│   ├── bookings/       # Réservations
│   ├── messaging/      # Messagerie
│   └── reviews/        # Évaluations
├── static/             # Fichiers statiques (CSS, JS, images)
├── templates/          # Templates HTML
├── media/              # Fichiers uploadés par les utilisateurs
└── covoiturage/        # Configuration du projet
```

## 🎯 Utilisation

### Pour les passagers
1. Créer un compte
2. Rechercher un trajet
3. Réserver une place
4. Contacter le conducteur
5. Évaluer le trajet après le voyage

### Pour les conducteurs
1. Créer un compte et activer le mode conducteur
2. Publier un trajet
3. Gérer les réservations
4. Communiquer avec les passagers
5. Recevoir des évaluations

## 🛠️ Technologies utilisées

- **Backend** : Django 4.2
- **Frontend** : HTML5, CSS3, Bootstrap 5, JavaScript
- **Base de données** : SQLite (développement) / PostgreSQL (production recommandée)
- **Authentification** : Django Auth System
- **Formulaires** : Django Crispy Forms

## 📊 Administration

Accéder au panel d'administration Django :
- URL : http://127.0.0.1:8000/admin/
- Utiliser les identifiants du superutilisateur

## 🔒 Sécurité

- Authentification requise pour les actions sensibles
- Protection CSRF activée
- Validation des données côté serveur
- Hashage sécurisé des mots de passe

## 🚀 Déploiement

Pour le déploiement en production :
1. Configurer `DEBUG=False` dans `.env`
2. Définir `ALLOWED_HOSTS` appropriés
3. Utiliser PostgreSQL au lieu de SQLite
4. Configurer un serveur web (Nginx/Apache)
5. Utiliser Gunicorn comme serveur WSGI
6. Activer HTTPS

## 📝 Licence

Ce projet est développé à des fins éducatives.

## 👥 Auteur

**TAWSILA24** - Plateforme de covoiturage tunisienne développée dans le cadre d'un projet académique.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou soumettre une pull request.
