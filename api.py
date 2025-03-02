import os

import uvicorn
from agno.agent import Agent  # type: ignore
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.models.openai import OpenAIChat  # type: ignore
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.vectordb.pgvector import PgVector, SearchType as PgSearchType  # type: ignore
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
DB_HOST = os.getenv("DB_HOST", "localhost")
db_url = f"postgresql+psycopg://postgres:postgres@{DB_HOST}:5432/agno"

knowledge_base = PDFKnowledgeBase(
    path="local_pdf.pdf",
    vector_db=PgVector(
        table_name="api_agent_embedding",
        db_url=db_url,
        search_type=PgSearchType.hybrid,
        schema="public",
    ),
)
knowledge_base.load(recreate=True)

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="あなたは有能なAIアシスタントです。",
    knowledge=knowledge_base,
    storage=PostgresAgentStorage(table_name="api_agent", db_url=db_url),
    markdown=True,
)


@app.get("/ask")
async def ask(query: str):
    response = agent.run(query)
    return {"response": response.content}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
