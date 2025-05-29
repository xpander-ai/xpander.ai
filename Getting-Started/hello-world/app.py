import json
import asyncio
from xpander_sdk import XpanderClient , Agent

from my_agent import MyAgent

# === Load Configuration ===
# Reads API credentials and organization context from a local JSON file
with open('xpander_config.json', 'r') as config_file:
    xpander_config: dict = json.load(config_file)

# initialize xpander_client
xpander_client = XpanderClient(api_key=xpander_config.get("api_key"))
xpander_agent : Agent = xpander_client.agents.get(agent_id=xpander_config.get("agent_id"))

async def main():
    # initialize agent
    agent = MyAgent(xpander_agent)
    
    # start the agent
    thread = await agent.chat(
        "Hi!"
    )
    
    while True:
        user_input = input("You: ")
        thread = await agent.chat(user_input, thread)          

if __name__ == "__main__":
    asyncio.run(main())