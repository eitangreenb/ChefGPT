import streamlit as st
import openai
from google.cloud import firestore
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import random
from utils import set_bg
import json


with open('secrets.json', 'r') as file:
    config = json.load(file)
FIREBASE_JSON = config['FIREBASE_JSON']
OPENAI_KEY = config['OPENAI_KEY']



db = firestore.Client.from_service_account_json(FIREBASE_JSON)

openai.api_key = OPENAI_KEY

def get_response(prompt):

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.9,
    max_tokens=400,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    )
    return response.choices[0].text

def get_prompt(input):
    r = f"give me a recipe for {input}."
    if diet:
        r+= f" I'm on a {diet} diet."
    if allergies:
        r+= f" I'm allergic to {allergies}."
    return r


def get_modified_prompt(input):
    r = get_prompt(st.session_state.get("user_input", None))
    r += f" {input}."
    return r


def get_cuisine_prompt(input, num=4):
    r = f"Can you suggest {num} dishes from {input} cuisine?"
    return r


def get_surprise():
    name = st.session_state["name"]
    all_users = db.collection('users').get()
    all_data = {}
    diets = set()
    allergies = set()
    cuisines = set()
    for user in all_users:
        user_recipes = db.collection('users').document(user.id).collection('recipes').document('favorites').get().to_dict()
        user_info = db.collection('users').document(user.id).get().to_dict()
        user_allergies, user_diet, user_fav_cuisines = parse_user_dict(user_info)
        all_data[user.id] = [user_allergies, user_diet, user_fav_cuisines, user_recipes]
        diets.add(user_diet)
        allergies.update(user_allergies)
        cuisines.update(user_fav_cuisines)
    if '' in diets:
        diets.remove('')
    columns = list(diets) + list(allergies) + list(cuisines)
    df = pd.DataFrame(columns=columns)
    for user in all_data:
        if user != name and not all_data[user][3]:
            continue
        df.loc[user] = [0]*len(columns)
        for allergy in all_data[user][0]:
            df.loc[user][allergy] = 1
        if all_data[user][1]:
            df.loc[user][all_data[user][1]] = 1
        for cuisine in all_data[user][2]:
            df.loc[user][cuisine] = 1
    
    row_to_compare = df.loc[name].values
    df.drop(name, inplace=True)
    similarities = cosine_similarity(df.values, row_to_compare.reshape(1, -1))
    top_5_indices = (-similarities[:, 0]).argsort()[:5]
    top_5_users = df.iloc[top_5_indices].index
    recipes_to_choose_from = []
    for user in top_5_users:
        recipes_to_choose_from.extend(list(all_data[user][3].values()))

    result = random.choice(recipes_to_choose_from)
    return result

def parse_user_dict(user_dict):
    allergies = user_dict['allergies']
    diet = user_dict['diet']
    fav_cuisines = user_dict['favorite cuisines']
    return allergies, diet, fav_cuisines



st.set_page_config(layout="wide",
                   page_title="ChefGPT",
                   page_icon='assets/icon.png')
set_bg("assets/background_c.png")
st.markdown("# ChefGPT")
st.markdown("### A GPT-3 powered recipe generator")


col1, col2 = st.columns([1, 2])
col1.header("Ask for a recipe")
col2.header("Recipe")

with st.sidebar:
    name = st.session_state.get("name", None)
    if name:
        db_ref = db.collection('users').document(name)
        data = db_ref.get().to_dict()
        favorites = db_ref.collection('recipes').document('favorites').get().to_dict()
        allergies = data['allergies']
        diet = data['diet']
        fav_cuisines = data['favorite cuisines']
        st.write(f"Welcome back, {name}!")
        if diet:
            st.write(f"Diet: {diet}")
        if allergies:
            st.write(f"Allergies: {(', ').join(allergies)}")
        st.write(f"Favroite cuisines: {(', ').join(fav_cuisines)}")

        if not favorites:
            st.write("You have no saved recipes!")
        else:
            st.write(f"You have saved {len(favorites)} recipes!")


if "current_recipe" not in st.session_state:
    st.session_state['current_recipe'] = ""

if "user_input" not in st.session_state:
    st.session_state['user_input'] = ""

if "disable_save" not in st.session_state:
    st.session_state['disable_save'] = True

if "disable_get_recipe" not in st.session_state:
    st.session_state['disable_get_recipe'] = False

if "disable_modify" not in st.session_state:
    st.session_state['disable_modify'] = True

if "disable_new" not in st.session_state:
    st.session_state['disable_new'] = True

if "disable_get_cuisine" not in st.session_state:
    st.session_state['disable_get_cuisine'] = False

if "disable_more" not in st.session_state:
    st.session_state['disable_more'] = True

if "disable_get_recipe2" not in st.session_state:
    st.session_state['disable_get_recipe2'] = True

if "disable_modify2" not in st.session_state:
    st.session_state['disable_modify2'] = True

if "disable_new2" not in st.session_state:
    st.session_state['disable_new2'] = True

if "disable_modify3" not in st.session_state:
    st.session_state['disable_modify3'] = True

with col1:
    ask_for_recipe_tab, ask_for_cuisine_tab, surprise_me_tab = st.tabs(["Ask for a recipe", "Ask for a cuisine", "Surprise me!"])

with col2:
    recipe_placeholder = st.empty()
    recipe_placeholder.write(st.session_state['current_recipe'])
    save = st.button("Save", "s1", disabled=st.session_state['disable_save'])
    if save:
        if "user_input" not in st.session_state or not st.session_state['user_input']:
            st.error("Please ask for a recipe first!")
        else:
            doc_ref = db.collection('users').document(name).collection('recipes').document("favorites")
            doc_ref.set({
                st.session_state['user_input'].replace(" ", "_"): st.session_state['current_recipe']
                }, merge=True)
            st.success("You saved the recipe!")

with ask_for_recipe_tab:
    placeholder = st.empty()
    if not st.session_state['disable_get_recipe']:
        user_input_text = "Ask for a recipe"
    elif st.session_state['disable_get_recipe']:
        user_input_text = "You can now ask for a modification"
    user_input = placeholder.text_input(user_input_text, key="t1")
    get_recipe_button = st.button("Get Recipe", "g1", disabled=not user_input or st.session_state['disable_get_recipe'])
    modify = st.button("Modify", "m1", disabled=st.session_state['disable_modify'])
    new = st.button("New", "n1", disabled=st.session_state['disable_new'])
    
    if get_recipe_button:
        st.success(f"You asked for {user_input}")
        response = get_response(get_prompt(user_input))
        st.session_state['user_input'] = response.lstrip("\n").split("\n")[0].rstrip(" ").rstrip(":")
        st.session_state['current_recipe'] = response
        recipe_placeholder.write(response)
        st.session_state['disable_get_recipe'] = True
        st.session_state['disable_modify'] = False
        st.session_state['disable_new'] = False
        st.session_state['disable_save'] = False
        st.experimental_rerun()

    if new:
        recipe_placeholder.write("")
        user_input = placeholder.text_input("Ask for a new recipe")
        st.session_state['disable_get_recipe'] = False
        st.session_state['disable_modify'] = True
        st.session_state['disable_new'] = True
        st.session_state['disable_save'] = True
        st.session_state['user_input'] = ""
        st.session_state['current_recipe'] = ""
        st.experimental_rerun()

    if modify:
        st.success(f"You asked for {user_input}")
        response = get_response(get_modified_prompt(user_input))
        st.session_state['current_recipe'] = response
        recipe_placeholder.write(response)
      

with ask_for_cuisine_tab:
    cuisine_placeholder = st.empty()
    if not st.session_state['disable_get_cuisine']:
        user_input_text = "Ask for a cuisine"
    elif st.session_state['disable_get_cuisine'] and not st.session_state['disable_get_recipe2']:
        user_input_text = "Choose a dish"
    elif st.session_state['disable_get_recipe2']:
        user_input_text = "You can now ask for a modification"
    user_input = cuisine_placeholder.text_input(user_input_text, key="t2")
    get_cuisine_button = st.button("Get Cuisine", "c2", disabled=not user_input or st.session_state['disable_get_cuisine'])
    more = st.button("More", "more_dishes", disabled=st.session_state['disable_more'])
    get_recipe_button = st.button("Get Recipe", "g2", disabled=not user_input or st.session_state['disable_get_recipe2'])
    modify = st.button("Modify", "m2", disabled=st.session_state['disable_modify2'])
    new = st.button("New", "n2", disabled=st.session_state['disable_new2'])
    
    if get_cuisine_button:
        st.success(f"You asked for {user_input}")
        response = get_response(get_cuisine_prompt(user_input))
        recipe_placeholder.write(response)
        st.session_state['current_recipe'] = response
        st.session_state['user_input'] = user_input
        st.session_state['disable_get_cuisine'] = True
        st.session_state['disable_more'] = False
        st.session_state['disable_get_recipe2'] = False
        st.session_state['disable_modify2'] = True
        st.session_state['disable_new2'] = False
        st.session_state['disable_save'] = True
        st.experimental_rerun()

    if more:
        st.success(f"You asked for more {st.session_state['user_input']} dishes")
        response = get_response(get_cuisine_prompt(st.session_state['user_input'], 8))
        st.session_state['current_recipe'] = response
        recipe_placeholder.write(response)
    
    if get_recipe_button:
        st.success(f"You asked for {user_input}")
        response = get_response(get_prompt(user_input))
        st.session_state['user_input'] = response.lstrip("\n").split("\n")[0].rstrip(" ").rstrip(":")
        st.session_state['current_recipe'] = response
        recipe_placeholder.write(response)
        st.session_state['disable_get_cuisine'] = True
        st.session_state['disable_more'] = True
        st.session_state['disable_get_recipe2'] = True
        st.session_state['disable_modify2'] = False
        st.session_state['disable_new2'] = False
        st.session_state['disable_save'] = False
        st.experimental_rerun()

    if new:
        recipe_placeholder.write("")
        user_input = cuisine_placeholder.text_input("Ask for a new recipe")
        st.session_state['disable_get_cuisine'] = False
        st.session_state['disable_more'] = True
        st.session_state['disable_get_recipe2'] = True
        st.session_state['disable_modify2'] = True
        st.session_state['disable_new2'] = True
        st.session_state['disable_save'] = True
        st.session_state['user_input'] = ""
        st.session_state['current_recipe'] = ""
        st.experimental_rerun()

    if modify:
        st.success(f"You asked for {user_input}")
        response = get_response(get_modified_prompt(user_input))
        st.session_state['current_recipe'] = response
        recipe_placeholder.write(response)


with surprise_me_tab:
    surprise_button = st.button("Surprise me!", "surprise")
    surprise_placeholder = st.empty()
    user_input = surprise_placeholder.text_input("You can now ask for a modification", key="t3", disabled=st.session_state['disable_modify3'])
    modify = st.button("Modify", "m3", disabled=st.session_state['disable_modify3'])

    if surprise_button:
        st.success("You asked for a surprise!")
        response = get_surprise()
        st.session_state['user_input'] = response.lstrip("\n").split("\n")[0].rstrip(" ").rstrip(":")
        st.session_state['current_recipe'] = response
        
        recipe_placeholder.write(response)
        st.session_state['disable_modify3'] = False
        st.experimental_rerun()


    if modify:
        st.success(f"You asked for {user_input}")
        response = get_response(get_modified_prompt(st.session_state['user_input']))
        st.session_state['current_recipe'] = response
        recipe_placeholder.write(response)
