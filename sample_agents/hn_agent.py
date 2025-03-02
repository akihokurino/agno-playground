import json
import os

import httpx
from agno.agent import Agent, RunResponse  # type: ignore
from agno.models.openai import OpenAIChat  # type: ignore
from agno.vectordb.lancedb import LanceDb, SearchType  # type: ignore
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)


# https://docs.agno.com/agents/tools
def get_top_hackernews_stories(num_stories: int = 10) -> str:
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()

    stories = []
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()
        if "text" in story:
            story.pop("text", None)
        stories.append(story)
    return json.dumps(stories)


agent = Agent(tools=[get_top_hackernews_stories], show_tool_calls=True, markdown=True)

agent.print_response("ハッカーニュースのトップ５の記事を要約して", stream=True)
