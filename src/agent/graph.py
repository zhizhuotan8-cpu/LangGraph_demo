"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""
from langchain.agents import create_agent

from src.agent.Tools.runnable_tool02 import runnable_tool
from src.agent.Tools.tool_demo01 import calculate
from src.agent.my_llm import llm


# Define the graph
graph = create_agent(
    llm,
    tools=[calculate, runnable_tool],
    system_prompt="你是一个智能助手，请回答我的问题。"
)

# result = graph.stream(
#     input={"messages":[{"role":"user","content":"计算一下(3+7)*5的值是多少？"}]},
#     stream_mode='messages'
# )
#
# for message, metadata in result:
#     if message.content:
#         print(message.content, end="", flush=True)