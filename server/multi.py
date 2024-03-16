import requests
import json
import base64

class MultimodalAI:
    def __init__(self):
        # FireworksAI API credentials
        self.fireworks_api_key = "3J2VhOCg9nJF30zpLUJvlALsMAM0zG6b9KjJf1PhX7mx7GIn"
        self.fireworks_url = "https://api.fireworks.ai/inference/v1/chat/completions"
        self.fireworks_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.fireworks_api_key}"
        }

        # RunPod API credentials
        self.runpod_api_key = "PX3E31M7X73TBZQW8FL8JZ8I5GD52ALJGMTIGVD1"
        self.runpod_url = "https://api.runpod.ai/v2/sdxl/runsync"
        self.runpod_headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.runpod_api_key
        }

    class FireworksAIClient:
        def __init__(self, url):
            self.api_key = "3J2VhOCg9nJF30zpLUJvlALsMAM0zG6b9KjJf1PhX7mx7GIn"
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

    def generate_text(self, user_message):
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

        response = requests.request("POST", self.fireworks_url, headers=self.fireworks_headers, data=json.dumps(payload))
        llm_response = response.json()['choices'][0]['message']['content'].replace('\\n', '')
        return llm_response

    def generate_image(self, user_prompt):
        payload = {
            "input": {
                "prompt": user_prompt,
                "num_inference_steps": 50,
                "refiner_inference_steps": 60,
                "width": 1024,
                "height": 1024,
                "guidance_scale": 10,
                "strength": 0.5,
                "seed": None,
                "num_images": 1,
                "negative_prompt": "bad anatomy, bad hands, three hands, three legs, bad arms, missing legs, missing arms, poorly drawn face, bad face, fused face, cloned face, worst face, three crus, extra crus, fused crus, worst feet, three feet, fused feet, fused thigh, three thigh, fused thigh, extra thigh, worst thigh, missing fingers, extra fingers, ugly fingers, long fingers, horn, extra eyes, huge eyes, 2girl, amputation, disconnected limbs, cartoon, cg, 3d, unreal, animate"
            }
        }

        response = requests.post(self.runpod_url, json=payload, headers=self.runpod_headers)
        data = response.json()
        image_url = data["output"]["image_url"]
        return image_url

    def generate_text_from_image(self, image_base64, user_message):
        fireworks_client = self.FireworksAIClient(self.fireworks_url)
        text_response = fireworks_client.get_response(image_base64, user_message)
        return text_response


#from multimodal import MultimodalAI
#import base64

#Instantiate the MultimodalAI class
#multimodal_ai = MultimodalAI()

#Generate text response
#text_prompt = "Hello, how are you?"
#text_response = multimodal_ai.generate_text(text_prompt)
#print(f"{text_response}")

#Generate image
#image_prompt = "A majestic lion standing on a rock, surrounded by a beautiful sunset landscape."
#image_url = multimodal_ai.generate_image(image_prompt)
#print(f"{image_url}")

#Generate text response from image
#Load and example image and encode it as base64
#with open("example_image.png", "rb") as image_file:
#    image_data = image_file.read()
#    image_base64 = base64.b64encode(image_data).decode('utf-8')

#user_message_with_image = "Describe the image."
#text_response_from_image = multimo dal_ai.generate_text_from_image(image_base64, user_message_with_image)
#print(f"{text_response_from_image}")
