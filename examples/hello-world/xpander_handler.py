import json
from xpander_utils.events import XpanderEventListener, AgentExecutionResult, AgentExecution, ExecutionStatus
from xpander_sdk import XpanderClient

from my_agent import MyAgent

# === Load Configuration ===
# Reads API credentials and organization context from a local JSON file
with open('xpander_config.json', 'r') as config_file:
    xpander_config: dict = json.load(config_file)

# === Initialize Event Listener ===
# Create a listener to subscribe to execution requests from specified agent(s)
listener = XpanderEventListener(**xpander_config)

# initialize xpander_client
xpander = XpanderClient(api_key=xpander_config.get("api_key"))

# === Define Execution Handler ===
async def on_execution_request(execution_task: AgentExecution) -> AgentExecutionResult:
    """
    Callback triggered when an execution request is received from a registered agent.
    
    Args:
        execution_task (AgentExecution): Object containing execution metadata and input.

    Returns:
        AgentExecutionResult: Object describing the output of the execution.
    """
    
    # initialize agent instance
    agent = xpander.agents.get(agent_id=xpander_config.get("agent_id"))
    
    # initialize the agent with task
    agent.init_task(execution=execution_task.model_dump()) 
    
    # initialize the agent    
    my_agent = MyAgent(agent=agent)
    exec_status = await my_agent._agent_loop() 
    
    return AgentExecutionResult(
        result=exec_status.result,
        is_success=exec_status.status == ExecutionStatus.COMPLETED,
    )

# === Register Callback ===
# Attach your custom handler to the listener
listener.register(on_execution_request=on_execution_request)