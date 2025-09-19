from pathlib import Path
import argparse
from typing import List
from pinecone import Pinecone, ServerlessSpec
from langchain.schema import Document
from src import config
from src.vectorstore.embeddings import load_embeddings
from src.vectorstore.pinecone import load_documents


def ensure_index(pc: Pinecone, index_name: str, dimension: int = 384, metric: str = "cosine") -> None:
    existing = {idx.name for idx in pc.list_indexes()}
    if index_name in existing:
        return
    pc.create_index(name=index_name, dimension=dimension, metric=metric, spec=ServerlessSpec(cloud="aws", region="us-east-1"))


def upsert_documents(index_name: str, docs: List[Document]) -> None:
    from langchain_pinecone import PineconeVectorStore
    embeddings = load_embeddings()
    PineconeVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        index_name=index_name,
        pinecone_api_key=config.PINECONE_API_KEY,
    )


def main(path: Path | None = None, index_name: str | None = None) -> None:
    config.ensure_env()
    data_path = path or (config.PROCESSED_DATA_DIR / "all_documents.json")
    name = index_name or config.INDEX_NAME

    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    ensure_index(pc, name)
    raw_docs = load_documents(data_path)
    upsert_documents(name, raw_docs)
    print(f"Indexed {len(raw_docs)} documents into '{name}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Pinecone index from processed documents")
    parser.add_argument("--path", type=str, default=str(config.PROCESSED_DATA_DIR / "all_documents.json"))
    parser.add_argument("--index_name", type=str, default=config.INDEX_NAME)
    args = parser.parse_args()
    main(Path(args.path), args.index_name)


