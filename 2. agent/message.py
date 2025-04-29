from camel.messages import BaseMessage   
from camel.types import RoleType

message = BaseMessage(
    role_name="宫水三叶",
    role_type=RoleType.USER,
    content="""你好呀，我是宫水三叶，一个喜欢研究AI的女孩。""",
    meta_dict={}
)
print(message)




