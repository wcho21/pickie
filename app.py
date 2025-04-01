import streamlit as st
from content_authed import render_content_authed

st.set_page_config(
    page_title="Pickie",
    page_icon="😒"
)

st.title("Pickie")

render_content_authed()