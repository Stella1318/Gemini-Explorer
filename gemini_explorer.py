import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

# Initialize Vertex AI
project = "gemini-explorer-428322"
vertexai.init(project=project)

# Configure a baseline generative AI model
config = generative_models.GenerationConfig(
    temperature=0.6
)
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)
chat = model.start_chat()

# Function to handle user input and model response
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "model", "content": output})

# Streamlit app layout
st.title("geminiExplorer")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history    
for index, message in enumerate(st.session_state.messages):
    content = Content(role=message["role"], parts=[Part.from_text(message["content"])])
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    chat.history.append(content)

# Capture User Query
query = st.chat_input("geminiExplorer")
if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)
