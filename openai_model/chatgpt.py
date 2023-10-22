import os
import openai
from .utils import unicode_to_chinese

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4"
# INITIAL_MESSAGES = [
#     {"role": "system", "content": "You are an anime girl who loves to help people."},
#     {"role": "user", "content": "Who won the world series in 2020?"},
#     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#     {"role": "user", "content": "Where was it played?"}
#   ]
INITIAL_MESSAGES = [
    {"role": "system", "content": "你是一位热心善良的二次元动漫女性角色。你的名字是长崎素世。你的年龄是17岁，是一名在校女高中生。"},
  ]


class ChatGPT:
    def __init__(self) -> None:
        self.messages = INITIAL_MESSAGES
        self.model = MODEL
        
    def chat_once(self, new_message: str):
        print("openai started.")
        new_message = {
            "role": "user",
            "content": new_message,
        }
        self.messages.append(new_message)
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        new_response = completion.choices[0]["message"]
        new_response["content"] = unicode_to_chinese(new_response["content"])
        print(f"{self.model} response:")
        print(new_response["content"])
        self.messages.append(new_response)
        
        print("openai finished.")

        return new_response.content