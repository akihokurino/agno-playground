import os

from agno.agent import Agent, RunResponse  # type: ignore
from agno.models.openai import OpenAIChat  # type: ignore
from agno.vectordb.lancedb import LanceDb, SearchType  # type: ignore
from dotenv import load_dotenv
from pydantic import BaseModel, Field

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)


# https://docs.agno.com/agents/structured-output
class MovieScript(BaseModel):
    setting: str = Field(
        ..., description="大ヒット映画のための魅力的な舞台設定を提供してください。"
    )
    ending: str = Field(
        ...,
        description="映画の結末。明確でない場合は、ハッピーエンドを提供してください。",
    )
    genre: str = Field(
        ...,
        description="映画のジャンル。明確でない場合は、アクション、スリラー、またはロマンティックコメディのいずれかを選んでください。",
    )
    name: str = Field(..., description="この映画に名前を付けてください。")
    characters: list[str] = Field(..., description="この映画の登場人物の名前。")
    storyline: str = Field(
        ...,
        description="映画のための3文のストーリーラインを提供してください。エキサイティングにしてください！",
    )


json_mode_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="あなたは映画の脚本を書きます。",
    response_model=MovieScript,
    debug_mode=True,
)
structured_output_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="あなたは映画の脚本を書きます。",
    response_model=MovieScript,
    structured_outputs=True,
    debug_mode=True,
)

json_mode_agent.print_response("ニューヨーク")
structured_output_agent.print_response("ニューヨーク")
