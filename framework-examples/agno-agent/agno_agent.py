import asyncio
from dotenv import load_dotenv
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import  MultiMCPTools
from agno.tools.thinking import ThinkingTools
load_dotenv()

class AgnoAgent:
    def __init__(self):
        self.mcp_tools = MultiMCPTools(
            commands=[
                "uvx awslabs.core-mcp-server@latest",
                "uvx awslabs.eks-mcp-server@latest --allow-sensitive-data-access"
            ], 
            env={"AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"] , "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SECRET_ACCESS_KEY"], "AWS_REGION": os.environ["AWS_REGION"]}
        )
        self.agent = None
    
    async def run(self, message: str, user_id: str, session_id: str) -> str:
        """Run the agent with the given message and maintain state"""
        if self.agent is None:
            await self.mcp_tools.__aenter__()
            self.agent = Agent(
                model=OpenAIChat(id="gpt-4.1"),
                tools=[self.mcp_tools,ThinkingTools(add_instructions=True)],
                add_history_to_messages=True,
                num_history_responses=3,
                search_previous_sessions_history=True,
                num_history_sessions=3,
                read_chat_history=True,
                instructions=[
                    "You are a kubernetes assistant. Help users explore kubernetes clusters.",
                    "Navigate the kubernetes cluster to answer questions",
                    "Use the list_allowed_directories tool to find directories that you can access",
                    "Provide clear context about files you examine",
                    "Use headings to organize your responses",
                    "Be concise and focus on relevant information",
                    "prod cluster is eks01, all services starts with svc- , most of the services has more than one pod, and the pods are in the same namespace as the service",
                    f"Current User ID: {user_id}",
                    f"Current Session ID: {session_id}"
                ],
                markdown=True,
                success_criteria="The response should contain the actual data of the requested resource",
                add_state_in_messages=True,
                add_datetime_to_instructions=True,
            )
        
        response = await self.agent.aprint_response(message, user_id=user_id, session_id=session_id, stream=True)
        return response
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.agent is not None:
            await self.mcp_tools.__aexit__(exc_type, exc_val, exc_tb)
    
if __name__ == "__main__":
    async def main():            
        async with AgnoAgent() as agno_agent:
            while True:
                message = input("Enter a message: (type exit to exit)")
                if message == "exit":
                    break
                await agno_agent.run(
                    message, 
                    user_id="123", 
                    session_id="456"
                )

    asyncio.run(main())