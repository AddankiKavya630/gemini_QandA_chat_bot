from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## Function yo load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history = [])

def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response

## Intialize our streamlit app

st.set_page_config("Gemini LLM Application")

st.header("Gemini LLM Application")
## Intialize the session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
    
input = st.text_input("Input:",key="input")
submit = st.button("Ask the Question")

if submit and input:
    response = get_gemini_response(input)
    ## Add user query and response to session chat history
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The Response is")
    bot = ''
    for chunk in response:
        bot += chunk.text
    st.write(bot)
    st.session_state['chat_history'].append(('Bot',bot))
st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")

