from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from src.generation.chain import init_rag_chain  # استخدام السلسلة الأساسية الخاصة بك
import uvicorn
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI(title="Customer Support RAG System")

# تحميل الملفات الثابتة
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")


rag_chain = init_rag_chain()



llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}"),
])
rephrase_chain = contextualize_q_prompt | llm | StrOutputParser()



chat_history = []

@app.get("/", response_class=HTMLResponse)
def welcome(request: Request):
    global chat_history
    chat_history = []
    return templates.TemplateResponse("index.html", {"request": request})

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query(payload: QueryRequest):
    global chat_history

    standalone_question = rephrase_chain.invoke({
        "chat_history": chat_history,
        "question": payload.question
    })

    response = rag_chain.invoke(standalone_question)
    
    chat_history.extend([
        HumanMessage(content=payload.question),
        AIMessage(content=response) 
    ])
    
    chat_history = chat_history[-6:]
    
    return {"message": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

