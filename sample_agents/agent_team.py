import os

from agno.agent import Agent, RunResponse  # type: ignore
from agno.models.openai import OpenAIChat  # type: ignore
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.vectordb.lancedb import LanceDb, SearchType  # type: ignore
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)


# https://docs.agno.com/get-started/agents#multi-agent-teams
agent = Agent(
    team=[
        Agent(
            name="Web Agent",
            role="Webから情報を検索します",
            model=OpenAIChat(id="gpt-4o"),
            tools=[DuckDuckGoTools()],
            instructions="常に情報源を含めてください。",
            show_tool_calls=True,
            markdown=True,
        ),
        Agent(
            name="Finance Agent",
            role="ファイナンス情報を取得します",
            model=OpenAIChat(id="gpt-4o"),
            tools=[
                YFinanceTools(
                    stock_price=True, analyst_recommendations=True, company_info=True
                )
            ],
            instructions="データは表を使用して表示してください。",
            show_tool_calls=True,
            markdown=True,
        ),
    ],
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "常に情報源を含めてください。",
        "データは表を使用して表示してください。",
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

agent.print_response(
    "AI半導体企業の市場見通しと財務実績はどうなっていますか？", stream=True
)
