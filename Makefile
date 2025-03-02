types:
	source venv/bin/activate && mypy .

run-basic-agent:
	source venv/bin/activate && python sample_agents/basic_agent.py

run-agent-with-tools:
	source venv/bin/activate && python sample_agents/agent_with_tools.py

run-agent-with-knowledge:
	source venv/bin/activate && python sample_agents/agent_with_knowledge.py

run-agent-team:
	source venv/bin/activate && python sample_agents/agent_team.py

run-research-agent:
	source venv/bin/activate && python sample_agents/research_agent.py

run-movie-agent:
	source venv/bin/activate && python sample_agents/movie_agent.py

run-hn-agent:
	source venv/bin/activate && python sample_agents/hn_agent.py

run-traditional-rag:
	source venv/bin/activate && python sample_agents/traditional_rag.py

run-local-rag:
	source venv/bin/activate && python sample_agents/local_rag.py

run-agentic-rag:
	source venv/bin/activate && python sample_agents/agentic_rag.py

run-agent-memory:
	source venv/bin/activate && python sample_agents/agent_memory.py

run-persistent-memory:
	source venv/bin/activate && python sample_agents/persistent_memory.py

run-personalized-memories-and-summaries:
	source venv/bin/activate && python sample_agents/personalized_memories_and_summaries.py

run-agent-with-storage:
	source venv/bin/activate && python sample_agents/agent_with_storage.py

run-reasoning-agent:
	source venv/bin/activate && python sample_agents/reasoning_agent.py

run-finance-reasoning:
	source venv/bin/activate && python sample_agents/finance_reasoning.py

run-hackernews-team-agent:
	source venv/bin/activate && python sample_agents/hackernews_team_agent.py

run-playground:
	source venv/bin/activate && python -m playground

run-db:
	docker-compose up
