import requests
import json

class FireworksAI:
    def __init__(self):
        self.api_key = "D9qC7JJY93GHq4NClIiTGZ2X23TA8nSYwexHsVoXSsxzVKdZ"  # Replace 'YOUR_API_KEY' with your actual API key
        self.url = "https://api.fireworks.ai/inference/v1/chat/completions"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def generate_response(self, user_message):
        payload = {
            "model": "accounts/fireworks/models/mixtral-8x7b-instruct",
            "max_tokens": 4096,
            "top_p": 1,
            "top_k": 40,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "temperature": 0.6,
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }

        response = requests.request("POST", self.url, headers=self.headers, data=json.dumps(payload))
        llm_response = response.json()['choices'][0]['message']['content'].replace('\\n', '')
        return llm_response


# Import the class
#from fireworks_ai import FireworksAI

# Instantiate the FireworksAI class
#fireworks_ai = FireworksAI()

# User's message
#user_message = "Hello, how are you?"

# Generate response
#response = fireworks_ai.generate_response(user_message)

# Print the response
#print(response)
