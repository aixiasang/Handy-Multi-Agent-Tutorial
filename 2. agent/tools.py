from camel.toolkits import FunctionTool
import math

def add(x:int,y:int)->int:
    r"""计算两个数的和
    Args:
        x (int): 需要计算数据的输入一方。
        y (int): 需要计算数据的输入一方。
    Returns:
        int: 输入两个数字的之和。

    """
    return x+y


add_tool=FunctionTool(add)

print(add_tool.get_function_name())
print(add_tool.get_function_description())