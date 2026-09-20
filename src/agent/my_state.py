from langchain.agents import AgentState


#自定义的状态类，继承自AgentState类
class CustomState(AgentState):
    username:str