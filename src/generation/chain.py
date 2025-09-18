from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src import config
from src.retrieval.semantic_retrieval import init_retriever


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def init_rag_chain():
    retriever = init_retriever()
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    prompt = ChatPromptTemplate.from_template(config.PROMPT_TEMPLATE)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

