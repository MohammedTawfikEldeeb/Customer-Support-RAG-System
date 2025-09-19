from typing import List
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from pinecone import Pinecone
from src import config
import json

def connect_vectorstore(index_name: str, embeddings) -> PineconeVectorStore:
    """Connect to an existing Pinecone index. Do not create at runtime."""
    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    existing = {idx.name for idx in pc.list_indexes()}
    if index_name not in existing:
        raise RuntimeError(f"Pinecone index '{index_name}' not found. Build it via the offline job before starting the API.")
    return PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)


def load_documents(path) -> List[Document]:
    with open(path, "r", encoding="utf-8") as f:
        raw_docs = json.load(f)
    return [
        Document(page_content=doc["page_content"], metadata=doc.get("metadata", {}))
        for doc in raw_docs
    ]
