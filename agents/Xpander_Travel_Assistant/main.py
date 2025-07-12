import asyncio
import json
from pathlib import Path
from xpander_utils.sdk.adapters import AgnoAdapter
from orchestrator.agno_agent import AgnoAgentOrchestrator

CFG_PATH = Path("xpander_config.json")
xpander_cfg = json.loads(CFG_PATH.read_text())

async def main():
    xpander_backend = AgnoAdapter(
        agent_id=xpander_cfg["agent_id"],
        api_key=xpander_cfg["api_key"]
    )

    async with AgnoAgentOrchestrator(xpander_backend) as orchestrator:
        workflow_result = await orchestrator.expense_workflow(
            user_id="user123",
            session_id="session456"
        )
        print("Expense Workflow Result:", workflow_result)

        while True:
            message = input("\nYou: ")
            if message.lower() in ["exit", "quit"]:
                break

            response = await orchestrator.run(
                message=message,
                user_id="user123",
                session_id="session456",
                cli=True
            )
            # print("Assistant:", response)

if __name__ == "__main__":
    asyncio.run(main())
