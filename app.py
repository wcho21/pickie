import streamlit as st
from content_authed import render_content_authed
from content_not_authed import render_content_not_authed

st.set_page_config(
    page_title="Pickie",
    page_icon="😒"
)

st.title("Pickie")

if "authed" not in st.session_state:
    st.session_state["authed"] = False
authed = st.session_state["authed"]

if authed:
    render_content_authed()
else:
    render_content_not_authed()