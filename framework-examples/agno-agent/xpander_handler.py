import json
import asyncio
from xpander_utils.events import XpanderEventListener, AgentExecutionResult, AgentExecution
from xpander_utils.sdk.adapters import AgnoAdapter

from pathlib import Path
from myCoolAgnoAgent import MyCoolAgnoAgent
from xpander_sdk import LLMTokens, Tokens

CFG_PATH = Path("xpander_config.json")
if not CFG_PATH.exists():
    raise FileNotFoundError("Missing xpander_config.json")

xpander_cfg: dict = json.loads(CFG_PATH.read_text())

# xpander‑sdk is blocking; create the client in a worker thread
xpander_backend: AgnoAdapter = asyncio.run(
    asyncio.to_thread(AgnoAdapter, agent_id=xpander_cfg["agent_id"], api_key=xpander_cfg["api_key"])
)

my_cool_agno_agent = MyCoolAgnoAgent(xpander_backend)

# === Define Execution Handler ===
async def on_execution_request(execution_task: AgentExecution) -> AgentExecutionResult:
    """
    Callback triggered when an execution request is received from a registered agent.
    
    Args:
        execution_task (AgentExecution): Object containing execution metadata and input.

    Returns:
        AgentExecutionResult: Object describing the output of the execution.
    """
    
    try:
        
        # initialize the agent with task
        await asyncio.to_thread(xpander_backend.agent.init_task, execution=execution_task.model_dump())
        
        IncomingEvent = (
            f"Incoming message: {execution_task.input.text}\n"
            f"From user: {execution_task.input.user.first_name} "
            f"{execution_task.input.user.last_name}\n"
            f"Email: {execution_task.input.user.email}" 
        )
        
        agent_response = await my_cool_agno_agent.run(IncomingEvent, execution_task.input.user.id, execution_task.memory_thread_id)
        metrics = agent_response.metrics
        llm_tokens = LLMTokens(
            completion_tokens=sum(metrics['completion_tokens']),
            prompt_tokens=sum(metrics['prompt_tokens']),
            total_tokens=sum(metrics['total_tokens']),
        )
        xpander_backend.agent.report_execution_metrics(llm_tokens=Tokens(worker=llm_tokens), ai_model=agent_response.model, source_node_type="agno")
    except Exception as e:
        return AgentExecutionResult(result=str(e), is_success=False)
    
    return AgentExecutionResult(result=agent_response.content, is_success=True)
# === Register Callback ===
# Attach your custom handler to the listener
listener = XpanderEventListener(**xpander_cfg)
listener.register(on_execution_request=on_execution_request)