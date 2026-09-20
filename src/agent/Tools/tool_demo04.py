from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from src.agent.my_state import CustomState


@tool
def get_user_info(
        tool_call_id:Annotated[str,InjectedToolCallId],#注入上一条消息的标识ToolCallId
        config: RunnableConfig) -> Command:
    """获得用户的名字、年龄、性别，以便生成祝福语句。"""
    user_name = config['configurable'].get('user_name','zs')
    print(f'调用工具，传入的用户名是：{user_name}')
    return Command(update={
        'user_name' : user_name,
        #更新一条工具执行后的消息，ToolMessage类型，需要和上一条消息合并，tool_call_id上一条消息的标识
        'Messages':[
            ToolMessage(
                content=f'调用工具，传入的用户名是：{user_name}',
                tool_call_id = tool_call_id
            )
        ]
    })
@tool
def greet_user(state:Annotated[CustomState,InjectedState]) -> None:
    """根据用户的名字，生成祝福语句。"""
    user_name = state.user_name
    return f"祝福{user_name}，恭喜你被我祝福到啦！"


