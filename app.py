import streamlit as st
import time

st.set_page_config(
    page_title="Pickie",
    page_icon="😒"
)

st.title("Pickie")

# configs
avatars = {
    "user": "🧑‍💻",
    "ai": "😒"
}

# initialize
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

def store_user_message(message):
    store_message(message, "user")

def store_ai_message(message):
    store_message(message, "ai")

def store_message(message, role):
    st.session_state["message_history"].append({ "message": message, "role": role })

def render_user_message(message):
    render_message(message, "user")

def render_ai_message(message):
    render_message(message, "ai")

def render_message(message, role):
    avatar = avatars[role]

    with st.chat_message(role, avatar=avatar):
        st.write(message)

def render_message_history():
    for item in st.session_state["message_history"]:
        message = item["message"]
        role = item["role"]
        render_message(message, role)

message = st.chat_input("Send a message")
if message:
    render_message_history()

    store_user_message(message)
    render_user_message(message)

    time.sleep(1)

    ai_message="Some AI response"
    store_ai_message(ai_message)
    render_ai_message(ai_message)