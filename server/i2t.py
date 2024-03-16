import requests
import json

class FireworksAIClient:
    def __init__(self, url):
        self.api_key = "3J2VhOCg9nJF30zpLUJvlALsMAM0zG6b9KjJf1PhX7mx7GIn"  # Your API key goes here
        self.url = url
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_response(self, base64code, user_message):
        payload = {
            "model": "accounts/fireworks/models/firellava-13b",
            "max_tokens": 512,
            "top_p": 1,
            "top_k": 40,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "temperature": 0.6,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_message
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64code}"
                            }
                        }
                    ]
                }
            ]
        }

        response = requests.request("POST", self.url, headers=self.headers, data=json.dumps(payload))
        llm_response = response.json()['choices'][0]['message']['content'].replace('\\n', '')
        return llm_response

