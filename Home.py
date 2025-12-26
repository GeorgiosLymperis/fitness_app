import streamlit as st
from core.db import init_db

init_db()

st.title("Home")
st.write("Welcome to the Fitness Tracker App!")