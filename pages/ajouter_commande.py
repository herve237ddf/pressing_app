import streamlit as st
import sqlite3
import re
from datetime import datetime

# Connexion à la base de données SQLite
conn = sqlite3.connect("pressing1.db")
cursor = conn.cursor()

# Configuration de la page
st.set_page_config(page_title="Ajouter une Commande", layout="centered",initial_sidebar_state="collapsed")
st.title("Ajouter une Nouvelle Commande")

# Fonction pour valider l'email
def validate_email(email):
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(regex, email) is not None

# Fonction pour valider le téléphone
def validate_telephone(telephone):
    regex = r"^\+237\s6\d{2}\s\d{3}\s\d{3}$"
    return re.match(regex, telephone) is not None

# Fonction pour traiter un client (nouveau ou existant)
def process_client(nom, prenom, adresse, telephone, email):
    cursor.execute("SELECT client_id, points_fidelite FROM Clients WHERE email = ? OR telephone = ?", (email, telephone))
    client = cursor.fetchone()

    if client:
        client_id = client[0]
        points_fidelite = client[1] + 1
        cursor.execute("UPDATE Clients SET points_fidelite = ? WHERE client_id = ?", (points_fidelite, client_id))
        conn.commit()
        return client_id, True
    else:
        cursor.execute(
            "INSERT INTO Clients (nom, prenom, adresse, telephone, email, date_inscription) VALUES (?, ?, ?, ?, ?, ?)",
            (nom, prenom, adresse, telephone, email, datetime.now().strftime('%Y-%m-%d'))
        )
        conn.commit()
        return cursor.lastrowid, False

# Formulaire principal
with st.form(key="order_form"):
    st.subheader("Informations Client")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    adresse = st.text_input("Adresse")
    telephone = st.text_input("Téléphone", placeholder="+237 6xx xxx xxx")
    email = st.text_input("Email", placeholder="exemple@gmail.com")

    st.subheader("Informations Commande")
    date_commande = st.date_input("Date de Commande")
    date_retour_prevue = st.date_input("Date de Retour Prévue")
    montant_total = st.number_input("Montant Total", min_value=0.0, step=0.01)
    remise = st.number_input("Remise", min_value=0.0, step=0.01)
    mode_paiement = st.selectbox("Mode de Paiement", ["Espèce", "Carte", "En ligne"])
    statut_commande = st.selectbox("Statut", ["En attente", "En cours", "Terminé", "Annulé"])

    st.subheader("Détails de l'Article")
    type_article = st.text_input("Type d'Article")
    matiere = st.text_input("Matière")
    couleur = st.text_input("Couleur")
    marque = st.text_input("Marque")
    taille = st.text_input("Taille")

    st.subheader("Service à Appliquer")
    cursor.execute("SELECT service_id, nom_service FROM Services")
    services = cursor.fetchall()

    nom_service = st.selectbox("Nom du Service", ["Nettoyage à eau", "Repassage", "Nettoyage à sec"])
    quantite = st.number_input("Quantité", min_value=1, step=1)
    prix_unitaire = st.number_input("Prix Unitaire", min_value=0.0, step=0.01)

    submit_button = st.form_submit_button("Ajouter la Commande")

# Traitement du formulaire
if submit_button:
    if not nom or not prenom or not adresse or not telephone or not email or montant_total == 0.0:
        st.error("Veuillez remplir tous les champs requis.")
    elif not validate_email(email):
        st.error("Email invalide.")
    elif not validate_telephone(telephone):
        st.error("Téléphone invalide. Format attendu : +237 6xx xxx xxx")
    else:
        try:
            conn.execute("BEGIN TRANSACTION")

            # Ajouter ou mettre à jour le client
            client_id, is_existing_client = process_client(nom, prenom, adresse, telephone, email)

            # Appliquer remise fidélité
            if is_existing_client:
                cursor.execute("SELECT points_fidelite FROM Clients WHERE client_id = ?", (client_id,))
                if cursor.fetchone()[0] >= 50:
                    remise = 500  # remise automatique

            # Insérer la commande
            cursor.execute("""
                INSERT INTO Commandes (client_id, date_commande, date_retour_prevue, montant_total, remise, mode_paiement, statut)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (client_id, date_commande, date_retour_prevue, montant_total, remise, mode_paiement, statut_commande))
            commande_id = cursor.lastrowid

            # Insérer l'article
            cursor.execute("""
                INSERT INTO Articles (commande_id, type_article, matiere, couleur, marque, taille)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (commande_id, type_article, matiere, couleur, marque, taille))
            article_id = cursor.lastrowid

            # Insérer le service
            cursor.execute("""
                INSERT INTO Lignes_Commande_Services (commande_id, article_id, service_id, quantite, prix_unitaire)
                VALUES (?, ?, ?, ?, ?)
            """, (commande_id, article_id, nom_service, quantite, prix_unitaire))

            conn.commit()
            st.success(f"Commande ajoutée avec succès pour {nom} {prenom} !")

        except Exception as e:
            conn.rollback()
            st.error(f"Erreur lors de l'ajout : {e}")
