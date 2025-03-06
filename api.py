import os
from typing import final

import uvicorn
from agno.agent import Agent, AgentKnowledge  # type: ignore
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.models.openai import OpenAIChat  # type: ignore
from agno.vectordb.pgvector import PgVector, SearchType as PgSearchType  # type: ignore
from dotenv import load_dotenv
from fastapi import FastAPI
from google.cloud import storage
from pydantic import BaseModel

load_dotenv()

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
DB_HOST = os.getenv("DB_HOST", "localhost")
db_url = f"postgresql+psycopg://postgres:postgres@{DB_HOST}:5432/agno"


def download_object(
    key: str,
    destination_file_name: str,
    bucket_name: str = "agno-playground",
) -> None:
    cli = storage.Client()
    bucket = cli.bucket(bucket_name)
    blob = bucket.blob(key)
    blob.download_to_filename(destination_file_name)


@final
class PreparePayload(BaseModel):
    document_id: str
    gs_key: str


@final
class SummaryPayload(BaseModel):
    document_id: str


@final
class Text(BaseModel):
    text: str


@final
class Empty(BaseModel):
    pass


@app.post("/prepare")
async def prepare(payload: PreparePayload) -> Empty:
    download_object(payload.gs_key, "downloaded.pdf")
    knowledge_base = PDFKnowledgeBase(
        path="downloaded.pdf",
        vector_db=PgVector(
            table_name=payload.document_id,
            db_url=db_url,
            search_type=PgSearchType.hybrid,
            schema="agno",
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        ),
    )
    knowledge_base.load(recreate=True)
    os.remove("downloaded.pdf")
    return Empty()


@app.post("/summary")
async def summary(payload: SummaryPayload) -> Text:
    knowledge_base = AgentKnowledge(
        vector_db=PgVector(
            table_name=payload.document_id,
            db_url=db_url,
            search_type=PgSearchType.hybrid,
            schema="agno",
        ),
    )

    agent = Agent(
        description="あなたはPDF文書を読み取り、ユーザーの欲しい情報を抽出・要約するスペシャリストです",
        instructions=[
            "あなたのナレッジベースから回答してください。",
            "ナレッジベースの情報のみを参照してください。",
        ],
        model=OpenAIChat(id="gpt-4o"),
        knowledge=knowledge_base,
        add_references=True,
        search_knowledge=False,
        markdown=True,
    )

    response = agent.run("経歴を要約してください")
    content = response.content
    if content is None:
        return Text(text="要約できませんでした")

    return Text(text=str(content))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
