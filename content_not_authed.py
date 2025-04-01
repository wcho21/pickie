import streamlit as st

def render_content_not_authed():
    st.write("Hello, you need to sign in.")

    st.text_input("Enter the password.", type="password")