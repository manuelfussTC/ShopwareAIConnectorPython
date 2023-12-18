import requests
import json


class GPTCommunicator:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_gpt_request(self, prompt, model="gpt-4-1106-preview"):
        print(f"Anfrage an GPT: {prompt[:200]}...")
        api_url = 'https://api.openai.com/v1/chat/completions'

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        post_fields = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4000,
            "temperature": 0,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

        response = requests.post(api_url, headers=headers, json=post_fields)

        if response.status_code != 200:
            print(f'GPT-Anfrage fehlgeschlagen: {response.text}')
            raise Exception(f'GPT Request Failed: {response.text}')
        print("Antwort von GPT erhalten.")
        return response.json()

    def generate_response(self, prompt, first_prompt):
        try:
            model_1 = "gpt-4-1106-preview"
            model_2 = "gpt-4"

            response = self.send_gpt_request(prompt, model_1)
            if not response:
                response = self.send_gpt_request(prompt, model_2)

            self.process_gpt_response(response, first_prompt)
        except Exception as e:
            print(f'Error: {e}')

    def process_gpt_response(self, gpt_response, first_prompt):
        # Verarbeite die GPT-Antwort. Diese Methode muss basierend auf deinen Anforderungen implementiert werden.
        pass
