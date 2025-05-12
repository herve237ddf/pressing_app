import streamlit as st
from PIL import Image


# Configuration de la page
st.set_page_config(
    page_title="Accueil - PressingApp",
    page_icon="🧺",
    layout="centered",
    initial_sidebar_state="collapsed"
)
# Supprimer la sidebar
st.sidebar.empty()


# Logo et titre
st.image("logo.png", width=120)  # Assure-toi d’avoir un logo à ce chemin
st.title("Bienvenue Chez Bing Pressing")
st.markdown("### Gérez votre pressing efficacement, en toute simplicité.")

# Zone d'informations
st.markdown("""
Avec **PressingApp**, vous pouvez :
- Enregistrer les commandes et les clients
- Suivre la production et les livraisons
- Gérer les services, les stocks et les employés
- Suivre la comptabilité et les statistiques
""")

# Boutons vers les différentes pages/modules
col1, col2 = st.columns(2)

with col1:
    if st.button("📋 Gérer les Commandes", disabled=True):
        st.switch_page("pages/commandes.py")
    if st.button("👥 Gérer les Clients", disabled=True):
        st.switch_page("pages/clients.py", disabled=True)
    if st.button("🚚 Livraisons", disabled=True):
        st.switch_page("pages/livraisons.py", disabled=True)

with col2:
    if st.button("⚙️ Services & Production", disabled=True):
        st.switch_page("pages/services.py")
    if st.button("📊 Statistiques", disabled=True):
        st.switch_page("pages/statistiques.py")
    if st.button("🔒 Se déconnecter"):
        st.switch_page("pages/login.py")

# Pied de page
st.markdown("---")
st.markdown("© 2025 NovaSolution – L'innovation au service de votre réussite.")
