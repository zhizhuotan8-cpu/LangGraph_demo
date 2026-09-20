from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

@tool
def get_user_info(config: RunnableConfig) -> float:
    """Get user information."""
    user_name = config['configurable'].get('user_name','zs')
    print(f'调用工具，传入的用户名是：{user_name}')
    return {
        'user_name': user_name,
        'user_age': 18,
        'user_gender': 'male'
    }


