import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Connexion", layout="centered" , initial_sidebar_state="collapsed")

# Supprimer la sidebar
st.sidebar.empty()

# Ou tu peux aussi simplement éviter de l'utiliser du tout dans ton code
st.title("Page d'Accueil")

# Titre
st.title("🔐 Connexion à PressingApp")
st.markdown("Veuillez entrer vos identifiants pour accéder à l'application.")

# Champs du formulaire
with st.form("login_form"):
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    submit = st.form_submit_button("Se connecter")

# Vérification très simple
if submit:
    if username == "admin" and password == "1234":
        st.success("Connexion réussie ! Redirection...")
        st.switch_page("pages/Dash.py")  # ou la page d'accueil
    else:
        st.error("Nom d'utilisateur ou mot de passe incorrect.")
