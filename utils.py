from pathlib import Path
import streamlit as st
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from configs import *
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

FILE_FOLDER = Path(__file__).parent / 'files'

def import_documents():
    documents = []
    for file in FILE_FOLDER.glob('*.pdf'):
        loader = PyPDFLoader(str(file))
        file_documents = loader.load()
        documents.extend(file_documents)
        return documents
    
    
def split_documents(documents):
    recur_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        separators=["\n\n", "\n", " ", ""]
    )
    
    documents = recur_splitter.split_documents(documents)
    
    for i, doc in enumerate(documents):
        doc.metadata['source'] = doc.metadata['source'].split('/')[-1]
        doc.metadata['doc_id'] = i
    return documents


def create_vector_store(documents):
    embedding_model = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embedding_model
    )
    return vector_store


def create_chat_chain():
    
    documents = import_documents()
    documents = split_documents(documents)
    vector_store = create_vector_store(documents)
    
    chat = ChatOpenAI(model=get_config('model_name'))
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key='chat_history',
        output_key='answer')
    
    retriever = vector_store.as_retriever(
        search_type=get_config('retrieval_search_type'),
        search_kwargs=get_config('retrieval_kwargs')
    )
    
    prompt = PromptTemplate.from_template(get_config('prompt'))
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        memory=memory,
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
        combine_docs_chain_kwargs={'prompt': prompt}
    )
    
    st.session_state['chain'] = chat_chain


