from typing import List
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from pinecone import Pinecone
from src.vectorstore.embeddings import load_embeddings
from src import config
import json
from pinecone import ServerlessSpec

def init_vectorstore(index_name: str,
                     lc_docs: List[Document],
                     embeddings,
                     dimension: int = 384,
                     metric: str = "cosine") -> PineconeVectorStore:
                     
    """Ensure a Pinecone index exists. Create it if missing."""
    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    existing = {idx.name for idx in pc.list_indexes()}
    if index_name not in existing:
        pc.create_index(name=index_name, dimension=dimension, metric=metric , spec=ServerlessSpec(cloud="aws", region="us-east-1"))
        vectorstore = PineconeVectorStore.from_documents(
            documents=lc_docs,
            embedding=embeddings,
            index_name=index_name,
            pinecone_api_key=config.PINECONE_API_KEY,
        )
    else:
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
    return vectorstore


def load_documents(path) -> List[Document]:
    with open(path, "r", encoding="utf-8") as f:
        raw_docs = json.load(f)
    return [
        Document(page_content=doc["page_content"], metadata=doc.get("metadata", {}))
        for doc in raw_docs
    ]
