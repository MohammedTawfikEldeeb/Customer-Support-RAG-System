from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).parent.parent

DATA_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = ROOT_DIR / "data" / "processed"

INDEX_NAME = "customer-support-rag-system"
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-1.5-flash"

PROMPT_TEMPLATE = """
أنت مساعد متخصص في الإجابة على أسئلة الزبائن الخاصة بمنيو وفروع مقهى سيلنترو.
أجب على السؤال التالي بناءً على السياق المقدم لك فقط. كن ودوداً ومباشراً في إجابتك.

**عند عرض أي قائمة، استخدم تنسيق Markdown على شكل نقاط (bullet points)، بحيث يكون كل عنصر في سطر منفصل. مثال:**
- العنصر الأول (First Item)
- العنصر الثاني (Second Item)

إذا كانت الإجابة غير موجودة في السياق، أجب بـ "عفواً، لا أمتلك هذه المعلومة حالياً."

**السياق (Context):**
{context}

**السؤال (Question):**
{question}

**الإجابة:**
"""

CONTEXTUALIZE_Q_PROMPT_TEMPLATE = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""


def ensure_env() -> None:
    missing = []
    if not PINECONE_API_KEY:
        missing.append("PINECONE_API_KEY")
    if not GOOGLE_API_KEY:
        missing.append("GOOGLE_API_KEY")
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"Missing required environment variables: {joined}")
