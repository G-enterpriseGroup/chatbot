import streamlit as st
from openai import OpenAI

st.title("You should not be here, I will track your IP address, LEAVE!")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "o1"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to compute cost breakdown
def compute_cost():
    new_input_word_count = 0
    cached_input_word_count = 0
    seen_user_messages = set()

    # Process user messages: treat duplicates as cached
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
    output_word_count = 0
    for m in st.session_state.messages:
        if m["role"] == "assistant":
            words = m["content"].split()
            output_word_count += len(words)
    
    # Cost breakdown based on per word pricing:
    # New Input: $0.00002 per word
    # Cached Input: $0.00001 per word
    # Output: $0.00008 per word
    new_input_cost = new_input_word_count * 0.00002
    cached_input_cost = cached_input_word_count * 0.00001
    output_cost = output_word_count * 0.00008
    net_cost = new_input_cost + cached_input_cost + output_cost

    return new_input_cost, cached_input_cost, output_cost, net_cost

# Sidebar: display the cost breakdown
with st.sidebar:
    st.header("Cost Breakdown")
    new_cost, cached_cost, out_cost, net_cost = compute_cost()
    st.write(f"New Input Cost: ${new_cost:.6f}")
    st.write(f"Cached Input Cost: ${cached_cost:.6f}")
    st.write(f"Output Cost: ${out_cost:.6f}")
    st.write(f"Net Charge: ${net_cost:.6f}")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
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
