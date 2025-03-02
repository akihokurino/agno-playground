import os

from agno.agent import Agent, RunResponse  # type: ignore
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.models.openai import OpenAIChat  # type: ignore
from agno.vectordb.pgvector import PgVector, SearchType as PgSearchType  # type: ignore
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)
DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/agno"

# https://docs.agno.com/agents/knowledge
# https://docs.agno.com/agents/memory
knowledge_base = PDFKnowledgeBase(
    path="local_pdf.pdf",
    vector_db=PgVector(
        table_name="local_rag_embedding",
        db_url=DB_URL,
        search_type=PgSearchType.hybrid,
        schema="public",
    ),
)
knowledge_base.load(upsert=True)

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge_base,
    add_references=False,
    search_knowledge=True,  # ナレッジベースにアクセスする必要があるかどうか、またどの検索パラメータを使ってナレッジベースを検索するかを自ら判断する
    read_chat_history=True,  # チャット履歴を読み取る
    show_tool_calls=True,  # get_chat_history()を利用するため
    markdown=True,
    debug_mode=True,
)

agent.print_response("栗野さんの経歴を教えてください", stream=True)
agent.print_response("私の最後の質問は？", stream=True)
