import asyncio
from dotenv import load_dotenv
from xpander_sdk import Backend, Task, on_task
from agno.agent import Agent
from tools.pr_tools import send_slack_message, review_pr

load_dotenv()


class MyAgent(Agent):
    def __init__(self, backend: Backend, **kwargs):
        super().__init__(**kwargs)
        self.backend = backend
        self.tools.extend([
            send_slack_message,
            review_pr,
        ])

    async def run(self, message, user_id, session_id, cli=False):
        if cli:
            return await self.aprint_response(
                message,
                user_id=user_id,
                session_id=session_id,
                stream=True,
                stream_intermediate_steps=True,
            )
        else:
            return await self.arun(
                message,
                user_id=user_id,
                session_id=session_id
            )


@on_task
async def my_agent_handler(task: Task):
    """
    Handles incoming Xpander tasks using MyAgent (subclass of Agent)
    """
    backend = Backend(configuration=task.configuration)
    agno_args = await backend.aget_args(task=task)
    
    my_agent = MyAgent(backend, **agno_args)
    result = await my_agent.arun(message=task.to_message())
    
    task.result = result.content
    return task

if __name__ == "__main__":
    async def main():
        backend = Backend()
        async with MyAgent(backend) as agent:
            response = await orchestrator.run(
                message="Review this PR for code quality issues: https://github.com/example/repo/pull/123",
                user_id="cli-user",
                session_id="cli-session",
                cli=True,
            )
            print("Response:", response)

    asyncio.run(main())
