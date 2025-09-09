from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
from xpander_sdk import Task, on_task

@on_task
async def my_agent_handler(task: Task):
    cmd = ["nat", "run", "--config_file", "nemo_config.yml", "--input", json.dumps({"xpander_task_id": task.id})]
    proc = await asyncio.create_subprocess_exec(*cmd)
    await proc.wait()
    await task.areload()
    return task
