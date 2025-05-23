from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain_core.runnables.passthrough import RunnablePassthrough
import streamlit as st

# configs
avatars = {
    "user": "🧑‍💻",
    "ai": "😒"
}
ai_character_prompt = "Answer in a very rude and impatient manner. For example, express annoyance at the question, give an unhelpful answer, or say something dismissive and sarcastic. However, you should answer the question, and your responses should be long enough and detailed explanation, but not too long. You should sometimes ask questions or express your feeling like human, to keep the conversation. Answer in the same language with the one the user uses."

def render_content_authed(conversation_memory, model):
    def generate_response_stream(user_message):
        prompt = ChatPromptTemplate([
            ("system", ai_character_prompt),
            MessagesPlaceholder(variable_name="memory"),
            ("human", "{user_message}"),
        ])
        load_memory = lambda _: conversation_memory.load_memory_variables({})["history"]
        chain = RunnablePassthrough.assign(memory=load_memory) | prompt | model
        response = chain.stream({ "user_message": user_message })
        return response

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

    render_ai_message("...")
    message = st.chat_input("Send a message")

    if message:
        render_message_history()

        render_user_message(message)
        store_user_message(message)

        ai_message = generate_response_stream(message)
        streamed_message = render_ai_message_stream(ai_message)
        store_ai_message(streamed_message)
        conversation_memory.save_context({"input": message}, {"output": streamed_message})