# llm = ChatOpenAI(
#     model='gpt-5.6-luna',
#     # model='deepseek-chat',
#     temperature=0.8,
#     api_key=CCTQ_API_KEY,
#     base_url=CCTQ_BASE_URL,
# )
from langchain_openai import ChatOpenAI

from .env_utils import SHUSHENG_API_KEY, SHUSHENG_BASE_URL

llm = ChatOpenAI(
    model='Agents-A1',
    # model='deepseek-chat',
    temperature=0.8,
    api_key=SHUSHENG_API_KEY,
    base_url=SHUSHENG_BASE_URL,
)