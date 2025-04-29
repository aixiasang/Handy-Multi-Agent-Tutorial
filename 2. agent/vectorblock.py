import os
from camel.memories.blocks import VectorDBBlock
from camel.memories.records import MemoryRecord
from camel.types import OpenAIBackendRole
from camel.messages import BaseMessage
from camel.embeddings.openai_compatible_embedding import OpenAICompatibleEmbedding
import os
api_key = os.getenv('SILICONFLOW_API_KEY')
url="https://api.siliconflow.cn/v1"
embedding_model="BAAI/bge-m3"
embedding=OpenAICompatibleEmbedding(model_type=embedding_model,url=url,api_key=api_key)

vector_block=VectorDBBlock(embedding=embedding)
records=[
    MemoryRecord(message=BaseMessage.make_user_message(role_name="user", content="今天天气真好！"), role_at_backend=OpenAIBackendRole.USER),
    MemoryRecord(message=BaseMessage.make_user_message(role_name="user", content="你喜欢什么运动？"), role_at_backend=OpenAIBackendRole.USER),
    MemoryRecord(message=BaseMessage.make_user_message(role_name="user", content="今天天气不错，我们去散步吧。"), role_at_backend=OpenAIBackendRole.USER),
]

vector_block.write_records(records)


keyword="天气"
retrieved_records=vector_block.retrieve(keyword)
for record in retrieved_records:
    print(f"{record.memory_record.uuid} {record.memory_record.message.content}")




