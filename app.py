import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Configurat
st.set_page_config(
    page_title="Jupiter Money Q&A Bot 🤖",
    page_icon="🤖",
    layout="wide"
)

# Vector Store
DB_FAISS_PATH = "vectorstore/db_faiss"
MODEL_NAME_EMBEDDINGS = 'sentence-transformers/all-MiniLM-L6-v2'
MODEL_NAME_LLM = 'google/flan-t5-large'

@st.cache_resource
def load_resources():
    """
    Load the embedding model and the FAISS vector store.
    This function is cached to avoid reloading on every user interaction.
    """
    st.write("Loading resources... This may take a moment.")
    
    # embeddin model
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME_EMBEDDINGS,
        model_kwargs={'device': 'cpu'}
    )
    
    # vec store
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

    # LLM
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_LLM)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME_LLM)
    
    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=512,
        torch_dtype=torch.bfloat16 
    )
    
    llm = HuggingFacePipeline(pipeline=pipe)
    st.write("Resources loaded successfully!")
    return db, llm

try:
    db, llm = load_resources()
except Exception as e:
    st.error(f"Failed to load resources. Please ensure the vector store exists at '{DB_FAISS_PATH}'. Error: {e}")
    st.stop()


def create_qa_chain(db, llm):
    """
    Create the RetrievalQA chain.
    """
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=db.as_retriever(search_kwargs={'k': 3}), # Retrieve top 3 chunks
        return_source_documents=True
    )

qa_chain = create_qa_chain(db, llm)


st.title("Jupiter Money Q&A Bot 🤖")
st.markdown("Ask any question about Jupiter Money's products, services, or fees, and get answers based on their official website.")

if 'history' not in st.session_state:
    st.session_state['history'] = []

user_question = st.text_input("Your Question:", key="input_question")

if user_question:
    with st.spinner("Thinking..."):
        try:
            result = qa_chain({'query': user_question})
            answer = result.get('result')
            source_documents = result.get('source_documents', [])

            st.session_state['history'].insert(0, (user_question, answer, source_documents))
        
        except Exception as e:
            st.error(f"An error occurred: {e}")


st.subheader("Conversation")
if not st.session_state['history']:
    st.info("Ask a question to start the conversation.")
else:
    for i, (question, answer, sources) in enumerate(st.session_state['history']):
        with st.container():
            st.markdown(f"**You:** {question}")
            st.markdown(f"**Bot:** {answer}")
            
            with st.expander("Show Sources"):
                for doc in sources:
                    st.markdown(f"**Source:** `{doc.metadata.get('source', 'N/A')}`") # Assuming you might add source metadata later
                    st.markdown(f"```\n{doc.page_content}\n```")
            st.markdown("---")