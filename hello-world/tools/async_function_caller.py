"""
Generic utility for asynchronously executing functions.
"""

import asyncio
import inspect
import time
import traceback
from typing import Any, Callable, Dict, List, Mapping

from loguru import logger
from xpander_sdk import ToolCallResult


async def execute_local_functions(
    function_calls: List[Any],
    functions_by_name: Dict[str, Callable],
    execute_single_function: Callable = None
) -> List[ToolCallResult]:
    """
    Execute multiple functions concurrently in a thread pool.

    Args:
        function_calls (List[Any]): List of function call objects to run.
        functions_by_name (Dict[str, Callable]): Dictionary mapping function names to actual functions.
        execute_single_function (Callable, optional): Custom function executor. Defaults to None.

    Returns:
        List[ToolCallResult]: Results of executed functions.
    """
    if not function_calls:
        return []

    start = time.time()
    
    # Use the provided custom executor or fall back to the default
    executor = execute_single_function or _execute_single_function
    
    results = await asyncio.gather(
        *(executor(call, functions_by_name) for call in function_calls)
    )
    
    if len(results) > 1:
        logger.info(f"⚙️ Executed {len(results)} functions in {time.time() - start:.2f} s")
    
    return results


async def _execute_single_function(function_call: Any, functions_by_name: Dict[str, Callable]) -> ToolCallResult:
    """
    Execute a single function in a background thread.

    Args:
        function_call: Function call object containing name, payload, and tool_call_id.
        functions_by_name: Dictionary mapping function names to actual functions.

    Returns:
        ToolCallResult: Result object with success flag and output payload.
    """
    tool_start_time = time.time()
    logger.info(
        f"🔦 Requesting function: {function_call.name} "
        f"with payload: {function_call.payload}"
    )

    tool_call_result = ToolCallResult(
        function_name=function_call.name,
        tool_call_id=function_call.tool_call_id,
        payload=function_call.payload,
    )

    def _run_function():
        original_func = functions_by_name.get(function_call.name)
        if not original_func:
            raise ValueError(f"Function {function_call.name} not found")

        params = {
            k: v for k, v in function_call.payload.items()
        }

        sig = inspect.signature(original_func)
        invalid = [k for k in params if k not in sig.parameters]
        if invalid:
            return False, {
                "success": False,
                "message": f"Invalid parameters for {function_call.name}: {', '.join(invalid)}",
                "invalid_params": invalid,
            }

        return True, original_func(**params)

    try:
        is_ok, result_dict = await asyncio.to_thread(_run_function)
        tool_call_result.is_success = result_dict.get("success", is_ok)
        tool_call_result.result = result_dict
    except Exception as exc:
        logger.error(f"❌ Error executing function {function_call.name}: {exc}")
        logger.critical("Traceback:", traceback.format_exc())
        tool_call_result.is_success = False
        tool_call_result.result = {
            "success": False,
            "message": f"Error executing {function_call.name}: {exc}",
            "error": str(exc),
        }

    logger.info(f"🔧 Function {function_call.name} completed in {time.time() - tool_start_time:.2f} s")
    return tool_call_result
