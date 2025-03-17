import openai
import requests
import time
import google.generativeai as genai

block_paid_apis = False  # Define it directly to avoid circular import



class OpenAIWriter:
    def __init__(
        self,
        system_context="You are an automated assistant. Your top goal is to answer questions to the best of your ability"
    ):
        self.client = openai.OpenAI(
            base_url="https://api.openai.com/v1",
            api_key="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"
        )
        self.system_context = system_context

    def write(self, prompt):
        if block_paid_apis:
            return ""
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_context},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content


class LlamacppWriter:
    def __init__(
        self,
        temperature=0.5,
        n_predict=4000,
        system_context="You are an automated assistant. Your top goal is to answer questions to the best of your ability",
    ):
        self.system_context = system_context
        self.temperature = temperature
        self.n_predict = n_predict

    def write(self, prompt):
        json = {
            'prompt': f"system: {self.system_context}\nuser: {prompt}",
        }
        response = requests.post(f"http://127.0.0.1:{port}/completion", json=json)
        return response.json()["content"].strip()


class Gemini15Writer:
    def __init__(
        self,
        system_context="You are an automated assistant. Your top goal is to answer questions to the best of your ability"
    ):
        model_name = "gemini-1.5-pro-latest"
        self.minimum_time_between_writes = 31
        self.last_write_time = 0
        genai.configure(api_key="your-gemini-api-key-here")
        config = {
            "max_output_tokens": 8192,
            "temperature": 0.7,
            "top_p": 1
        }
        dumb_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ]
        self.model = genai.GenerativeModel(
            model_name,
            generation_config=config,
            safety_settings=dumb_settings
        )
        self.system_context = system_context

    def write(self, prompt):
        while True:
            if time.time() - self.last_write_time >= self.minimum_time_between_writes:
                chat = self.model.start_chat(history=[])
                chat.send_message(f"{self.system_context} {prompt}")
                response = chat.last.text
                self.last_write_time = time.time()
                return response
            else:
                time.sleep(1)


class Gemini10Writer:
    def __init__(
        self,
        system_context="You are an automated assistant. Your top goal is to answer questions to the best of your ability"
    ):
        model_name = "gemini-1.0-pro-latest"
        self.minimum_time_between_writes = 1
        self.last_write_time = 0
        genai.configure(api_key="your-gemini-api-key-here")
        config = {
            "max_output_tokens": 8192,
            "temperature": 0.7,
            "top_p": 1
        }
        dumb_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ]
        self.model = genai.GenerativeModel(
            model_name,
            generation_config=config,
            safety_settings=dumb_settings
        )
        self.system_context = system_context

    def write(self, prompt):
        while True:
            if time.time() - self.last_write_time >= self.minimum_time_between_writes:
                chat = self.model.start_chat(history=[])
                chat.send_message(f"{self.system_context} {prompt}")
                response = chat.last.text
                self.last_write_time = time.time()
                return response
            else:
                time.sleep(1)
