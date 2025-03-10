import streamlit as st
from openai import OpenAI

# Set wide mode and page details
st.set_page_config(layout="wide", page_title="Stock Market Chat", page_icon="💹")

# Inject custom CSS for a stock market-themed style
st.markdown(
    """
    <style>
    /* Set a dark gradient background and light text for a trading vibe */
    .reportview-container {
        background: linear-gradient(to bottom, #0d1b2a, #1b263b);
        color: #e0e1dd;
    }
    /* Style the sidebar with a matching dark background */
    .sidebar .sidebar-content {
        background: #1b263b;
    }
    /* Customize the title appearance */
    .css-18e3th9 {  
        color: #f0a500;
    }
    /* Customize chat message containers for a ticker look */
    .chat-message {
        font-family: 'Courier New', Courier, monospace;
        border: 1px solid #f0a500;
        border-radius: 8px;
        padding: 10px;
        background-color: #1b263b;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Stock Market Chat Bot 💹")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model if not already defined
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "o1"

# Initialize chat history if not already defined
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's on your mind about the market?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
