from camel.prompts import TextPrompt

prompt=TextPrompt("我是{name}，我今年{age}岁")
print(prompt)
print(prompt.key_words)
formatted_prompt=prompt.format(name="小明", age=18)
print(formatted_prompt)








