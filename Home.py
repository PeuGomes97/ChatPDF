import streamlit as st
from pathlib import Path
from utils import create_chat_chain, FILE_FOLDER
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

def sidebar():
    uloaded_pdfs = st.file_uploader(
        'Upload PDF file',
        type=['.pdf'],
        accept_multiple_files=True)
    if not uloaded_pdfs is None:
        for file in FILE_FOLDER.glob('*.pdf'):
            file.unlink()
        for pdf in uloaded_pdfs:
            with open(FILE_FOLDER / pdf.name, 'wb') as f:
                f.write(pdf.read())    
    
    button_label = 'Start Chatbot'
    if 'chain' in st.session_state:
        button_label = 'Update Chatbot'
    if st.button(button_label, use_container_width=True):
        if len(list(FILE_FOLDER.glob('*.pdf'))) == 0:
            st.error('Add .pdf files to start chatbot')
        else:
            st.success('Starting Chatbot ...')
            create_chat_chain()
            st.rerun()

def chat_window():
    st.markdown("""
        <style>
        .centered-header {
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="centered-header">Welcome to ChatPDF</h1>', unsafe_allow_html=True)
    
    if not 'chain' in st.session_state:
        st.error('Upload a .pdf file to start')
        st.stop()
    
    chain = st.session_state['chain']
    memory = chain.memory
    
    messages = memory.load_memory_variables({})['chat_history']
    
    container = st.container()
    for message in messages:
        chat = container.chat_message(message.type)
        chat.markdown(message.content)
    
    new_message = st.chat_input('Type your prompt...')
    if new_message:
        chat = container.chat_message('human')
        chat.markdown(new_message)
        chat = container.chat_message('ai')
        chat.markdown('Waiting for response ...')
        
        
        response = chain.invoke({'question': new_message})
        st.session_state['last_message'] = response
        st.rerun()
    
    
    

def main():
    with st.sidebar:
        sidebar()
    chat_window()    
    
if __name__=='__main__':
    main()
    
    