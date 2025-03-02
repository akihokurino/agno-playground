import os

from agno.agent import Agent, RunResponse  # type: ignore
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.openai import OpenAIChat  # type: ignore
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.lancedb import LanceDb, SearchType  # type: ignore
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)


# https://docs.agno.com/get-started/agents#agent-with-knowledge
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="あなたは、日本のAI政策の有識者です",
    instructions=[
        "あなたのナレッジベースから日本のAI政策に関して回答してください。",
        # "質問がウェブ検索の方が適している場合は、不足している情報を補うためにウェブを検索してください。",
        # "ウェブの検索結果よりも、ナレッジベースの情報を優先してください。",
        "ナレッジベースの情報のみを参照してください。",
    ],
    knowledge=PDFUrlKnowledgeBase(
        urls=[
            "https://www8.cao.go.jp/cstp/ai/ai_senryaku/11kai/shiryo1.pdf",
        ],
        vector_db=LanceDb(
            uri="db/lancedb",
            table_name="agent_with_knowledge_embedding",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        ),
    ),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

if agent.knowledge is not None:
    agent.knowledge.load()

agent.print_response("日本のAISIの概要について教えてください", stream=True)
