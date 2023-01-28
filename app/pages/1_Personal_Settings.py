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
set_bg("assets/background_o.png")

col1, col2 = st.columns([1,2])
with col1:
    st.markdown("##### Before we start cooking, let's get to know you a little better.")
    st.markdown("##### What's your name?")
    name = st.text_input("Name", value="")
    st.markdown("##### Do you have any special diet?\nleave blank if not")
    diet = st.text_input("Diet", value="")
    st.markdown("##### Do you have any food allergies?\nleave blank if not")
    allergies = st.text_input("Allergies", value="")
    if allergies != "":
        allergies = allergies.split(", ")
    st.markdown("##### Please choose up to 3 favorite cuisines:")
    cuisines = st.multiselect("Cuisines", ["American", "Chinese", "French", "Indian", "Italian", "Japanese", "Korean", "Mexican", "Thai", "Vietnamese"])
    button = st.button("Submit",disabled=False)

    if button :
        if len(cuisines) <= 3:
            if "name" not in st.session_state:
                st.session_state["name"] = name
            if "diet" not in st.session_state:
                st.session_state["diet"] = diet
            if "allergies" not in st.session_state:
                st.session_state["allergies"] = allergies
            if "cuisines" not in st.session_state:
                st.session_state["cuisines"] = cuisines
            db_ref = db.collection("users").document(name)
            db_ref.set({
                "diet": diet,
                "allergies": allergies,
                "favorite cuisines": cuisines
            })
            st.success("Thank you for your input! You can now start cooking.")
        else:
            st.warning("You have to select up to 3 cuisines.")

with col2:
    pass
