from camel.messages import BaseMessage  
from camel.types import RoleType
from camel.responses import ChatAgentResponse

response = ChatAgentResponse(
    msgs=[
        BaseMessage(
            role_name="小明",
            role_type=RoleType.USER,
            content="你好，我是小明，请问我应该如何学习AI？",
            meta_dict={}
        ),
    ],
    terminated=False,
    info={"usage": {"prompt_tokens": 10, "completion_tokens": 15}}  
)

messages=response.msgs
is_terminated=response.terminated
additional_info=response.info

print(messages[0].content)
print(is_terminated)
print(additional_info)








