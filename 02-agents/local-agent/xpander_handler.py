from dotenv import load_dotenv
load_dotenv()

from xpander_sdk import Task, Backend, on_task, OutputFormat, Tokens
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.ollama import Ollama

@on_task
async def my_agent_handler(task: Task):
    backend = Backend(configuration=task.configuration)
    
    agno_agent = Agent(**backend.get_args(override={
    'model': Ollama(id="gpt-oss:20b")
    }))

    result = await agno_agent.arun(message=task.to_message())
    
    # in case of structured output, return as stringified json
    if task.output_format == OutputFormat.Json and isinstance(result.content, BaseModel):
        result.content = result.content.model_dump_json()
    
    task.result = result.content
    
    # report execution metrics
    task.tokens = Tokens(prompt_tokens=sum(result.metrics['input_tokens']),completion_tokens=sum(result.metrics['completion_tokens']))
    task.used_tools = [tool.tool_name for tool in result.tools]
    
    return task
