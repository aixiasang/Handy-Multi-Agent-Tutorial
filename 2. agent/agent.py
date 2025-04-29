import os

from camel.agents import ChatAgent
from camel.configs import ZhipuAIConfig
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

model = ModelFactory.create(
    model_platform=ModelPlatformType.ZHIPU,
    model_type=ModelType.GLM_4,
    model_config_dict=ZhipuAIConfig(temperature=0.2).as_dict(),
    api_key=os.environ.get("zhipuai"),
    url="https://open.bigmodel.cn/api/paas/v4/",
)

# 设置system prompt
sys_msg = BaseMessage.make_assistant_message(
    role_name="Assistant",
    content="You are a helpful assistant.",
)

# 初始化agent
camel_agent = ChatAgent(system_message=sys_msg, model=model, output_language="zh")#这里同样可以设置输出语言

user_msg = BaseMessage.make_user_message(
    role_name="User",
    content="""Say hi to CAMEL AI, one open-source community 
    dedicated to the study of autonomous and communicative agents.""",
)


# 调用模型
response = camel_agent.step(user_msg)
print(response.msgs[0].content)
