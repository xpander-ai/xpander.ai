import asyncio
import json
from pathlib import Path
from Xpander_Auto_PR.orchestrator.agno_agent import PRReviewOrchestrator
from xpander_utils.sdk.adapters import AgnoAdapter

CFG_PATH = Path("xpander_config.json")
xpander_cfg = json.loads(CFG_PATH.read_text())

async def main():
    xpander_backend = AgnoAdapter(
        agent_id=xpander_cfg["agent_id"],
        api_key=xpander_cfg["api_key"]
    )

    orchestrator = PRReviewOrchestrator(xpander_backend)

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

if __name__ == "__main__":
    asyncio.run(main())