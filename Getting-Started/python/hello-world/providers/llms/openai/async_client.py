"""
OpenAI model provider implementation – async version using openai.

Copyright (c) 2025 Xpander, Inc. All rights reserved.
"""

from os import getenv
import time
from typing import Dict, Optional, List, Any
from dotenv import load_dotenv
from loguru import logger
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from xpander_sdk import LLMTokens, Tokens

from providers.llms.llm_provider_base import LLMProviderBase

load_dotenv()

class AsyncOpenAIProvider(LLMProviderBase):
    """
    Async Provider for OpenAI model API interactions.

    Handles async communication with OpenAI's Chat API including
    authentication, request configuration, safety guardrails,
    and token accounting for use in xpander.ai.

    Environment Variables:
        OPENAI_API_KEY: API key to authenticate with OpenAI.
    """

    def __init__(self) -> None:
        super().__init__()
        self.model_id = getenv("OPENAI_MODEL_ID", "gpt-4.1")
        self.openai_key = getenv("OPENAI_API_KEY")
        
    def ensure_required_secrets(self):
        # Ensure required secrets
        required_env_vars: List[str] = [
            "OPENAI_API_KEY",
        ]
        
        missing = [v for v in required_env_vars if getenv(v) is None]
        if missing:
            raise KeyError(f"Environment variables are missing: {missing}")

    
    async def invoke_model(
        self,
        messages: List[Dict[str, Any]],
        temperature: float = 0.0,
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[str] = "required",
    ) -> Dict[str, Any]:
        """
        Asynchronously invoke OpenAI's ChatCompletion API.

        Appends a safety instruction to the first system message if present,
        constructs the request parameters, and returns the raw response from
        OpenAI or a standardized error on failure.

        Args:
            messages (List[Dict[str, Any]]): Chat conversation messages.
            temperature (float): Generation temperature setting.
            tools (Optional[List[Dict]]): Tool calling configurations.
            tool_choice (Optional[str]): Tool selection strategy.

        Returns:
            Dict[str, Any]: OpenAI response or an error response dictionary.
        """
        start = time.time()
        _messages = messages.copy()
        
        params: Dict[str, Any] = {
            "model": self.model_id,
            "messages": _messages,
            "temperature": temperature,
            "tools": tools,
            "tool_choice": tool_choice,
        }

        try:
            client = self._get_client()
            resp : ChatCompletion = await client.chat.completions.create(**params)

            elapsed = time.time() - start
            logger.info(f"🔄 Model response received in {elapsed:.2f} s")
            logger.debug(f"🔄 Model finish reason: {resp.choices[0].finish_reason}")
            if resp.choices[0].message.content:
                logger.info(f"🔄 Model response: {resp.choices[0].message.content}")
            if resp.choices[0].message.tool_calls:
                for tool_call in resp.choices[0].message.tool_calls:
                    logger.info(f"🔄 Tool call function name: {tool_call.function.name}")
                    logger.debug(f"🔄 Tool call function arguments: {tool_call.function.arguments}")
            return resp

        except Exception as exc:
            logger.error(f"🔴 Error during model invocation: {exc}")
            msg = str(exc)

            if "ValidationException" in msg and "model identifier is invalid" in msg:
                err = (
                    f"The model ID '{self.model_id}' is invalid. "
                    "Please check your model environment variable."
                )
            else:
                err = "An error occurred while invoking the model. Please try again later."

            return self._error_response(err)

    def _get_client(self) -> AsyncOpenAI:
        """
        Return an authenticated OpenAI async client.

        Returns:
            AsyncOpenAI: OpenAI async client instance with configured API key.
        """
        return AsyncOpenAI(api_key=self.openai_key)

    def handle_token_accounting(self, execution_tokens: Tokens, response: ChatCompletion) -> LLMTokens:
        """
        Handle token usage accounting from the OpenAI model response.

        Args:
            execution_tokens (Tokens): Execution tracking container.
            response (ChatCompletion): OpenAI API response with token usage.

        Returns:
            LLMTokens: Structured usage object with prompt, completion, and total tokens.
        """
        llm_tokens = LLMTokens(
            completion_tokens=response.usage.completion_tokens,
            prompt_tokens=response.usage.prompt_tokens,
            total_tokens=response.usage.total_tokens,
        )

        execution_tokens.worker.completion_tokens += llm_tokens.completion_tokens
        execution_tokens.worker.prompt_tokens += llm_tokens.prompt_tokens
        execution_tokens.worker.total_tokens += llm_tokens.total_tokens

        return llm_tokens