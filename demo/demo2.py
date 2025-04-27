from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.messages import BaseMessage

from io import BytesIO
import requests
from PIL import Image
import os


model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="Qwen/QVQ-72B-Preview",
    url='https://api-inference.modelscope.cn/v1/',
    api_key=os.getenv('MODEL_SCOPE_API_KEY')
)

agent = ChatAgent(
    model=model,
    output_language='中文'
)

# 图片URL
url = "https://res1.vmallres.com/pimages/FssCdnProxy/vmall_product_uom/pmsSalesFile/800_800_99ED8B46BD1278B167D00B1688385FA8.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))

user_msg = BaseMessage.make_user_message(
    role_name="User", 
    content="华为手机", 
    image_list=[img]  
)

response = agent.step(user_msg)
print(response.msgs[0].content)

