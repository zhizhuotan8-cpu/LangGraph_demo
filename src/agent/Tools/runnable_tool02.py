from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from src.agent.my_llm import llm

prompt = (  # 外层的模板
    PromptTemplate.from_template("帮我生成一个简短的，关于{topic}的报幕词。")
    + ", 要求： 1、内容搞笑一点；"
    + "2、输出的内容采用{language}。"
)

class ChainTool(BaseModel):
    topic:str = Field(description="报幕词的主题")
    language:str = Field(description="输出的语言")


chain = prompt | llm | StrOutputParser()
runnable_tool = chain.as_tool(
    name="chain_tool",
    description="这是一一个生成报幕词的工具，输入一个topic和language，输出一个报幕词。",
    args_schema=ChainTool
)

# print(runnable_tool.args_schema.model_json_schema())