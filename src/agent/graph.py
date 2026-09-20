"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""
from langchain.agents import create_agent, AgentState
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig

from src.agent.Tools.runnable_tool02 import runnable_tool
from src.agent.Tools.tool_demo01 import calculate
from src.agent.Tools.tool_demo03 import get_user_info
from src.agent.my_llm import llm


# 提示词模板的函数: 由用户传入内容，组成一个动态的系统提示词
def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    user_name = config['configurable'].get('user_name', 'zs')
    print(user_name)
    system_message = f'你是一个智能助手，尽可能的调用工具回答用户的问题，当前用户的名字是: {user_name}'
    return [{'role': 'system', 'content': system_message}] + state['messages']

# Define the graph
graph = create_agent(
    llm,
    tools=[calculate, runnable_tool,get_user_info],
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