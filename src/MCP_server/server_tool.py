import time
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
from fastmcp import FastMCP
from fastmcp.prompts import Message
from fastmcp.server.auth import JWTVerifier

from src.agent.my_llm import llm
from typing import Annotated



# ============================================================
# 1. JWT 配置
# ============================================================

JWT_ISSUER = "https://www.laotan.com"
JWT_AUDIENCE = "my-dev-server"


# ============================================================
# 2. 生成 RSA 密钥对
# ============================================================

private_key = generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)


# ============================================================
# 3. 获取 PEM 格式的私钥
# ============================================================

private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)


# ============================================================
# 4. 获取 PEM 格式的公钥
# ============================================================

public_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode("utf-8")


# ============================================================
# 5. 创建 FastMCP JWT 验证器
# ============================================================

auth = JWTVerifier(
    public_key=public_pem,
    issuer=JWT_ISSUER,
    audience=JWT_AUDIENCE,
)


# ============================================================
# 6. 创建 MCP Server
# ============================================================

server = FastMCP(
    name="tzz_mcp",
    instructions="我定义的一个MCP服务器",
    auth=auth,
)


# ============================================================
# 7. 生成测试 JWT Token
# ============================================================

test_token = jwt.encode(
    {
        "sub": "dev_user",

        # 签发者
        "iss": JWT_ISSUER,

        # 受众
        "aud": JWT_AUDIENCE,

        # 权限范围
        "scope": "laotan invoke_tools",

        # 过期时间：1小时
        "exp": int(time.time()) + 3600,
    },
    private_pem,
    algorithm="RS256",
)


print("=" * 70)
print("MCP Server JWT 测试 Token")
print("=" * 70)
print(test_token)
print("=" * 70)





@server.tool(
    name="chain_tool",
    description="这是一个生成报幕词的工具，输入一个topic和language，输出一个报幕词。",
)
async def chain_tool(
    topic: Annotated[str, "报幕词的主题"],
    language: Annotated[str, "输出的语言"],
) -> str:
    """生成关于topic的报幕词，用language输出"""
    return await llm.ainvoke({"topic": topic, "language": language})


@server.tool(name='calculate', description='这是一个计算工具，输入两个数和一个操作符，输出计算结果')
def calculate(
    a: Annotated[float, '这是第一个参数'],
    b: Annotated[float, '这是第二个参数'],
    operation: Annotated[str, '这是操作符'],
) -> float:
    """计算两个数的和、差、积、商，操作符为add、subtract、multiply、divide"""
    if operation == 'add':
        return a + b
    elif operation == 'subtract':
        return a - b
    elif operation == 'multiply':
        return a * b
    elif operation == 'divide':
        if b == 0:
            raise ValueError('除数不能为零')
        return a / b
    else:
        raise ValueError('无效的操作符')

@server.prompt
def ask_about_topic(topic: str) -> str:
    """生成请求解释特定主题的用户消息模板"""
    return f"能否请您解释一下'{topic}'这个概念？"

@server.prompt
def generate_code_request(language: str, task_description: str) -> Message:
    """生成代码编写请求的用户消息模板"""
    return Message(
        f"请用{language}编写一个实现以下功能的函数：{task_description}",
        role="user",
    )

@server.resource("resource://config")
def get_config() -> dict:
    """以JSON格式返回应用配置"""
    return {
        "theme": "dark",
        "version": "1.2.0",
        "features": ["tools", "resources"],
    }