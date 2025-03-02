import os

from agno.agent import Agent  # type: ignore
from agno.models.openai import OpenAIChat  # type: ignore
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)


agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        )
    ],
    instructions=["データは表を使用して表示してください。"],
    show_tool_calls=True,
    markdown=True,
    reasoning=True,
    debug_mode=True,
)

agent.print_response(
    "NVDAとTSLAを比較するレポートを日本語で書いてください。",
    stream=True,
    show_full_reasoning=True,
)
