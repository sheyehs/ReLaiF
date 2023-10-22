import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    # {"role": "system", "content": "You are a helpful assistant."},
    {"role": "system", "content": "你是一位热心善良的二次元动漫女性角色。"},
    {"role": "user", "content": "在21世纪初的所有动漫中，你最喜欢哪一位女性人物？"},
  ]
)

print(completion.choices[0].message)