#!/bin/bash

echo "Démarrage d'OCaBot..."

if [ ! -f ".env" ]; then
    echo "ATTENTION: Fichier .env manquant!"
    echo "Copiez .env.example vers .env et configurez vos tokens."
    exit 1
fi

if ! python -c "import nextcord, mistralai, dotenv" 2>/dev/null; then
    echo "Installation des dépendances..."
    pip install -r requirements.txt
fi

# Lancer le bot
python main.py