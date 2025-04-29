from io import BytesIO
from PIL import Image
from camel.models import ModelFactory
from camel.types import ModelPlatformType, TaskType
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
from camel.agents import TaskSpecifyAgent
my_prompt_template="""
    'Here is a task: I\'m a {occupation} and I want to {task}. Help me to make this task more specific.'
"""
task_specify_agent=TaskSpecifyAgent(
    model=model,
    task_type=TaskType.AI_SOCIETY,
    output_language="zh",
)
specify_task_prompt=task_specify_agent.run(
    task_prompt="get promotion",
    meta_dict=dict(occupation="Software Engineer"),
)

print(specify_task_prompt)


