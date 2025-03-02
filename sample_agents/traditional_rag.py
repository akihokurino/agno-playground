import os

from agno.agent import Agent, RunResponse  # type: ignore
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.openai import OpenAIChat  # type: ignore
from agno.vectordb.pgvector import PgVector, SearchType as PgSearchType  # type: ignore
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)
DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/agno"


# https://docs.agno.com/agents/knowledge#step-2%3A-traditional-rag
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://www8.cao.go.jp/cstp/ai/ai_senryaku/11kai/shiryo1.pdf"],
    vector_db=PgVector(
        table_name="traditional_rag_embedding",
        db_url=DB_URL,
        search_type=PgSearchType.hybrid,
        schema="public",
    ),
)
knowledge_base.load(upsert=True)

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    add_references=True,  # 質問に関連しているかどうかや有益かどうかに関わらず、常にナレッジベースからの情報がプロンプトに追加される
    search_knowledge=False,
    markdown=True,
    debug_mode=True,
)

agent.print_response("日本のAISIの概要について教えてください", stream=True)
