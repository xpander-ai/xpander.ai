from agno.agent import Agent
from agno.tools.mcp import MultiMCPTools
import os
from loguru import logger
from pydantic import BaseModel
from xpander_sdk import Task, Backend, on_task, OutputFormat, on_boot
from dotenv import load_dotenv
load_dotenv()

# Global MCP tools instance
mcp_tools = None


@on_boot
async def initialize_mcp():
    """Initialize MCP tools on boot"""
    global mcp_tools
    logger.info("🚀 Initializing MCP tools on boot...")

    mcp_tools = MultiMCPTools(
        commands=[
            "uvx mcp-proxy --transport streamablehttp https://knowledge-mcp.global.api.aws",
            "uvx awslabs.aws-api-mcp-server"
        ],
        env={
            "AWS_ACCESS_KEY_ID": os.environ.get("PROD_AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.environ.get("PROD_AWS_SECRET_ACCESS_KEY"),
            "AWS_REGION": os.environ.get("AWS_REGION", ""),
        },
        timeout_seconds=300
    )

    await mcp_tools.__aenter__()
    logger.info("✅ MCP tools initialized successfully on boot!")


@on_task
async def my_agent_handler(task: Task):
    backend = Backend(configuration=task.configuration)
    agno_args = await backend.aget_args(task=task)

    # Use pre-initialized MCP tools
    if mcp_tools:
        agno_args["tools"].append(mcp_tools)
        logger.info("🔧 Processing task with MCP tools")
    else:
        logger.info("⚠️  No MCP tools available")

    agno_agent = Agent(**agno_args)

    result = await agno_agent.arun(message=task.to_message())

    # in case of structured output, return as stringified json
    if task.output_format == OutputFormat.Json and isinstance(result.content, BaseModel):
        result.content = result.content.model_dump_json()

    task.result = result.content
    return task
