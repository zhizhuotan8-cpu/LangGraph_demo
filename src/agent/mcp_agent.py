# -*- coding: utf-8 -*-
# Python MCP 服务端的连接配置
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from src.agent.my_llm import llm
import asyncio

# ============================================================
# JWT Token
# ============================================================

test_token = 'token'

# ============================================================
# Python MCP 服务端连接配置
# ============================================================

python_mcp_server_config = {
    'url': 'http://127.0.0.1:8080/streamable',
    'transport': 'streamable_http',
    'headers': {
        'Authorization': f'Bearer {test_token}',
    }
}

# python_mcp_server_config = {
#     'url': 'http://127.0.0.1:8080/streamable',
#     'transport': 'streamable_http',
#     # 'url': 'http://127.0.0.1:8080/sse',
#     # 'transport': 'sse',
# }
# # JAVA MCP 服务端的连接配置
# java_mcp_server_config = {
#     'url': 'http://127.0.0.1:8086/sse',
#     'transport': 'sse',
# }
# # 外网上公开 MCP 服务端的连接配置
# zhipuai_mcp_server_config = {
#     'url': "https://open.bigmodel.cn/api/mcp/web_search/sse?Authorization="+ZHIPU_API_KEY,
#     'transport': 'sse',
# }


# MCP的客户端
mcp_client = MultiServerMCPClient(
    {
        'python_mcp': python_mcp_server_config,
        # 'java_mcp': java_mcp_server_config,
        # 'zhipuai_mcp': zhipuai_mcp_server_config,
    }
)


async def create_mcp_agent():
    """异步构建 Agent，避免在模块导入时阻塞事件循环"""
    # 获取 MCP 工具
    mcp_tools = await mcp_client.get_tools()
    print(f"✅ 成功加载 {len(mcp_tools)} 个 MCP 工具")

    # 注意：get_prompt 和 get_resources 仅建议用于本地调试。
    # 在生产环境中，建议将它们移到具体的 Agent 节点逻辑中按需调用。
    try:
        p = await mcp_client.get_prompt(
            server_name='python_mcp',
            prompt_name='ask_about_topic',
            arguments={'topic': '深度学习'}
        )
        print("✅ Prompt 获取成功:", p)
    except Exception as e:
        print("⚠️ 获取 Prompt 失败 (可能服务端未提供此 prompt):", e)

    try:
        data = await mcp_client.get_resources(
            server_name='python_mcp',
            uris='resource://config'
        )
        if data:
            print("✅ Resource 获取成功, 数据:", data[0].data)
    except Exception as e:
        print("⚠️ 获取 Resource 失败:", e)

    # 创建并返回 LangChain Agent
    return create_agent(
        llm,
        tools=mcp_tools,
        system_prompt="你是一个智能助手，尽可能的调用工具回答用户的问题",
    )



agent = asyncio.run(create_mcp_agent())