from src.vectorstore.pinecone import init_vectorstore , load_documents
from src import config
from src.vectorstore.embeddings import load_embeddings


documents = load_documents(config.PROCESSED_DATA_DIR / "all_documents.json")
embeddings = load_embeddings()

def init_retriever():
    vectorstore = init_vectorstore(config.INDEX_NAME, documents, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    return retriever


