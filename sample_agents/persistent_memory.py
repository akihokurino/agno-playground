import json
import os
from typing import Any

from agno.agent import Agent, RunResponse  # type: ignore
from agno.models.openai import OpenAIChat  # type: ignore
from agno.storage.agent.sqlite import SqliteAgentStorage
from dotenv import load_dotenv
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)


# https://docs.agno.com/agents/memory#persistent-memory
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    storage=SqliteAgentStorage(
        table_name="persistent_memory",
        db_file="db/sample_agents.db",
    ),
    add_history_to_messages=True,
    num_history_responses=3,
    description="あなたは、常に丁寧で前向きかつポジティブな態度で対応する、頼りになるアシスタントです。",
    # session_id="f03785d4-56d5-4da7-9919-7f046b28cc33",  # SessionIdを指定することで再開可能
    debug_mode=True,
)


console = Console()


def print_chat_history(agent: Any) -> None:
    console.print(
        Panel(
            JSON(
                json.dumps(
                    [
                        m.model_dump(include={"role", "content"})
                        for m in agent.memory.messages
                    ]
                ),
                indent=4,
            ),
            title=f"Chat History for session_id: {agent.session_id}",
            expand=True,
        )
    )


agent.print_response("怖い話の最初の2行を教えてください", stream=True)
print_chat_history(agent)

# agent.print_response("私の最初の質問は？", stream=True)
# print_chat_history(agent)
