import os

from agno.agent import Agent, RunResponse  # type: ignore
from agno.models.openai import OpenAIChat  # type: ignore
from dotenv import load_dotenv
from rich.pretty import pprint

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)


# https://docs.agno.com/agents/memory#built-in-memory
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    add_history_to_messages=True,
    num_history_responses=3,
    description="あなたは、常に丁寧で前向きかつポジティブな態度で対応する、頼りになるアシスタントです。",
    debug_mode=True,
)

agent.print_response("怖い話の最初の2行を教えてください", stream=True)
if agent.memory is not None:
    pprint([m.model_dump(include={"role", "content"}) for m in agent.memory.messages])

agent.print_response("私の最初の質問は？", stream=True)
if agent.memory is not None:
    pprint([m.model_dump(include={"role", "content"}) for m in agent.memory.messages])
