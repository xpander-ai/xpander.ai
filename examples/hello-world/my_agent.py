"""
Copyright (c) 2025 Xpander, Inc. All rights reserved.
"""

import asyncio
import json
import sys
import time
from typing import Optional, List, Dict, Any
from loguru import logger
from xpander_sdk import (
    Agent, LLMProvider, MemoryStrategy, LLMTokens,Tokens
)
from providers.llms.openai.async_client import AsyncOpenAIProvider
from tools.async_function_caller import execute_local_functions
from tools.local_tools import local_tools_by_name, local_tools_list
from dotenv import load_dotenv

load_dotenv()

logger.remove()  # Remove all handlers including the default one
logger.add(sink=sys.stderr, level="INFO")

# Provider to use. Default OpenAI
llm_provider = LLMProvider.OPEN_AI

class MyAgent:
    """
    A framework agnostic agent implementation leveraging xpander.ai's backend-as-a-service infrastructure.

    Handles asynchronous LLM interactions, orchestrates multi-step reasoning, and seamlessly integrates both local and cloud-based tools.

    Args:
        agent (Agent): The xpander.ai Agent instance to operate.
    """

    def __init__(
        self,
        agent: Agent
    ) -> None:
        self.agent = agent
        self.llm_provider = llm_provider

        self.agent.memory_strategy = MemoryStrategy.BUFFERING
        
        with open("agent_instructions.json", "r") as f:
            local_instructions = json.load(f)
        
        if local_instructions:
            self.agent.instructions.role = local_instructions["role"]
            self.agent.instructions.goal = local_instructions["goal"]
            self.agent.instructions.general = local_instructions["general"]
            
        # Register local tools with the agent
        self.agent.add_local_tools(local_tools_list)
        
        self.agent.select_llm_provider(llm_provider)

        if llm_provider == LLMProvider.OPEN_AI:
            self.model_endpoint = AsyncOpenAIProvider()

    async def chat(self, user_input: str, thread_id: Optional[str] = None) -> str:
        """
        Public entry point for chat interaction.

        Adds a user task to the agent memory and initiates the async reasoning loop.

        Args:
            user_input (str): User's input or instruction.
            thread_id (Optional[str]): Memory thread to append to (if continuing a thread).

        Returns:
            str: The memory thread ID of the resulting agent run.
        """
        if thread_id:
            logger.info(f"🧠 Adding task to existing thread: {thread_id}")
            self.agent.add_task(input=user_input, thread_id=thread_id)
        else:
            logger.info("🧠 Adding task to a new thread")
            self.agent.add_task(input=user_input)

        agent_thread = await self._agent_loop()
        logger.info("-" * 80)
        logger.info(f"🤖 Agent response: {agent_thread.result}")
        return agent_thread.memory_thread_id

    async def _call_model(self) -> Dict[str, Any]:
        """
        Internal helper to call the model endpoint.

        Args:
            tools (Optional[List[Dict]]): Tool specification for the model.

        Returns:
            Dict[str, Any]: Model response or error.
        """
        response = await self.model_endpoint.invoke_model(
            messages=self.agent.messages,
            temperature=0.0,
            tools=self.agent.get_tools(),
            tool_choice=self.agent.tool_choice,
        )

        return response

    async def _agent_loop(self):
        """
        Core async loop coordinating reasoning steps and tool execution.

        Returns:
            Any: The final agent thread result after loop completion.
        """
        step = 1
        logger.info("🪄 Starting Agent Loop")
        execution_tokens = Tokens(worker=LLMTokens(0, 0, 0))
        execution_start_time = time.perf_counter()

        ## main agentic loop
        while not self.agent.is_finished():
            logger.info("-" * 80)
            logger.info(f"🔍 Step {step}")

            ## call the AI model with tools and the state of the agent
            response = await self._call_model()

            ## handle token accounting
            step_usage = self.model_endpoint.handle_token_accounting(
                execution_tokens=execution_tokens,
                response=response,
            )

            ## add llm response to agent memory
            llm_response = response.model_dump() if not isinstance(response, dict) else response
            self.agent.add_messages(llm_response)
            
            ## report execution metrics
            self.agent.report_execution_metrics(
                llm_tokens=execution_tokens,
                ai_model=self.model_endpoint.model_id,
            )

            ## extract all tool calls from llm response
            tool_calls = self.agent.extract_tool_calls(llm_response=llm_response)

            ## execute cloud tool calls
            cloud_tool_call_results = await asyncio.to_thread(
                self.agent.run_tools,
                tool_calls=tool_calls,
            )

            ## retrieve pending local tool calls
            local_tool_calls = await asyncio.to_thread(
                self.agent.retrieve_pending_local_tool_calls,
                tool_calls=tool_calls,
            )
            
            ## remove cloud tool calls empty results that are already in local tool calls
            cloud_tool_call_results[:] = [
                c for c in cloud_tool_call_results
                if c.tool_call_id not in {t.tool_call_id for t in local_tool_calls}
            ]
            
            ## execute local tool calls
            local_tool_call_results = await execute_local_functions(
                function_calls=local_tool_calls,
                functions_by_name=local_tools_by_name,
            )

            ## add local tool call results to agent memory
            if local_tool_call_results:
                self.agent.memory.add_tool_call_results(
                    tool_call_results=local_tool_call_results,
                )

            ## log tool call results
            for res in cloud_tool_call_results + local_tool_call_results:
                emoji = "✅" if res.is_success else "❌"
                logger.info(f"{emoji} {res.function_name}")

            logger.info(
                f"🔢 Step {step} tokens used: {step_usage.total_tokens} "
                f"(output: {step_usage.completion_tokens}, input: {step_usage.prompt_tokens})"
            )
            step += 1

        logger.info(
            f"✨ Execution duration: {time.perf_counter() - execution_start_time:.2f} s"
        )
        logger.info(
            f"🔢 Total tokens used: {execution_tokens.worker.total_tokens} "
            f"(output: {execution_tokens.worker.completion_tokens}, "
            f"input: {execution_tokens.worker.prompt_tokens})"
        )

        ## return the final agent thread result
        return self.agent.retrieve_execution_result()