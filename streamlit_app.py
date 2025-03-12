import streamlit as st
from openai import OpenAI

st.title("🏎️💨SKRT SKRT!")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Available GPT model options
model_options = ["gpt-3.5-turbo", "gpt-4","GPT-4o mini", "o1"]

# Initialize model selection in session state if not present
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model_options[0]  # default

# Sidebar: Model selection dropdown and cost breakdown
with st.sidebar:
    selected_model = st.selectbox("Choose GPT Model", model_options, index=model_options.index(st.session_state["openai_model"]))
    st.session_state["openai_model"] = selected_model

# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

def compute_cost():
    """
    Computes cost based on the following pricing per word:
    - New Input: $0.00002
    - Cached Input: $0.00001
    - Output: $0.00008

    Cached input is defined as user messages that have appeared before.
    """
    new_input_word_count = 0
    cached_input_word_count = 0
    seen_user_messages = set()

    # Process user messages: treat duplicates as cached input
    for m in st.session_state.messages:
        if m["role"] == "user":
            words = m["content"].split()
            count = len(words)
            if m["content"] in seen_user_messages:
                cached_input_word_count += count
            else:
                new_input_word_count += count
                seen_user_messages.add(m["content"])

    # Process assistant messages (all count as output)
    output_word_count = sum(len(m["content"].split()) for m in st.session_state.messages if m["role"] == "assistant")

    new_input_cost = new_input_word_count * 0.00002
    cached_input_cost = cached_input_word_count * 0.00001
    output_cost = output_word_count * 0.00008
    net_cost = new_input_cost + cached_input_cost + output_cost

    return new_input_cost, cached_input_cost, output_cost, net_cost

# Display chat history so far
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Generate assistant response and display in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Update sidebar with cost breakdown using the updated chat history
with st.sidebar:
    st.header("Cost Breakdown")
    new_cost, cached_cost, out_cost, net_cost = compute_cost()
    st.write(f"New Input Cost: ${new_cost:.6f}")
    st.write(f"Cached Input Cost: ${cached_cost:.6f}")
    st.write(f"Output Cost: ${out_cost:.6f}")
    st.write(f"Net Charge: ${net_cost:.6f}")
