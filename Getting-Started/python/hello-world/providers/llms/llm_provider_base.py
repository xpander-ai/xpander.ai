from typing import Any, Dict
from xpander_sdk import LLMTokens, Tokens


class LLMProviderBase:
    """
    Base class for LLM provider integration in xpander.ai platform.

    Provides interface methods for error handling, execution control,
    and token accounting, which can be extended by specific LLM provider implementations.
    """
    
    def __init__(self) -> None:
        self.ensure_required_secrets()

    @staticmethod
    def _error_response(msg: str) -> Dict[str, str]:
        """
        Generate a standardized error response.

        Args:
            msg (str): Error message to include in the response.

        Returns:
            Dict[str, str]: Dictionary with 'status' set to 'error' and the provided message under 'result'.
        """
        return {"status": "error", "result": msg}

    def should_stop_running(self, response: Any) -> bool:
        """
        Determine whether execution should be stopped based on LLM response.

        Args:
            response (Any): The response object from the LLM.

        Returns:
            bool: Always returns False in the base class.
        """
        return False

    def handle_token_accounting(self, execution_tokens: Tokens, response: Any) -> LLMTokens:
        """
        Handle the accounting of token usage after LLM execution.

        Args:
            execution_tokens (Tokens): Object containing execution token metadata.
            response (Any): The response object from the LLM.

        Returns:
            LLMTokens: An object representing the processed token accounting data.
        """
        pass
    
    def ensure_required_secrets(self):
        pass