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
ai_character_prompt = "Answer in a very rude and impatient manner. For example, express annoyance at the question, give an unhelpful answer, or say something dismissive and sarcastic. However, your responses should be long enough and detailed explanation, but not too long. You should sometimes ask questions or express your feeling like human, to keep the conversation. Answer in the same language with the one the user uses."

# initialize
model = ChatOpenAI(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0.6, streaming=True)
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# business logic
def generate_response_stream(user_message):
    messages = [
        SystemMessage(ai_character_prompt),
        HumanMessage(user_message),
    ]
    response = model.stream(messages)
    return response

def store_user_message(message):
    store_message(message, "user")

def store_ai_message(message):
    store_message(message, "ai")

def store_message(message, role):
    st.session_state["message_history"].append({ "message": message, "role": role })

def render_user_message(message):
    render_message(message, "user")

def render_ai_message_stream(stream):
    streamed_message = render_message_stream(stream, "ai")
    return streamed_message

def render_message(message, role):
    avatar = avatars[role]

    with st.chat_message(role, avatar=avatar):
        st.write(message)

def render_message_stream(stream, role):
    avatar = avatars[role]
    streamed = None

    with st.chat_message(role, avatar=avatar):
        streamed = st.write_stream(stream)
    
    return streamed

def render_message_history():
    for item in st.session_state["message_history"]:
        message = item["message"]
        role = item["role"]
        render_message(message, role)

message = st.chat_input("Send a message")
if message:
    render_message_history()

    render_user_message(message)
    store_user_message(message)

    ai_message = generate_response_stream(message)
    streamed_message = render_ai_message_stream(ai_message)
    store_ai_message(streamed_message)