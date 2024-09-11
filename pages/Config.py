import json
import streamlit as st
from configs import *
from utils import FILE_FOLDER, create_chat_chain

def config_page():
    st.header("Config RAG based on your preference", divider=True)
    
    model_name = st.text_input("Choose model", value=get_config('model_name'))
    retrieval_search_type = st.text_input("Set Retrieval type", value=get_config('retrieval_search_type'))
    retrieval_kwargs = st.text_input("Set Retrieval params", value=get_config('retrieval_kwargs'))
    prompt = st.text_area("Update default prompt", height=350, value=get_config('prompt'))
    
    if st.button("Change Parameters!", use_container_width=True):
        retrieval_kwargs = json.loads(retrieval_kwargs.replace("'", '"'))
        st.session_state['model_name'] = model_name
        st.session_state['retrieval_search_type'] = retrieval_search_type
        st.session_state['retrieval_kwargs'] = retrieval_kwargs
        st.session_state['prompt'] = prompt
    
    if st.button("Update Chatbot", use_container_width=True):
        if len(list(FILE_FOLDER.glob('*.pdf'))) == 0:
            st.error("Add .pdf file to star conversation!")
        else:
            st.success("Starting Conversation...")
            create_chat_chain()
            st.rerun()    
                
config_page()