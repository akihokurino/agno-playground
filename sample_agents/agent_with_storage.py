from typing import Optional

import typer
from agno.agent import Agent, RunResponse  # type: ignore
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.openai import OpenAIChat  # type: ignore
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.vectordb.lancedb import LanceDb, SearchType  # type: ignore
from agno.vectordb.pgvector import PgVector  # type: ignore
from dotenv import load_dotenv

load_dotenv()
DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/agno"


# https://docs.agno.com/agents/storage
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://www8.cao.go.jp/cstp/ai/ai_senryaku/11kai/shiryo1.pdf"],
    vector_db=PgVector(
        table_name="agent_with_storage_embedding",
        db_url=DB_URL,
        search_type=SearchType.hybrid,
        schema="public",
    ),
)
knowledge_base.load(upsert=True)

storage = PostgresAgentStorage(
    table_name="agent_with_storage", db_url=DB_URL, schema="public"
)


def run_agent(new: bool = False, user: str = "user") -> None:
    session_id: Optional[str] = None

    if not new:
        existing_sessions: list[str] = storage.get_all_session_ids(user)
        if len(existing_sessions) > 0:
            session_id = existing_sessions[0]

    agent = Agent(
        session_id=session_id,
        user_id=user,
        knowledge=knowledge_base,
        storage=storage,
        show_tool_calls=True,
        read_chat_history=True,
        debug_mode=True,
    )
    if session_id is None:
        session_id = agent.session_id
        print(f"Started Session: {session_id}\n")
    else:
        print(f"Continuing Session: {session_id}\n")

    agent.cli_app(markdown=True)


typer.run(run_agent)
