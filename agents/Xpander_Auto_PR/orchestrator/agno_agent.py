import os
import asyncio
from agno.agent import Agent
from agno.models.nebius import Nebius
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from agno.tools.thinking import ThinkingTools
from xpander_utils.sdk.adapters import AgnoAdapter
from Xpander_Auto_PR.tools.pr_tools import review_pr

DB_FILE = "agent_state.db"
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env into os.environ


class PRReviewOrchestrator:
    def __init__(self, agent_backend: AgnoAdapter):
        self.agent_backend = agent_backend
        self.agent = None
        self.tools = [ThinkingTools(add_instructions=True), review_pr]
        self.memory = Memory(
            model=Nebius(id="Qwen/Qwen3-235B-A22B", api_key=os.getenv("NEBIUS_API_KEY")),
            db=SqliteMemoryDb(table_name="user_memories", db_file=DB_FILE)
        )
        self.storage = SqliteStorage(table_name="agent_sessions", db_file=DB_FILE)

    async def run(self, message, user_id, session_id, cli=False):
        if self.agent is None:
            self.agent = Agent(
                model=Nebius(id="Qwen/Qwen3-235B-A22B", api_key=os.getenv("NEBIUS_API_KEY")),
                tools=self.tools,
                memory=self.memory,
                enable_agentic_memory=True,
                enable_user_memories=True,
                storage=self.storage,
                add_history_to_messages=True,
                num_history_runs=3,
                instructions=[
                    "You are a GitHub PR review agent.",
                    f"User: {user_id}",
                    f"Session: {session_id}"
                ]
            )
        if cli:
            return await self.agent.aprint_response(
                message,
                user_id=user_id,
                session_id=session_id,
                stream=True,
                stream_intermediate_steps=True
            )
        else:
            return await self.agent.arun(
                message,
                user_id=user_id,
                session_id=session_id
            )

