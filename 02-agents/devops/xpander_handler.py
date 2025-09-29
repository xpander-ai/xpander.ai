from agno.agent import Agent
from agno.tools.mcp import MultiMCPTools
import os
from loguru import logger
from pydantic import BaseModel
from xpander_sdk import Task, Backend, on_task, OutputFormat, on_boot
from payments_py.payments import Payments, PaymentsError
from dotenv import load_dotenv
load_dotenv()

# Global MCP tools instance
mcp_tools = None

# Global Nevermined payments instance
payments_builder = None
payments_subscriber = None


# Subscriber flow to get the access token
# This is not part of the agent code, it's just a helper function to get the access token
# Subscriber should have already purchased the plan and have an access token
def get_access_token() -> str:
    try:
        credentials = payments_subscriber.agents.get_agent_access_token(
        os.environ["NVM_PLAN_ID"],
        os.environ["NVM_AGENT_ID"],
        )
        access_token = credentials["accessToken"]
        return access_token
    except PaymentsError:
        # For demo purposes, we will order the plan if the access token is not found
        logger.info("No access token found, ordering plan")
        payments_subscriber.plans.order_plan(os.environ["NVM_PLAN_ID"])
        credentials = payments_subscriber.agents.get_agent_access_token(
            os.environ["NVM_PLAN_ID"],
            os.environ["NVM_AGENT_ID"],
        )
        access_token = credentials["accessToken"]
        return access_token


# Builder flow to validate the access token and authorize the request
# Nevermined was designed to protect API endpoints so we need to pass the request url and http verb to validate the access token.
def validate_access_token(access_token: str) -> [str, bool]:
    logger.info(f"🔑 Validating access token: {access_token}")
    http_verb = "POST"
    requested_url = "https://amethyst-pinniped.agents.xpander.ai"
    auth_header = f"Bearer {access_token}"
    request = payments_builder.requests.start_processing_request(
        os.environ["NVM_AGENT_ID"],
        auth_header,
        requested_url,
        http_verb,
    )
    logger.info(f"🔑 Request: {request}")
    logger.info(f"💰 The client balance is: {request["balance"]["balance"]}")
    return [request["agentRequestId"], request["balance"]["isSubscriber"]]

@on_boot
async def initialize_mcp():
    """Initialize MCP and Nevermined payment tools on boot"""
    global mcp_tools
    logger.info("🚀 Initializing MCP tools on boot...")

    mcp_tools = MultiMCPTools(
        commands=[
            # Knowledge MCP
            "uvx mcp-proxy --transport streamablehttp https://knowledge-mcp.global.api.aws",
            "uvx awslabs.aws-api-mcp-server",
            # EKS MCP
            "uvx awslabs.eks-mcp-server --allow-sensitive-data-access"
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

    # Initialize the Nevermined payments library.
    # In a normal scenario only the builder would need to initialize the payments library.
    # The subscriber would only need to get the access token.
    # But for demo purposes, we will initialize the payments library for both the builder and the subscriber.
    global payments_builder, payments_subscriber
    logger.info("🚀 Initializing Nevermined payments on boot...")
    payments_builder = Payments({
        "nvm_api_key": os.environ["NVM_API_KEY"],
        "environment": "sandbox",
    })
    payments_subscriber = Payments({
        "nvm_api_key": os.environ["NVM_SUBSCRIBER_API_KEY"],
        "environment": "sandbox",
    })
    logger.info("✅ Nevermined payments initialized successfully on boot!")


@on_task
async def my_agent_handler(task: Task):
    backend = Backend(configuration=task.configuration)
    agno_args = await backend.aget_args(task=task)

    # This access token typically comes in the authorization header of an api request
    # In this case let's assume it comes from the backend args
    access_token = get_access_token()
    logger.info(f"🔑 Access token: {access_token}")

    # Use pre-initialized MCP tools
    if mcp_tools:
        agno_args["tools"].append(mcp_tools)
        logger.info("🔧 Processing task with MCP tools")
    else:
        logger.info("⚠️  No MCP tools available")

    agno_agent = Agent(**agno_args)

    # validate the access before calling the agent
    [agent_request_id, is_subscriber] = validate_access_token(access_token)
    if not is_subscriber:
        logger.warning("Access token is not valid")
        task.result = "Access token is not valid. Please purchase a plan."
        return task

    result = await agno_agent.arun(task.to_message())

    # after a successful call, we can redeem the credits
    credit_redemption = payments_subscriber.requests.redeem_credits_from_request(
        agent_request_id,
        access_token,
        10,
    )
    logger.info(f"💰 Credit redemption: {credit_redemption}")

    # check remaining balance of the subscriber
    remaining_balance = payments_subscriber.plans.get_plan_balance(
        os.environ["NVM_PLAN_ID"],
    )
    logger.info(f"💰 Remaining balance: {remaining_balance["balance"]}")

    # in case of structured output, return as stringified json
    if task.output_format == OutputFormat.Json and isinstance(result.content, BaseModel):
        result.content = result.content.model_dump_json()

    task.result = result.content
    return task
