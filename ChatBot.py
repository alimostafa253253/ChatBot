import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# LangSmith Tracking (use fallback defaults to prevent errors)
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY', 'your_default_api_key')
os.environ['LANGCHAIN_TRACKING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT', 'default_project')

# Define prompt template
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful assistant. Please respond to the question asked.'),
    ('user', "Question: {question}")
])

# Streamlit UI Setup
st.title('AI Q&A App using LangChain & Gemma! 🌟')
st.write("🚀 Ask any question, and get an **AI-powered** response using **LangChain & Gemma 2B**!")

# Add user guidance
st.info("💡 Example: 'What is machine learning?' or 'Tell me a fun fact about space!'")

# Initialize Ollama Model (Load once using session state)
if "llm" not in st.session_state:
    st.session_state.llm = Ollama(model="gemma:2b")

# Initialize Output Parser
output_parser = StrOutputParser()

# Create the chain
chain = prompt | st.session_state.llm | output_parser

# Get user input
input_text = st.text_input("💬 Type your question here:")

# Process input and display response
if input_text:
    try:
        response = chain.invoke({'question': input_text})
        st.success(response)  # Display output in a highlighted box
    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
