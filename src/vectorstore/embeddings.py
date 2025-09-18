from langchain_community.embeddings import HuggingFaceEmbeddings

def load_embeddings(model_name: str = "intfloat/multilingual-e5-small"):
    return HuggingFaceEmbeddings(model_name=model_name)