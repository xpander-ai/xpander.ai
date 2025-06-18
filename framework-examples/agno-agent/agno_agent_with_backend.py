import asyncio
import json
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import  MultiMCPTools
from agno.tools.thinking import ThinkingTools
from xpander_utils.sdk.adapters import AgnoAdapter
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CFG_PATH = Path("xpander_config.json")
xpander_cfg: dict = json.loads(CFG_PATH.read_text())

class AgnoAgentWithBackend:
    def __init__(self, agent_backend: AgnoAdapter):
        self.mcp_tools = MultiMCPTools(
            commands=[
                "uvx awslabs.core-mcp-server@latest",
                "uvx awslabs.eks-mcp-server@latest --allow-sensitive-data-access"
            ], 
            env={"AWS_ACCESS_KEY_ID": os.environ["PROD_AWS_ACCESS_KEY_ID"] , "AWS_SECRET_ACCESS_KEY": os.environ["PROD_AWS_SECRET_ACCESS_KEY"], "AWS_REGION": os.environ["PROD_AWS_REGION"]}
        )
        self.agent_backend = agent_backend
        self.agent = None
    
    async def run(self, message: str, user_id: str, session_id: str, cli:bool = False) -> str:
        """Run the agent with the given message and maintain state"""
        if self.agent is None:
            await self.mcp_tools.__aenter__()
            self.agent = Agent(
                model=OpenAIChat(id="gpt-4.1"),
                tools=[self.mcp_tools, ThinkingTools(add_instructions=True),*self.agent_backend.get_tools()],
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
        if(cli):
            response = await self.agent.aprint_response(message, user_id=user_id, session_id=session_id, stream=True)
        else:
            response = await self.agent.arun(message, user_id=user_id, session_id=session_id)
        
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
        print("Starting Agno Agent with xpander.ai Backend", xpander_cfg["agent_id"])
        xpander_backend: AgnoAdapter = await asyncio.to_thread(
            AgnoAdapter, 
            agent_id=xpander_cfg["agent_id"], 
            api_key=xpander_cfg["api_key"]
        )
        
        async with AgnoAgentWithBackend(xpander_backend) as agno_agent_with_backend:
            while True:
                message = input("Enter a message: (type exit to exit)")
                xpander_backend.agent.add_task(
                    input=message,
                    thread_id="456",
                )
                if message == "exit":
                    break
                await agno_agent_with_backend.run(
                    message, 
                    user_id="123", 
                    session_id="456", 
                    cli=True
                )

    asyncio.run(main())