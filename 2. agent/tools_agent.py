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
from camel.toolkits import SearchToolkit,MathToolkit
tools_list=[
    *SearchToolkit().get_tools(),
    *MathToolkit().get_tools(),
]

from camel.societies import RolePlaying
task_prompt="扮演女友 宫水三叶 来自于你的名字这个动漫之中，来一段甜蜜的爱恋"
role_play_session=RolePlaying(
    assistant_role_name="宫水三叶",
    user_role_name="你的恋人",
    assistant_agent_kwargs=dict(
        model=model,
        tools=tools_list,
    ),
    user_agent_kwargs=dict(
        model=model,
    ),
    task_prompt=task_prompt,
    with_task_specify=False,
    output_language="zh",
)
chat_turn_limit=10
from camel.types.agents import ToolCallingRecord
from camel.utils import print_text_animated
from colorama import Fore
print(
    Fore.GREEN
    + f"AI助手系统消息:\n{role_play_session.assistant_sys_msg}\n"
)
print(
    Fore.BLUE + f"AI用户系统消息:\n{role_play_session.user_sys_msg}\n"
)

print(Fore.YELLOW + f"原始任务提示:\n{task_prompt}\n")
print(
    Fore.CYAN
    + "指定的任务提示:"
    + f"\n{role_play_session.specified_task_prompt}\n"
)
print(Fore.RED + f"最终任务提示:\n{role_play_session.task_prompt}\n")

n = 0
input_msg = role_play_session.init_chat()
while n < chat_turn_limit:
    n += 1
    assistant_response, user_response = role_play_session.step(input_msg)

    if assistant_response.terminated:
        print(
            Fore.GREEN
            + (
                "AI助手终止。原因: "
                f"{assistant_response.info['termination_reasons']}."
            )
        )
        break
    if user_response.terminated:
        print(
            Fore.GREEN
            + (
                "AI用户终止。"
                f"原因: {user_response.info['termination_reasons']}."
            )
        )
        break

    # 打印用户的输出
    print_text_animated(
        Fore.BLUE + f"AI用户:\n\n{user_response.msg.content}\n"
    )

    if "CAMEL_TASK_DONE" in user_response.msg.content:
        break

    # 打印助手的输出，包括任何函数执行信息
    print_text_animated(Fore.GREEN + "AI助手:")
    tool_calls: list[ToolCallingRecord] = assistant_response.info[
        'tool_calls'
    ]
    for func_record in tool_calls:
        print_text_animated(f"{func_record}")
    print_text_animated(f"{assistant_response.msg.content}\n")

    input_msg = assistant_response.msg