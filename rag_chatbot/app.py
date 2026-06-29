import time
from datetime import datetime

import streamlit as st

from chatbot import ask_question

st.set_page_config(
    page_title="RAG Assistant",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 100%); }
    .block-container { padding-top: 1rem; }
    div[data-testid="stChatMessageContent"] {
        border-radius: 18px;
        padding: 0.8rem 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 0.35rem;
        animation: fadeIn 0.25s ease-in;
    }
    [data-testid="stSidebar"] { background: #f5f8ff; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🤖 Local RAG Chatbot")
st.caption("A warmer, more natural chat experience for your knowledge base.")

with st.sidebar:
    st.header("⚙️ Controls")
    st.write("This interface uses the local document snippets from the workspace.")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.conversation_context = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        st.caption(msg.get("timestamp", ""))

prompt = st.chat_input("Ask a question about the documents...")

if prompt:
    user_message = {
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M"),
    }
    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(user_message["timestamp"])

    with st.chat_message("assistant"):
        st.markdown("Typing...")
        time.sleep(1.2)
        response = ask_question(prompt)
        st.session_state.conversation_context.append(prompt)
        st.session_state.conversation_context.append(response)
        st.markdown(response)
        st.caption(datetime.now().strftime("%H:%M"))

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().strftime("%H:%M"),
        }
    )

st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)