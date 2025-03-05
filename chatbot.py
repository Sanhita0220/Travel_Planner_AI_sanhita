import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PDFMinerLoader
from langchain_text_splitters import NLTKTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough

# Load API Key
f = open("key.txt")
KEY = f.read()

# Set up Chatbot Prompt Template
chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful AI Travel Assistant. Provide travel-related answers based on user context. give a gentle reponse if the user asks out of the pdf content."),
    HumanMessagePromptTemplate.from_template("""
    Answer the question based on the given context.
    Context:
    {context}
    
    Question: 
    {question}
    
    Answer: """)
])

# Load AI Model
chat_model = ChatGoogleGenerativeAI(google_api_key=KEY, model="gemini-1.5-pro-latest")
output_parser = StrOutputParser()
chain = chat_template | chat_model | output_parser

# Load and Process Travel Guide Data
dat = PDFMinerLoader("AI Travel Planner user manual.pdf")  # travel guide PDF
dat_nik = dat.load()

text_splitter = NLTKTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(dat_nik)

embedding_model = GoogleGenerativeAIEmbeddings(google_api_key=KEY, model="models/embedding-001")
db = Chroma.from_documents(chunks, embedding_model, persist_directory="./chroma_db_")
db.persist()
db_connection = Chroma(persist_directory="./chroma_db_", embedding_function=embedding_model)
retriever = db_connection.as_retriever(search_kwargs={"k": 5})

# Format retrieved documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Define Chatbot RAG Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | chat_template
    | chat_model
    | output_parser
)

# Chatbot UI function
def chatbot_ui():
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    if st.button("💬 Travel Assistant"):
        st.session_state.chat_open = not st.session_state.chat_open  # Toggle chatbot visibility

    if st.session_state.chat_open:
        with st.sidebar:
            st.header("Ask the Travel Bot ✈️")
            user_input = st.text_area("Type your question here...")
            if st.button("Get Answer"):
                response = rag_chain.invoke(user_input)
                st.subheader("Answer:")
                st.write(response)
