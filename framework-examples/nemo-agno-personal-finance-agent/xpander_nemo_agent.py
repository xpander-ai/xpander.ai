from textwrap import dedent
from dotenv import load_dotenv
load_dotenv()

from nat.builder.builder import Builder
from nat.builder.framework_enum import LLMFrameworkEnum
from nat.builder.function_info import FunctionInfo
from nat.cli.register_workflow import register_function
from nat.data_models.component_ref import LLMRef
from nat.data_models.function import FunctionBaseConfig
from nat.data_models.component_ref import FunctionRef


from xpander_sdk import Backend, OutputFormat, Tokens
from pydantic import BaseModel, Field
from agno.agent import Agent
from loguru import logger

class XpanderAgentConfig(FunctionBaseConfig, name="xpander_nemo_agent"):
    llm_name: LLMRef
    tools: list[FunctionRef] = Field(..., description="The tools to use for the financial research and planner agents.")

@register_function(config_type=XpanderAgentConfig, framework_wrappers=[LLMFrameworkEnum.AGNO])
async def xpander_nemo_agent_function(config: XpanderAgentConfig, builder: Builder):
    # run the agent
    async def load_and_run_xpander_nemo_agent(inputs: str) -> str:
        try:
            
            # Load NeMo LLM Gateway
            llm = await builder.get_llm(config.llm_name, wrapper_type=LLMFrameworkEnum.AGNO)
            
             # Get the search tool
            tools = builder.get_tools(tool_names=config.tools, wrapper_type=LLMFrameworkEnum.AGNO)
            
            # Load xpander backend
            backend = Backend()
            task = await backend.ainvoke_agent(prompt=inputs,run_locally=True)
            agno_args = await backend.aget_args(task=task,override={
                "model": llm,
                "role": "Generates a personalized financial plan based on user preferences and research results",
                "description": dedent("""\
                You are a senior financial planner. Given a user's financial goals, current financial situation, and a list of
                research results, your goal is to generate a personalized financial plan that meets the user's needs and
                preferences.
                """),
                "instructions": [
                    "Given a user's financial goals, current financial situation, and a list of research results, ",
                    "generate a personalized financial plan that includes suggested budgets, investment plans, ",
                    "and savings strategies. Ensure the plan is well-structured, informative, and engaging.",
                    "Ensure you provide a nuanced and balanced plan, quoting facts where possible.",
                    "Remember: the quality of the plan is important.",
                    "Focus on clarity, coherence, and overall quality.",
                    "Never make up facts or plagiarize. Always provide proper attribution.",
                    "Do not use any search functions directly; use only the information provided to create your plan.",
                ]
            })
            
            planner = Agent(**agno_args)
            
            researcher = Agent(
                name="Researcher",
                role="Searches for financial advice, investment opportunities, and savings strategies "
                "based on user preferences",
                model=llm,
                description=dedent("""\
                You are a world-class financial researcher. Given a user's financial goals and current financial situation,
                generate a list of search terms for finding relevant financial advice, investment opportunities, and savings
                strategies. Then search the web for each term, analyze the results, and return the 10 most relevant results.
                """),
                instructions=[
                    "Given a user's financial goals and current financial situation, first generate a list of 3 search terms "
                    "related to those goals.",
                    "For each search term, use the web_search_tool function to search the internet for information.",
                    "From the results of all searches, return the 10 most relevant results to the user's preferences.",
                    "Remember: the quality of the results is important.",
                ],
                tools=tools,
                add_datetime_to_instructions=True,
            )
            
            # First, use the researcher to gather relevant financial information
            researcher_response = await researcher.arun(task.to_message(), stream=False)
            
            # Combine the original input with the research results for the planner
            planner_input = f"""
                User query: {inputs}

                Research results:
                {researcher_response}

                Based on the above information, please create a personalized financial plan.
                """
            
            # Now run the planner with the research results
            planner_response = await planner.arun(message=planner_input)
            
            # in case of structured output, return as stringified json
            if task.output_format == OutputFormat.Json and isinstance(planner_response.content, BaseModel):
                planner_response.content = planner_response.content.model_dump_json()
            
            task.result = planner_response.content
            
            # report execution metrics
            task.tokens = Tokens(prompt_tokens=sum(planner_response.metrics['input_tokens']),completion_tokens=sum(planner_response.metrics['completion_tokens']))
            task.used_tools = [tool.tool_name for tool in planner_response.tools]
            
            # save changes
            await task.asave()
            
            return task.result
        except Exception as e:
            logger.critical(e)
            return f"Agent execution failed: {str(e)}"

    yield FunctionInfo.from_fn(load_and_run_xpander_nemo_agent)