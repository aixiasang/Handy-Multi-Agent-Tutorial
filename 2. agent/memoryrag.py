from camel.memories import (
    LongtermAgentMemory,
    MemoryRecord,
    ScoreBasedContextCreator,
    ChatHistoryBlock,
    VectorDBBlock,
)
from camel.messages import BaseMessage
from camel.types import ModelType,OpenAIBackendRole
from camel.utils import OpenAITokenCounter,BaseTokenCounter
from camel.embeddings.openai_compatible_embedding import OpenAICompatibleEmbedding
import os
api_key = os.getenv('SILICONFLOW_API_KEY')
url="https://api.siliconflow.cn/v1"
embedding_model="BAAI/bge-m3"
embedding=OpenAICompatibleEmbedding(model_type=embedding_model,url=url,api_key=api_key)

memory=LongtermAgentMemory(
    context_creator=ScoreBasedContextCreator(
        token_counter=OpenAITokenCounter(ModelType.GPT_4O_MINI),
        token_limit=4096,
    ),
    chat_history_block=ChatHistoryBlock(),
    vector_db_block=VectorDBBlock(embedding=embedding)
)

records=[
    MemoryRecord(
        message=BaseMessage.make_user_message(role_name="User",content="宫水三叶你好啊！"),
        role_at_backend=OpenAIBackendRole.USER,
    ),
    MemoryRecord(
        message=BaseMessage.make_assistant_message(role_name="Agent",content="我是宫水三叶，前辈你好啊！"),
        role_at_backend=OpenAIBackendRole.ASSISTANT,
    ),
]
memory.write_records(records=records)

context,token_count=memory.get_context()
print(context)
print(token_count)

from camel.models import ModelFactory
from camel.agents import ChatAgent
from camel.types import ModelPlatformType
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="Pro/deepseek-ai/DeepSeek-V3",
    # url='https://api-inference.modelscope.cn/v1/',
    url="https://api.siliconflow.cn/v1",
    api_key=api_key,
)
sys_msg="扮演电子女友，来一段甜蜜的爱恋"
agent=ChatAgent(
    system_message=sys_msg,
    model=model,
    output_language="zh",
    tools=[]
    )

# 加载memory
agent.memory=memory

user_msg="给我讲一个甜甜的爱情故事"
response=agent.step(user_msg)

print(response.msgs[0].content)
