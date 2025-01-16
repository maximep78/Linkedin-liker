# LinkedIn Auto-Liker Bot 🚀

## Description 📝
Ce projet est un bot Python automatisé utilisant Selenium pour interagir avec LinkedIn. Il permet :
- ✅ De naviguer vers la page des activités récentes d'un profil LinkedIn.
- 👍 D'identifier et liker les deux posts les plus récents.
- 📅 De trier les posts en fonction de leur date de publication (ex. "4 h", "2 j").

## Fonctionnalités ✨
- 🔐 Accès automatisé à LinkedIn.
- 🔄 Gestion de la session avec détection des connexions expirées.
- 📊 Tri des posts par date de publication pour garantir que seuls les plus récents sont likés.
- 📜 Logs détaillés pour suivre les actions du bot.

## Prérequis 🛠️
### Outils nécessaires :
1. **Python 3.8 ou supérieur** 🐍
2. **Docker et Docker Compose** 🐳
3. **Navigateur Google Chrome** 🌐
4. **ChromeDriver** 🚗

### Librairies Python utilisées :
- `selenium`
- `cryptography`
- `logging`

Installez les dépendances listées dans le fichier `requirements.txt` :
```bash
pip install -r requirements.txt
```

## Installation 🖥️
### Étape 1 : Cloner le dépôt
```bash
git clone <URL_DU_DÉPÔT>
cd <NOM_DU_RÉPERTOIRE>
```

### Étape 2 : Configurer les secrets 🔑
1. Créez les fichiers suivants dans le répertoire racine :
   - `linkedin_username.txt` : Contient votre identifiant LinkedIn.
   - `linkedin_password.txt` : Contient votre mot de passe LinkedIn.
   - `linkedin_profiles.txt` : Contient les URLs des profils à cibler (une URL par ligne).

2. Chiffrez ces fichiers :
```bash
python encrypt_secrets.py
```

### Étape 3 : Démarrer avec Docker 🐋
1. Construisez et démarrez le conteneur Docker :
```bash
docker-compose up --build
```
2. Surveillez les logs pour vérifier les actions du bot :
```bash
docker logs -f linkedin-liker-1
```

## Utilisation 📚
1. Le bot se connecte automatiquement à LinkedIn et accède à la page `/recent-activity/all/`.
2. Il trie les posts en fonction de leur heure de publication (ex. "4 h") et like les deux plus récents.
3. Les actions sont enregistrées dans des logs détaillés.

## Structure du projet 🗂️
- `encrypt_secrets.py` : Script pour chiffrer vos identifiants et secrets.
- `generate_key.py` : Génère une clé de chiffrement pour vos secrets.
- `linkedin_liker.py` : Script principal du bot.
- `Dockerfile` : Configuration Docker pour l'environnement.
- `docker-compose.yml` : Orchestration des conteneurs Docker.
- `requirements.txt` : Liste des dépendances Python.

## Personnalisation 🛠️
- **Nombre de posts à liker :** Modifiez la variable `num_posts` dans le script principal pour ajuster le nombre de posts likés.
- **Intervalle entre les cycles :** Modifiez `check_interval` pour ajuster le temps de pause entre deux cycles.

## Sécurité 🔒
- Les identifiants LinkedIn sont chiffrés avec `Fernet` (cryptographie symétrique).
- Ne partagez jamais votre clé de chiffrement ou vos fichiers chiffrés.

## Débogage 🐞
- Si le bot échoue à trouver des posts ou des boutons "J’aime", inspectez la structure HTML de la page et ajustez les sélecteurs XPath dans le script principal.
- Consultez les logs pour plus de détails sur les erreurs.

## Contributions 🤝
Les contributions sont les bienvenues ! Créez une pull request ou ouvrez une issue pour signaler un problème ou proposer une amélioration.

## Licence 📜
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.
