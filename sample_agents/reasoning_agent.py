import os

from agno.agent import Agent  # type: ignore
from agno.models.openai import OpenAIChat  # type: ignore
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)


task = (
    "3人の宣教師と3人の人食い人種が川を渡る必要があります。"
    "彼らは一度に最大2人まで乗れるボートを持っています。"
    "しかし、どちらかの岸で人食い人種の数が宣教師の数を上回ると、"
    "宣教師は食べられてしまいます。"
    "6人全員が無事に川を渡るにはどうすればよいでしょうか？"
    "ステップごとの解決策を示し、ASCII図で解答を表してください。"
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
    markdown=True,
    structured_outputs=True,
    debug_mode=True,
)

agent.print_response(task, stream=True, show_full_reasoning=True)
