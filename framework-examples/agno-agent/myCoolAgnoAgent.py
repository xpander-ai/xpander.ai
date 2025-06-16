from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import  MultiMCPTools
from xpander_utils.sdk.adapters import AgnoAdapter

class MyCoolAgnoAgent:
    def __init__(self, agent_backend: AgnoAdapter):
        self.mcp_tools = MultiMCPTools(
            commands=[
                "uvx awslabs.core-mcp-server@latest",
                "uvx awslabs.eks-mcp-server@latest --allow-sensitive-data-access"
            ], 
            env={"AWS_ACCESS_KEY_ID": "YOUR_ACCESS_KEY", "AWS_SECRET_ACCESS_KEY": "YOUR_SECRET_KEY", "AWS_REGION": "us-west-2"}
        )
        self.agent_backend = agent_backend
        self.agent = None
    
    async def run(self, message: str, user_id: str, session_id: str) -> str:
        """Run the agent with the given message and maintain state"""
        if self.agent is None:
            await self.mcp_tools.__aenter__()
            self.agent = Agent(
                model=OpenAIChat(id="gpt-4.1"),
                tools=[self.mcp_tools, *self.agent_backend.get_tools()],
                add_history_to_messages=True,
                num_history_responses=3,
                search_previous_sessions_history=True,
                num_history_sessions=3,
                read_chat_history=True,
                instructions=self.agent_backend.get_system_prompt(),
                markdown=True,
                success_criteria=self.agent_backend.agent.instructions.goal,
                add_state_in_messages=True,
                add_datetime_to_instructions=True,
                storage=self.agent_backend.storage
            )
        
        response = await self.agent.arun(message, user_id=user_id, session_id=session_id)
        return response
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    