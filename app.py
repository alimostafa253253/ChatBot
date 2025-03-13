from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
os.environ['LANGSMITH_API_KEY']=os.getenv('LANGSMITH_API_kEY')
os.environ['LANGSMITH_TRACING_V2']='true'
os.environ['LANGSMITH_PROJECT']='OllamaChatBot'

## prompt

prompt=ChatPromptTemplate.from_messages(
    [
        ('system','you are helpful assistant please answer as you can '),
        ('user','Question:{question}')
    ]
)

## Response Function
def generate_response(question,engine,temparture,max_tokens):
    
    llm=Ollama(model=engine)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

## Select the Ollama Model
engine=st.sidebar.selectbox("select Ollama AI model",['mistral','gemma:2b'])

## Adjust response parameter
temperature=st.sidebar.slider('Temperature',min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider('Max Tokens',min_value=50,max_value=300,value=150)

## Main interface for user input
st.write('Go ahead and ask any question')
user_input=st.text_input('You:')
 
if user_input:
    response=generate_response(user_input,engine,temperature,max_tokens)
    st.write(response)


else:
    st.write("Please provide the Question")    