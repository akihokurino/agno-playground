import os

from agno.agent import Agent, RunResponse  # type: ignore
from agno.agent import AgentMemory  # type: ignore
from agno.memory.db.postgres import PgMemoryDb
from agno.models.openai import OpenAIChat  # type: ignore
from agno.storage.agent.postgres import PostgresAgentStorage
from dotenv import load_dotenv
from rich.pretty import pprint

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)
DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/agno"

# https://docs.agno.com/agents/memory#user-preferences-and-conversation-summaries
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    memory=AgentMemory(
        db=PgMemoryDb(
            table_name="personalized_memories_and_summaries_memory",
            db_url=DB_URL,
            schema="public",
        ),
        create_user_memories=True,
        create_session_summary=True,
    ),
    storage=PostgresAgentStorage(
        table_name="personalized_memories_and_summaries",
        db_url=DB_URL,
        schema="public",
    ),
    debug_mode=True,
)

agent.print_response("私の名前はジョン・ビリングスです", stream=True)
if agent.memory is not None:
    pprint(agent.memory.memories)
    pprint(agent.memory.summary)

agent.print_response("私はニューヨークに住んでいます", stream=True)
if agent.memory is not None:
    pprint(agent.memory.memories)
    pprint(agent.memory.summary)

agent.print_response("私は明日コンサートに行きます", stream=True)
if agent.memory is not None:
    pprint(agent.memory.memories)
    pprint(agent.memory.summary)

agent.print_response(
    "私たちは何について話していましたか？私の名前を知っていますか？", stream=True
)
