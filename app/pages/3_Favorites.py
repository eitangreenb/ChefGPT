import streamlit as st
from google.cloud import firestore
from utils import set_bg
import json

with open('secrets.json', 'r') as file:
    config = json.load(file)
FIREBASE_JSON = config['FIREBASE_JSON']

db = firestore.Client.from_service_account_json(FIREBASE_JSON)

st.set_page_config(layout="wide",
                   page_title="ChefGPT",
                   page_icon='assets/icon.png')
set_bg("assets/background_f.png")

with st.sidebar:
    name = st.session_state.get("name", None)
    if name:
        db_ref = db.collection('users').document(name)
        data = db_ref.get().to_dict()
        favorites = db_ref.collection('recipes').document('favorites').get().to_dict()
        allergies = data['allergies']
        diet = data['diet']
        st.write(f"Welcome back, {name}!")
        if diet:
            st.write(f"Diet: {diet}")
        if allergies:
            st.write(f"Allergies: {(', ').join(allergies)}")
        st.write(f"Favroite cuisines: {(', ').join(data['favorite cuisines'])}")

        if not favorites:
            st.write("You have no saved recipes!")
        else:
            st.write(f"You have saved {len(favorites)} recipes!")


doc_ref = db.collection('users').document(name).collection('recipes').document("favorites")

col1, col2 = st.columns([1,2])
with col1:
    st.markdown("##### Here you can see all your favorite recipes.")
    st.markdown("##### You can also remove recipes from your favorites.")
    st.markdown("##### Enjoy!")
    favorites = doc_ref.get().to_dict()
    recipe_names = list(favorites.keys())
    for i in range(len(recipe_names)):
        recipe_names[i] = recipe_names[i].replace("_", " ")
    recipe_name = st.selectbox("Select a recipe", sorted(recipe_names))
    button = st.button("Remove from favorites",disabled=False)
    if button:
        doc_ref.update({
            recipe_name.replace(" ", "_"): firestore.DELETE_FIELD
        })
        st.success("Recipe removed from favorites.")

with col2:
    st.markdown("##### Recipe:")
    if recipe_name:
        st.markdown(favorites[recipe_name.replace(" ", "_")])
            