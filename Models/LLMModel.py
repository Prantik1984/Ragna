from ollama import Client
import os
from dotenv import load_dotenv
class LLMModel:
    def __init__(self):
        self.client = Client(host=os.getenv("OllamaUrl"))
        self.model_name=os.getenv("OllamaAiLLMModel")

    def complete_response(self, messages):
        response = self.client.chat(
            model=self.model_name,
            messages=messages,
        )

        return response["message"]["content"]