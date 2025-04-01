import streamlit as st

password = st.secrets["PASSWORD"]

def render_content_not_authed():
    st.write("Hello, you need to sign in.")

    claimed = st.text_input("Enter the password.", type="password")

    if claimed == "":
        return

    if password == claimed:
        st.session_state["authed"] = True
        st.rerun()
    else:
        st.error("Wrong.")
