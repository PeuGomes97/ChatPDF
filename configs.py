import streamlit as st

MODEL_NAME = 'gpt-3.5-turbo-0125'
RETRIEVAL_SEARCH_TYPE = 'mmr'
RETRIEVAL_KWARGS = {'k': 5,  'fetch_k': 20}
PROMPT = """ Você é um chatbot que auxilia na interpretação de documentos que lhe são fornecidos.
No contexto fornecido estão as informações dos documentos do usuário. Utilize o contexto para responder as perguntas do usuário.
Se você não souber a resposta, apenas diga que não sabe e nao tente inventar uma resposta.

Contexto:
{context}

Conversa Atual:
{chat_history}
Human: {question}
AI:"""

# valor de {context} é o conjunto de trechos relevantes extraídos dos documentos que o retriever conseguiu localizar.

# Aqui está um fluxo simplificado para esclarecer:

# Usuário faz uma pergunta: Por exemplo, "Qual é o principal tema deste documento?"
# Retriever entra em ação: O retriever busca os trechos relevantes do PDF carregado, utilizando o vetor FAISS que foi criado com base nos embeddings.
# Preenchimento automático de {context}: O LangChain insere automaticamente esses trechos (o contexto) na posição {context} dentro do seu prompt.
# Geração da resposta: O modelo de linguagem (como o GPT) usa o PromptTemplate preenchido com o contexto, a conversa anterior e a nova pergunta, e gera a resposta.

def get_config(config_name):
    if config_name.lower() in st.session_state:
        return st.session_state[config_name.lower()]
    elif config_name.lower() == 'model_name':
        return MODEL_NAME
    elif config_name.lower() == 'retrieval_search_type':
        return RETRIEVAL_SEARCH_TYPE
    elif config_name.lower() == 'retrieval_kwargs':
        return RETRIEVAL_KWARGS
    elif config_name.lower() == 'prompt':
        return PROMPT
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#     No seu código, o preenchimento ocorre no momento em que a função ConversationalRetrievalChain.from_llm é criada, onde o retriever busca os documentos relevantes no vetor criado anteriormente. Aqui está a explicação do fluxo:

# ConversationalRetrievalChain: Quando você cria a cadeia de conversação com ConversationalRetrievalChain.from_llm, o retriever (que vem da função create_vector_store) busca documentos relacionados com base na pergunta do usuário. Os documentos relevantes são então agregados e passados para o prompt como o contexto.

# retriever: O retriever é responsável por encontrar documentos que são relevantes para a pergunta feita pelo usuário. Ele utiliza o modelo de embeddings e a base de dados FAISS para encontrar os trechos mais relevantes no PDF que foi carregado.

# Preenchimento da variável {context}: Quando o usuário faz uma pergunta (prompt), o LangChain invoca o retriever, que retorna os documentos relevantes. Esses documentos são usados para preencher o campo {context} do PromptTemplate.

# Aqui está o trecho principal do código onde isso acontece:

# python
# Copiar código
# chat_chain = ConversationalRetrievalChain.from_llm(
#     llm=chat,
#     memory=memory,
#     retriever=retriever,
#     return_source_documents=True,
#     verbose=True,
#     combine_docs_chain_kwargs={'prompt': prompt}
# )
# O parâmetro retriever é o mecanismo que vai buscar os trechos relevantes dos documentos (os vetores do PDF carregado).
# O PromptTemplate que você definiu, com as variáveis {context}, {chat_history}, e {question}, é alimentado quando o LangChain cria o encadeamento de conversação. O retriever encontra as informações relevantes para preencher {context}, e o histórico da conversa anterior preenche {chat_history}.
# Assim, quando o usuário envia uma nova pergunta ({question}), o LangChain busca os documentos relevantes, preenche o {context} com os trechos obtidos, e combina isso com o histórico de conversação para gerar uma resposta do modelo.

# Resumo do fluxo:
# O usuário faz uma pergunta.
# O retriever busca trechos relevantes nos documentos carregados (PDF).
# Esses trechos preenchem o campo {context} no PromptTemplate.
# A resposta é gerada usando o contexto e a conversa anterior.
# Se você quiser visualizar mais explicitamente o conteúdo que está sendo preenchido no {context}, você pode adicionar verbose=True ao ConversationalRetrievalChain para ver os documentos retornados no log.

# Isso responde sua dúvida sobre como o {context} está sendo preenchido?