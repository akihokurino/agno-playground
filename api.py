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
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
DB_HOST = os.getenv("DB_HOST", "localhost")
db_url = f"postgresql+psycopg://postgres:postgres@{DB_HOST}:5432/agno"


@final
class PreparePayload(BaseModel):
    document_id: str
    gs_key: str


@final
class AskPayload(BaseModel):
    document_id: str


@final
class Text(BaseModel):
    text: str


@final
class Empty(BaseModel):
    pass


@final
class Extract(BaseModel):
    result1: str = Field(
        ...,
        description="エンジニアリングマネージャーとしてのPRを抽出してください",
    )
    result2: str = Field(
        ...,
        description="プロジェクトマネージャーとしてのPRを抽出してください",
    )
    result3: str = Field(
        ...,
        description="エンジニアとしてのPRを抽出してください",
    )
    result4: str = Field(
        ...,
        description="副業での経験を抽出してください",
    )


def download_object(
    key: str,
    destination_file_name: str,
    bucket_name: str = "agno-playground",
) -> None:
    cli = storage.Client()
    bucket = cli.bucket(bucket_name)
    blob = bucket.blob(key)
    blob.download_to_filename(destination_file_name)


def get_vector(document_id: str) -> PgVector:
    return PgVector(
        table_name=document_id,
        db_url=db_url,
        search_type=PgSearchType.hybrid,
        schema="agno",
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    )


def create_knowledge(path: str, document_id: str) -> AgentKnowledge:
    knowledge = PDFKnowledgeBase(
        path=path, vector_db=get_vector(document_id), num_documents=10
    )
    knowledge.load(recreate=True)
    return knowledge


def get_knowledge(document_id: str) -> AgentKnowledge:
    return AgentKnowledge(vector_db=get_vector(document_id), num_documents=10)


@app.post("/prepare")
async def prepare(payload: PreparePayload) -> Empty:
    download_object(payload.gs_key, "downloaded.pdf")
    create_knowledge(path="downloaded.pdf", document_id=payload.document_id)
    os.remove("downloaded.pdf")
    return Empty()


@app.post("/summary")
async def summary(payload: AskPayload) -> Text:
    agent = Agent(
        description="あなたはPDF文書を読み取り、ユーザーの欲しい情報を要約するスペシャリストです",
        instructions=[
            "あなたのナレッジベースから回答してください。",
            "ナレッジベースの情報のみを参照してください。",
        ],
        model=OpenAIChat(id="gpt-4o"),
        knowledge=get_knowledge(payload.document_id),
        add_references=True,
        search_knowledge=False,
        markdown=True,
    )

    response = agent.run("経歴を要約してください")
    content = response.content
    if content is None:
        raise ValueError("No content found")

    return Text(text=str(content))


@app.post("/extract")
async def extract(payload: AskPayload) -> Text:
    agent = Agent(
        description="あなたはPDF文書を読み取り、ユーザーの欲しい情報を抽出するスペシャリストです",
        instructions=[
            "あなたのナレッジベースから回答してください。",
            "ナレッジベースの情報のみを参照してください。",
            "回答は指示したフォーマットだけにしてください。"
            "以下は回答のフォーマットです。",
            "\n\n",
            "# Webフロントエンド",
            "\n",
            "# iOS/Android",
            "\n",
            "# バックエンド",
            "\n",
            "# インフラ",
            "\n",
            "# プロジェクトマネージャー",
            "\n",
            "# エンジニアリングマネージャー",
        ],
        model=OpenAIChat(id="gpt-4o"),
        knowledge=get_knowledge(payload.document_id),
        add_references=True,
        search_knowledge=False,
        markdown=True,
    )

    response = agent.run("使っている技術や経験を教えてください。（Java, Azureなど）")
    content = response.content
    if content is None:
        raise ValueError("No content found")

    return Text(text=str(content))


@app.post("/extract_json")
async def extract_json(payload: AskPayload) -> Text:
    agent = Agent(
        description="あなたはPDF文書を読み取り、ユーザーの欲しい情報を抽出するスペシャリストです",
        instructions=[
            "あなたのナレッジベースから回答してください。",
            "ナレッジベースの情報のみを参照してください。",
        ],
        model=OpenAIChat(id="gpt-4o"),
        knowledge=get_knowledge(payload.document_id),
        response_model=Extract,
        add_references=True,
        search_knowledge=False,
        markdown=True,
    )

    response = agent.run("指定したJSONの構造に沿って回答してください。")
    content = response.content
    if content is None:
        raise ValueError("No content found")

    return Text(text=str(content))


@app.post("/calc")
async def calc(payload: AskPayload) -> Text:
    agent = Agent(
        description="あなたはPDF文書を読み取り、ユーザーの欲しい情報を抽出するスペシャリストです",
        instructions=[
            "あなたのナレッジベースから回答してください。",
            "ナレッジベースの情報のみを参照してください。",
        ],
        model=OpenAIChat(id="gpt-4o"),
        knowledge=get_knowledge(payload.document_id),
        add_references=True,
        search_knowledge=False,
        markdown=True,
    )

    response = agent.run("彼はこれまでに何回転職していますか？")
    content = response.content
    if content is None:
        raise ValueError("No content found")

    return Text(text=str(content))


@app.post("/delete")
async def delete(payload: AskPayload) -> Empty:
    knowledge = get_knowledge(payload.document_id)
    knowledge.delete()
    return Empty()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
