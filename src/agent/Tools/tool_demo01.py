from typing import Annotated

from langchain_core.tools import tool


@tool('calculate')
def calculate(
        a: Annotated[float, '这是第一个参数']
        , b: Annotated[float, '这是第二个参数']
        , operation: Annotated[str, '这是操作符']
) -> float:
    """计算两个数的和、差、积、商，操作符为add、subtract、multiply、divide，结果为float类型"""
    result = 0.0
    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        if b == 0:
            raise ValueError('除数不能为零')
        result = a / b
    else:
        raise ValueError('无效的操作符')
    return result


# print(calculate.description)
# print(calculate.name)
# print(calculate.args_schema.model_fields)
# print(calculate.return_direct)
