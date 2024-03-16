import requests
import json

class TaskClassifier:
    def __init__(self):
        self.url = "https://api.fireworks.ai/inference/v1/completions"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer 3J2VhOCg9nJF30zpLUJvlALsMAM0zG6b9KjJf1PhX7mx7GIn"
        }
        self.payload = {
            "model": "accounts/fireworks/models/mixtral-8x7b-instruct",
            "max_tokens": 5,
            "top_p": 1,
            "top_k": 40,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "temperature": 0.1,
            "prompt": "You are an intermediate system AI system that classifies the task given by the user into one of the predefined pipelines, so that the appropriate pipeline is used in the step , available pipelines [ t2i (text to image) , t2t (text to text) , i2t (image to text) , t2s (text to speech) , i2s (image to speech) ]\n\nExample :\n\nUSER: Generate an image of A Dog in a playground\n\nASSISTANT: {t2i}\n\nUSER: Can you say what is happening in this (IMG IS UPLOADED)\n\nASSISTANT: {i2t}\n\nUSER: Translate this and read it aloud (IMG IS UPLOADED)\n\nASSISTANT: {i2s}\n\nUSER: Who was the first president of India?\n\nASSISTANT:{t2t}\n\nUSER: Describe the weather in Tokyo right now.\n\nASSISTANT: {t2t}\n\nUSER: Show me a picture of the Eiffel Tower at night.\n\nASSISTANT: {t2i}\n\nUSER: Convert this handwritten letter into text.\n\nASSISTANT: {i2t}\n\nUSER: Read aloud this passage from Shakespeare's \"Hamlet.\"\n\nASSISTANT: {t2s}\n\nUSER: Generate a poem about love.\n\nASSISTANT: {t2t}\n\nUSER: What breed is this dog? (IMG IS UPLOADED)\n\nASSISTANT: {i2t}\n\nUSER: Can you summarize the plot of \"To Kill a Mockingbird\"?\n\nASSISTANT: {t2t}\n\nUSER: Translate this Chinese text into English.\n\nASSISTANT: {t2t}\n\nUSER: Describe the Mona Lisa painting by Leonardo da Vinci.\n\nASSISTANT: {t2t}\n\nUSER: Identify the objects in this image. (IMG IS UPLOADED)\n\nASSISTANT: {i2t}\n\nUSER: Convert this PDF document into spoken words.\n\nASSISTANT: {t2s}\n\nUSER: Generate a recipe for lasagna.\n\nASSISTANT: {t2t}\n\nUSER: Show me a picture of a tropical beach.\n\nASSISTANT: {t2i}\n\nUSER: Summarize the latest research on climate change.\n\nASSISTANT: {t2t}\n\nUSER: Convert this mathematical equation into spoken words.\n\nASSISTANT: {t2s}\n\nUSER: What is the meaning of this symbol? (IMG IS UPLOADED)\n\nASSISTANT: {i2t}\n\nUSER: Describe the style of architecture in ancient Rome.\n\nASSISTANT: {t2t}\n\nUSER: Translate this French poem into Spanish.\n\nASSISTANT: {t2t}\n\nUSER: Generate a speech about the importance of education.\n\nASSISTANT: {t2t}\n\nUSER: Identify the landmarks in this cityscape. (IMG IS UPLOADED)\n\nASSISTANT: {i2t}\n\nUSER: Describe the behavior of dolphins.\n\nASSISTANT: {t2t}\n\nUSER: Create a logo for my company.\n\nASSISTANT: {t2i}\n\nUSER: Convert this audio recording into text.\n\nASSISTANT: {i2t}\n\nUSER: Read aloud the lyrics of \"Bohemian Rhapsody\" by Queen.\n\nASSISTANT: {t2s}\n\nUSER: Generate a synopsis for a science fiction novel.\n\nASSISTANT: {t2t}\n\nUSER: What type of bird is shown in this picture? (IMG IS UPLOADED)\n\nASSISTANT: {i2t}\n\nUSER: Summarize the main events of World War II.\n\nASSISTANT: {t2t}\n\nUSER: Translate this Japanese website into English.\n\nASSISTANT: {t2t}\n\nUSER: Describe the process of photosynthesis.\n\nASSISTANT: {t2t}\n\nUSER: Convert this graph into spoken words.\n\nASSISTANT: {t2s}\n\nUSER: Identify the artist of this painting. (IMG IS UPLOADED)\n\nASSISTANT: {i2t}\n\nUSER: Summarize the plot of \"The Great Gatsby.\"\n\nASSISTANT: {t2t}\n\nUSER: Translate this Russian document into French.\n\nASSISTANT: {t2t}\n\nUSER: Create a storyboard for a short film.\n\nASSISTANT: {t2i}\n\nUSER: Convert this video into a written transcript.\n\nASSISTANT: {i2t}\n\nUSER: Describe the characteristics of a black hole.\n\nASSISTANT: {t2t}\n\nUSER: Generate a logo for a fitness center.\n\nASSISTANT: {t2i}\n\nUSER: Convert this recipe into spoken instructions.\n\nASSISTANT: {t2s}\n\nUSER: Identify the constellations in this night sky. (IMG IS UPLOADED)\n\nASSISTANT: {i2t}\n\nUSER: Summarize the history of ancient Egypt.\n\nASSISTANT: {t2t}\n\nUSER: Read aloud this excerpt from Martin Luther King Jr.'s \"I Have a Dream\" speech. (IMG IS UPLOADED)\n\nASSISTANT: {i2s}\n\nUSER: "
        }

    def classify_task(self, user_prompt):
        self.payload["prompt"] += f"USER: {user_prompt}\n\nASSISTANT:"
        response = requests.request("POST", self.url, headers=self.headers, data=json.dumps(self.payload))
        llm_response = response.json()['choices'][0]['text']
        return llm_response

