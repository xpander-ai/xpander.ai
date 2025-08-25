import asyncio
import os
import time
from dotenv import load_dotenv
from uuid import uuid4
from loguru import logger
from pydantic import BaseModel

from agno.agent import Agent
from xpander_sdk import Backend, Task, on_task, OutputFormat, on_boot

from tools.travel_tools import (
    ta_book_flight,
    ta_book_hotel,
    ta_log_expense,
    ta_check_policy_violations,
    ta_summarize_expenses,
    ta_send_reminder
)

load_dotenv()

# Generate per-process random defaults to use when IDs are not supplied
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID") or f"user-{uuid4().hex[:8]}"
DEFAULT_SESSION_ID = os.getenv("DEFAULT_SESSION_ID") or f"session-{uuid4().hex[:12]}"

# Global agent instance
travel_agent = None
reminder_task = None

@on_boot
async def initialize_travel_agent():
    """Initialize travel agent on boot"""
    global travel_agent, reminder_task
    logger.info("🚀 Initializing Travel Agent on boot...")
    
    try:
        # The agent will be initialized per task with proper backend configuration
        logger.info("✅ Travel Agent initialized successfully on boot!")
        
        # Start the daily reminder scheduler
        reminder_task = asyncio.create_task(daily_reminder_scheduler())
        logger.info("📅 Daily reminder scheduler started")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize Travel Agent: {e}")

async def daily_reminder_scheduler():
    """Send reminders daily at 17:00 IST"""
    logger.info("📅 Daily reminder scheduler started")
    while True:
        try:
            now = time.localtime()
            if now.tm_hour == 17 and now.tm_min == 0:
                # Send reminders to predefined users
                for user_id in ["user123", "user456"]:
                    os.environ["AGENT_USER_ID"] = user_id
                    await ta_send_reminder(message="Daily reminder: Please submit your pending travel expenses.")
                    logger.info(f"📨 Sent reminder to user: {user_id}")
                await asyncio.sleep(86400)  # Wait a day
            else:
                await asyncio.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"❌ Error in reminder scheduler: {e}")
            await asyncio.sleep(60)

@on_task
async def my_agent_handler(task: Task):
    """Handles incoming Xpander tasks using Agno Agent"""
    logger.info(f"🎯 Processing travel agent task: {task.to_message()}")
    
    backend = Backend(configuration=task.configuration)
    agno_args = await backend.aget_args(task=task)

    # Add travel tools to the agent
    if "tools" not in agno_args:
        agno_args["tools"] = []
        
    agno_args["tools"].extend([
        ta_book_flight,
        ta_book_hotel,
        ta_log_expense,
        ta_check_policy_violations,
        ta_summarize_expenses,
        ta_send_reminder
    ])
    
    logger.info("🔧 Processing task with travel tools")

    agno_agent = Agent(**agno_args)

    # Extract user and session IDs
    user_id = getattr(task, "user_id", None) or (
        getattr(task, "metadata", {}) or {}
    ).get("user_id") or (
        getattr(task, "context", {}) or {}
    ).get("user_id") or DEFAULT_USER_ID

    session_id = (
        getattr(task, "session_id", None)
        or getattr(task, "thread_id", None)
        or getattr(task, "conversation_id", None)
        or (getattr(task, "metadata", {}) or {}).get("session_id")
        or (getattr(task, "context", {}) or {}).get("session_id")
    ) or DEFAULT_SESSION_ID

    # Set environment variables for tools
    os.environ["AGENT_USER_ID"] = str(user_id)
    os.environ["AGENT_SESSION_ID"] = str(session_id)

    logger.info(f"👤 User ID: {user_id}, Session ID: {session_id}")

    result = await agno_agent.arun(message=task.to_message())

    # Handle structured output
    if task.output_format == OutputFormat.Json and isinstance(result.content, BaseModel):
        result.content = result.content.model_dump_json()

    task.result = result.content
    logger.info("✅ Task processed successfully")
    return task
