from src.vectorstore.pinecone import connect_vectorstore
from src import config
from src.vectorstore.embeddings import load_embeddings


_embeddings = None
_retriever = None

def get_retriever():
    global _embeddings, _retriever
    if _retriever is None:
        if _embeddings is None:
            _embeddings = load_embeddings()
        vectorstore = connect_vectorstore(config.INDEX_NAME, _embeddings)
        _retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    return _retriever


