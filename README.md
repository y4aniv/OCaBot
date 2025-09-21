<div align="center">
  <img width="217.6875" height="122.8125" alt="Adobe Express - file (7) 1" src="https://github.com/user-attachments/assets/c5e6a30e-ad21-4c84-8f59-b911c982b24a" />
  <h3>OCaBot</h3>
  <p>OCaml. Smarter. Faster.</p>
</div>


## Fonctionnalités

- **Évaluation de code OCaml** : Exécute du code OCaml dans un environnement sécurisé
- **Explications IA** : Génère des explications détaillées grâce à Mistral AI
- **Discussions interactives** : Répond aux questions dans les threads de discussion

## Installation

### Prérequis

- Python 3.8+
- OCaml installé sur le système
- Compte Discord Developer avec un bot token
- Clé API Mistral

### Configuration

1. Clonez le repository :
```bash
git clone https://github.com/y4aniv/OCaBot.git
cd OCaBot
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez les variables d'environnement :
```bash
cp .env.example .env
```

4. Lancez le bot :
```bash
./start.sh
# ou directement : python main.py
```

## Configuration

Créez un fichier `.env` à partir de `.env.example` et renseignez :

- `BOT_TOKEN` : Token de votre bot Discord
- `MISTRAL_API_KEY` : Votre clé API Mistral
- `LOG_LEVEL` : Niveau de logging (DEBUG, INFO, WARNING, ERROR)

## Architecture

```
OCaBot/
├── main.py                       # Point d'entrée principal
├── src/
│   ├── cogs/                     # Commandes Discord organisées
│   │   ├── basic.py              # Commandes de base (ping)
│   │   └── ocaml.py              # Commandes OCaml
│   ├── config/                   # Configuration
│   │   ├── messages.py           # Messages centralisés
│   │   └── settings.py           # Configuration système
│   ├── services/                 # Services métier
│   │   ├── mistral_service.py    # Interface Mistral AI
│   │   └── ocaml_service.py      # Évaluation OCaml
│   └── utils/                    # Utilitaires
│       ├── error_handler.py      # Gestion d'erreurs
│       └── logger.py             # Système de logging
├── logs/                         # Logs générés
├── requirements.txt              # Dépendances Python
└── start.sh                      # Script de lancement
```

## Utilisation

### Commandes disponibles

- `/ping` : Vérifier la latence du bot
- `/evaluate` : Évaluer du code OCaml dans un modal

### Mentions

Mentionnez le bot (`@OCaBot`) dans les threads de discussion OCaml pour obtenir de l'aide contextuelle.

## Développement

### Ajout de nouvelles fonctionnalités

1. Créez un nouveau cog dans `src/cogs/`
2. Chargez-le dans `main.py`
3. Ajoutez les messages dans `src/config/messages.py`

### Logging

Le système de logging génère :
- `logs/ocabot.log` : Log complet avec rotation
- `logs/errors.log` : Erreurs uniquement
- Console : Messages INFO et plus