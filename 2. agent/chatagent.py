from io import BytesIO
from PIL import Image
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.agents import ChatAgent

from dotenv import load_dotenv

import os

import requests
load_dotenv(dotenv_path='.env')

api_key = os.getenv('SILICONFLOW_API_KEY')

model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="Pro/deepseek-ai/DeepSeek-V3",
    # url='https://api-inference.modelscope.cn/v1/',
    url="https://api.siliconflow.cn/v1",
    api_key=api_key,
)

system_message ="你是一个AI助手，请根据用户的问题给出回答。"

chat_agent = ChatAgent(
    model=model,
    system_message=system_message,
    output_language="zh",
)

user_message = "你好，我是小明，请问我应该如何学习AI？"

response = chat_agent.step(user_message)

print(response.msgs[0].content)

from camel.messages import BaseMessage
user_msg_with_meta = BaseMessage.make_user_message(
    role_name="小明",
    content="我想学习计算机视觉",
    meta_dict={"processing_time": 1.23, "api_version": "v2", "user_id": "1234567890"}
)

response_with_meta = chat_agent.step(user_msg_with_meta)

print(response_with_meta.msgs[0].content)


model=ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="Qwen/QVQ-72B-Preview",
    url="https://api.siliconflow.cn/v1",
    api_key=api_key,
)

chat_agent = ChatAgent(
    model=model,
    output_language="zh",
)

url = "https://res1.vmallres.com/pimages/FssCdnProxy/vmall_product_uom/pmsSalesFile/800_800_99ED8B46BD1278B167D00B1688385FA8.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))

user_msg_with_image = BaseMessage.make_user_message(
    role_name="小明",
    content="请你解读一下这个图片内容",
    image_list=[img],
)

response_with_image = chat_agent.step(user_msg_with_image)

print(response_with_image.msgs[0].content)







