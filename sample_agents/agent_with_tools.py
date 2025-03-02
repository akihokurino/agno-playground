import os

from agno.agent import Agent, RunResponse  # type: ignore
from agno.models.openai import OpenAIChat  # type: ignore
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.lancedb import LanceDb, SearchType  # type: ignore
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)


# https://docs.agno.com/get-started/agents#agent-with-tools
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="あなたは、ストーリーテリングの才能を持つ情熱的なニュース記者です！",
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

agent.print_response("日本の最新の速報ニュースを教えてください。", stream=True)
