import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

st.set_page_config(
    page_title="Pickie",
    page_icon="😒"
)

st.title("Pickie")

# configs
openai_api_key = st.secrets["OPENAI_API_KEY"]
avatars = {
    "user": "🧑‍💻",
    "ai": "😒"
}

# initialize
model = ChatOpenAI(api_key=openai_api_key, temperature=0.6, streaming=True)
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# business logic
def generate_response(user_message):
    messages = [
        SystemMessage("Answer the message."),
        HumanMessage(user_message),
    ]
    response = model.invoke(messages)
    return response.content

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

    ai_message = generate_response(message)
    store_ai_message(ai_message)
    render_ai_message(ai_message)