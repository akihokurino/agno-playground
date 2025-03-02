import os

from agno.agent import Agent  # type: ignore
from agno.models.openai import OpenAIChat  # type: ignore
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)

hn_researcher = Agent(
    name="HackerNews Researcher",
    model=OpenAIChat("gpt-4o"),
    role="Hacker Newsのトップストーリーを取得する。",
    tools=[HackerNewsTools()],
)

web_searcher = Agent(
    name="Web Searcher",
    model=OpenAIChat("gpt-4o"),
    role="特定のトピックに関する情報をウェブ検索する。",
    tools=[DuckDuckGoTools()],
    add_datetime_to_instructions=True,
)

article_reader = Agent(
    name="Article Reader",
    model=OpenAIChat("gpt-4o"),
    role="URLから記事を読む。",
    tools=[Newspaper4kTools()],
)

hn_team = Agent(
    name="Hackernews Team",
    model=OpenAIChat("gpt-4o"),
    team=[hn_researcher, web_searcher, article_reader],
    instructions=[
        "まず、Hacker Newsでユーザーが求めている情報を検索してください。",
        "次に、記事リーダーにリンクを渡し、ストーリーの詳細を読むよう依頼してください。",
        "重要: 記事リーダーには必ず読むべきリンクを提供してください。",
        "その後、ウェブ検索ツールを使って各ストーリーの追加情報を検索してください。",
        "最後に、よく考えられた魅力的な要約を日本語で提供してください。",
    ],
    show_tool_calls=True,
    markdown=True,
)

hn_team.print_response(
    "Hacker Newsのトップ2のストーリーについて記事を書いてください", stream=True
)
