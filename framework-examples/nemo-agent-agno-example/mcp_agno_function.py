"""
MCP Agno Agent Function for AIQ Toolkit
"""

import os
from typing import Optional
from agno.agent import Agent
from agno.tools.mcp import MultiMCPTools
from agno.tools.thinking import ThinkingTools
from aiq.builder.builder import Builder
from aiq.builder.framework_enum import LLMFrameworkEnum
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig


class MCPAgnoConfig(FunctionBaseConfig, name="mcp_agno"):
    """Configuration for MCP Agno Agent"""
    _type: str = "mcp_agno"
    llm_name: str = "openai_llm"
    mcp_commands: list[str] = [
        "awslabs.core-mcp-server",
        "awslabs.eks-mcp-server --allow-sensitive-data-access"
    ]
    user_id: str = "default_user"
    session_id: str = "default_session"
    description: str = "A Kubernetes assistant using MCP tools"


class MCPAgnoAgent:
    """Encapsulates the MCP Agno agent and its tools"""

    def __init__(self, config: MCPAgnoConfig, builder: Builder):
        self.config = config
        self.builder = builder
        self.mcp_tools: Optional[MultiMCPTools] = None
        self.agent: Optional[Agent] = None
        self._initialized = False

    async def initialize(self):
        """Initialize the MCP tools and agent"""
        if self._initialized:
            return

        # Get AWS credentials from environment
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        aws_region = os.environ.get("AWS_REGION", "us-east-1")

        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError(
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in environment variables")

        # Initialize MCP tools
        self.mcp_tools = MultiMCPTools(
            commands=self.config.mcp_commands,
            env={
                "AWS_ACCESS_KEY_ID": aws_access_key_id,
                "AWS_SECRET_ACCESS_KEY": aws_secret_access_key,
                "AWS_REGION": aws_region
            }
        )
        await self.mcp_tools.__aenter__()

        # Get LLM config and create Agno model
        llm_config = self.builder.get_llm_config(self.config.llm_name)

        # Create Agno model using the config from workflow.yaml
        from agno.models.openai import OpenAIChat
        llm = OpenAIChat(id=llm_config.model_name,
                         api_key=os.environ.get("OPENAI_API_KEY"))

        # Initialize agent
        self.agent = Agent(
            model=llm,
            tools=[self.mcp_tools, ThinkingTools(add_instructions=True)],
            add_history_to_messages=True,
            num_history_responses=3,
            instructions=[
                "You are a kubernetes assistant. Help users explore kubernetes clusters.",
                "Navigate the kubernetes cluster to answer questions",
                "Use the list_allowed_directories tool to find directories that you can access",
                "Provide clear context about files you examine",
                "Use headings to organize your responses",
                "Be concise and focus on relevant information",
                "prod cluster is eks01, all services starts with svc- , most of the services has more than one pod, and the pods are in the same namespace as the service",
                f"Current User ID: {self.config.user_id}",
                f"Current Session ID: {self.config.session_id}"
            ],
            markdown=True,
        )

        self._initialized = True

    async def run(self, message: str) -> str:
        """Run the agent with the given message"""
        if not self._initialized:
            await self.initialize()

        response = await self.agent.arun(
            message,
            user_id=self.config.user_id,
            session_id=self.config.session_id
        )
        return response.content

    async def cleanup(self):
        """Clean up resources"""
        if self.mcp_tools:
            await self.mcp_tools.__aexit__(None, None, None)


# Global agent instance (required for AIQ's stateless function calls)
_agent_instance: Optional[MCPAgnoAgent] = None


@register_function(config_type=MCPAgnoConfig, framework_wrappers=[LLMFrameworkEnum.AGNO])
async def mcp_agno(config: MCPAgnoConfig, builder: Builder):
    """MCP-enabled Agno agent for Kubernetes assistance."""
    global _agent_instance

    if _agent_instance is None:
        _agent_instance = MCPAgnoAgent(config, builder)
        await _agent_instance.initialize()

    yield FunctionInfo.from_fn(_agent_instance.run, description=config.description)
