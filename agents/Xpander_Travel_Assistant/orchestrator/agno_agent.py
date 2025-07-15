from agno.agent import Agent
from agno.models.nebius import Nebius
from agno.tools.thinking import ThinkingTools
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from xpander_utils.sdk.adapters import AgnoAdapter

from tools.travel_tools import (
    book_flight,
    book_hotel,
    log_expense,
    check_policy_violations,
    summarize_expenses,
    send_reminder
)
from core.travel import (
    book_flight_impl,
    book_hotel_impl,
    check_policy_impl,
    summarize_expenses_impl
)

import asyncio
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_FILE = "agent_state.db"

class AgnoAgentOrchestrator:
    def __init__(self, agent_backend: AgnoAdapter):
        self.agent_backend = agent_backend
        self.agent = None
        self.tools = [
            ThinkingTools(add_instructions=True),
            book_flight,
            book_hotel,
            log_expense,
            check_policy_violations,
            summarize_expenses,
            send_reminder
        ]
        self.reminder_task = None
        self.memory = Memory(
            model=Nebius(id="Qwen/Qwen3-235B-A22B", api_key=os.getenv("NEBIUS_API_KEY")),
            db=SqliteMemoryDb(table_name="user_memories", db_file=DB_FILE)
        )
        self.storage = SqliteStorage(table_name="agent_sessions", db_file=DB_FILE)

    async def __aenter__(self):
        self.reminder_task = asyncio.create_task(self.daily_reminder_scheduler())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.reminder_task:
            self.reminder_task.cancel()

    async def daily_reminder_scheduler(self):
        while True:
            now = time.localtime()
            if now.tm_hour == 17 and now.tm_min == 0:
                for user_id in ["user123", "user456"]:
                    await send_reminder(user_id=user_id, message=None)
                await asyncio.sleep(86400)
            else:
                await asyncio.sleep(60)

    async def plan_trip(self, origin, destination, dates, budget, user_id, session_id):
        flight_result = await book_flight_impl(
            origin=origin,
            destination=destination,
            date=dates.split(' to ')[0],
            budget=str(budget),
            user_id=user_id,
            session_id=session_id
        )
        try:
            start_date, end_date = [datetime.strptime(d, "%Y-%m-%d") for d in dates.split(' to ')]
            nights = (end_date - start_date).days
        except Exception:
            nights = 3
        hotel_result = await book_hotel_impl(
            destination=destination,
            nights=nights,
            budget=str(budget * 0.6),
            user_id=user_id,
            session_id=session_id
        )
        return {"flight": flight_result, "hotel": hotel_result}

    async def expense_workflow(self, user_id, session_id):
        violations = await check_policy_impl(user_id=user_id, session_id=session_id)
        summary = await summarize_expenses_impl(user_id=user_id, session_id=session_id)
        return {"violations": violations, "summary": summary}

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
                    "You are a travel and expense assistant.",
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