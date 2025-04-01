import streamlit as st
from langchain.memory import ConversationSummaryBufferMemory
from content_authed import render_content_authed
from content_not_authed import render_content_not_authed
from langchain_openai import ChatOpenAI

# initialize
openai_api_key = st.secrets["OPENAI_API_KEY"]
model = ChatOpenAI(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0.6, streaming=True)
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
if "conversation_memory" not in st.session_state:
    st.session_state["conversation_memory"] = ConversationSummaryBufferMemory(llm=model, max_token_limit=200, return_messages=True)
conversation_memory = st.session_state["conversation_memory"]

st.set_page_config(
    page_title="Pickie",
    page_icon="😒"
)

st.title("Pickie")

if "authed" not in st.session_state:
    st.session_state["authed"] = False
authed = st.session_state["authed"]

if authed:
    render_content_authed(conversation_memory, model)
else:
    render_content_not_authed()