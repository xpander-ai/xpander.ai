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

xpander_agent.add_task(input="Hello, how are you?") ## Create a new thread for the agent (Empty messages object)

while not xpander_agent.is_finished: ## This is the main loop of the agent,
    ## Run the llm provider and get the response
    llm_response = your_llm_provider.completion(
        messages=xpander_agent.messages, #  A list of messages according to the agent's llm provider.
        tools=xpander_agent.get_tools(),  #A list of tools according to the agent's llm provider.
        tool_choice=xpander_agent.tool_choice,
        temperature=0.0,
    ) ## This is the response from the llm provider.
    
    ## Run the tools according to the agent's llm provider.
    ## If the AI will run "xpfinish-agent-execution-finished" tool, it will stop the execution of the agent and store the result in the agent's state.
    xpander_agent.run_tools(xpander_agent.extract_tool_calls(llm_response=llm_response)) 
    
    ## Optional: You can stop the execution of the agent if you want to.
    xpander_agent.stop_execution(is_success=True,result=("Your result here"))
    
final_result = xpander_agent.retrieve_execution_result()
print(final_result.result)
print(final_result.status)
print(final_result.memory_thread_id)

## Then you can call the agent again with the same thread id xpander_agent.add_task(input="Hello, how are you?", thread_id=final_result.memory_thread_id) 

async def main():
    # initialize agent
    agent = MyAgent(xpander_agent)
    
    # start the agent
    thread = await agent.chat(
        "Hi!, what can you do ?"
    )
    
    while True:
        user_input = input("You: ")
        thread = await agent.chat(user_input, thread)          

if __name__ == "__main__":
    asyncio.run(main())