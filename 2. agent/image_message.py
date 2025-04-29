from PIL import Image
from io import BytesIO
import requests
from camel.messages import BaseMessage
from camel.types import RoleType

# 下载一张图片并创建一个 PIL Image 对象
url = "https://res1.vmallres.com/pimages/FssCdnProxy/vmall_product_uom/pmsSalesFile/800_800_99ED8B46BD1278B167D00B1688385FA8.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# 创建包含图片的用户消息
image_message = BaseMessage(
    role_name="User_with_image",
    role_type=RoleType.USER,
    content="Here is an image",
    meta_dict={},
    image_list=[img]  # 将图片列表作为参数传入
)

print(image_message)

# 创建用户消息
user_msg = BaseMessage.make_user_message(
    role_name="User_1",
    content="Hi, what can you do?"
)

# 创建助手消息
assistant_msg = BaseMessage.make_assistant_message(
    role_name="Assistant_1",
    content="I can help you with various tasks."
)

print("User Message:", user_msg)
print("Assistant Message:", assistant_msg)


updated_user_msg = user_msg.create_new_instance("Hi, can you tell me more about CAMEL?")
print("Updated User Message:", updated_user_msg)


msg_dict = assistant_msg.to_dict()
print("Message as dict:", msg_dict)

from camel.types import OpenAIBackendRole

openai_user_msg = user_msg.to_openai_message(role_at_backend=OpenAIBackendRole.USER)
print("OpenAI User Message:", openai_user_msg)


openai_assistant_msg = assistant_msg.to_openai_assistant_message()
print("OpenAI Assistant Message:", openai_assistant_msg)









