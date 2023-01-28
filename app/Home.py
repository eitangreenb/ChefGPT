import streamlit as st
from utils import set_bg


st.set_page_config(layout="wide",
                   page_title="ChefGPT",
                   page_icon='assets/icon.png')
set_bg("assets/background_o.png")
st.markdown("# ChefGPT")
st.markdown("### A GPT-3 powered recipe generator")
st.write("###### Welcome to ChefGPT!\n" +
            "###### We're excited to help you discover new and delicious recipes to try out in the kitchen.\n" +
            "###### Whether you're a seasoned chef or just starting out, we have something for everyone.\n" +
            "###### Simply search for a recipe by ingredient or cuisine, and we'll provide you with a list of mouth-watering options to choose from.")
