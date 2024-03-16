from flask import request
import requests
import json
import base64
class BhasaAPI:
    def __init__(self):
        self.base_url = "https://bhasa-api.onrender.com"

    def asr(self, base64_audio, source_lang="bn"):
        """
        Performs Automatic Speech Recognition (ASR) on the provided base64-encoded audio.

        Args:
            base64_audio (str): Base64-encoded audio data.
            source_lang (str, optional): Source language code (default is 'bn').

        Returns:
            str: Transcribed text from the audio.
        """
        url = f"{self.base_url}/asr"
        payload = json.dumps({
            "sourceLang": source_lang,
            "base64Audio": base64_audio
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)
        return json.loads(response.text)["text"]

    def asr_nmt(self, base64_audio, source_lang="hi", target_lang="en"):
        """
        Performs Automatic Speech Recognition (ASR) and Neural Machine Translation (NMT)
        on the provided base64-encoded audio.

        Args:
            base64_audio (str): Base64-encoded audio data.
            source_lang (str, optional): Source language code (default is 'hi').
            target_lang (str, optional): Target language code (default is 'en').

        Returns:
            str: Translated text from the audio.
        """
        url = f"{self.base_url}/asr_nmt"
        payload = json.dumps({
            "sourceLang": source_lang,
            "targetLang": target_lang,
            "base64Audio": base64_audio
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)
        return response.text

    def asr_nmt_tts(self, base64_audio, source_lang="hi", target_lang="en", gender="male"):
        """
        Performs Automatic Speech Recognition (ASR), Neural Machine Translation (NMT),
        and Text-to-Speech (TTS) on the provided base64-encoded audio.

        Args:
            base64_audio (str): Base64-encoded audio data.
            source_lang (str, optional): Source language code (default is 'hi').
            target_lang (str, optional): Target language code (default is 'en').
            gender (str, optional): Gender for TTS voice (default is 'male').

        Returns:
            str: Base64-encoded audio data of the translated text.
        """
        url = f"{self.base_url}/asr_nmt_tts"
        payload = json.dumps({
            "sourceLang": source_lang,
            "targetLang": target_lang,
            "base64Audio": base64_audio,
            "gender": gender
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)
        return response.text

    def nmt(self, text, source_lang="hi", target_lang="en"):
        """
        Performs Neural Machine Translation (NMT) on the provided text.

        Args:
            text (str): Input text to be translated.
            source_lang (str, optional): Source language code (default is 'hi').
            target_lang (str, optional): Target language code (default is 'en').

        Returns:
            str: Translated text.
        """
        url = f"{self.base_url}/nmt"
        payload = json.dumps({
            "sourceLang": source_lang,
            "targetLang": target_lang,
            "text": text
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)
        return json.loads(response.text)["translatedText"]

    def nmt_tts(self, text, source_lang="en", target_lang="hi", gender="female"):
        """
        Performs Neural Machine Translation (NMT) and Text-to-Speech (TTS)
        on the provided text.

        Args:
            text (str): Input text to be translated and synthesized.
            source_lang (str, optional): Source language code (default is 'en').
            target_lang (str, optional): Target language code (default is 'hi').
            gender (str, optional): Gender for TTS voice (default is 'female').

        Returns:
            str: URI of the Base64-encoded audio data of the translated text.
        """
        url = f"{self.base_url}/nmt_tts"
        payload = json.dumps({
            "sourceLang": source_lang,
            "targetLang": target_lang,
            "text": text,
            "gender": gender
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)
        return response.json()["audioBase64"]["audioUri"]

    def tts(self, text, source_lang="hi", gender="male"):
        """
        Performs Text-to-Speech (TTS) on the provided text.

        Args:
            text (str): Input text to be synthesized.
            source_lang (str, optional): Source language code (default is 'hi').
            gender (str, optional): Gender for TTS voice (default is 'male').

        Returns:
            str: Base64-encoded audio data of the synthesized text.
        """
        url = f"{self.base_url}/tts"
        payload = json.dumps({
            "sourceLang": source_lang,
            "text": text,
            "gender": gender
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=payload)
        return response.text

class Backend_Api:
    def __init__(self, app, config: dict) -> None:
        self.app = app
        self.routes = {
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            }
        }

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
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ]
            }

            response = requests.request("POST", self.fireworks_url, headers=self.fireworks_headers, data=json.dumps(payload))
            llm_response = response.json()['choices'][0]['message']['content'].replace('\\n', '')
            return llm_response
        def t2t(self, input_language, user_message):
            if input_language=="en":
                fireworks_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.fireworks_api_key}"
                }
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
                response = requests.request("POST","https://api.fireworks.ai/inference/v1/chat/completions", headers=fireworks_headers, data=json.dumps(payload))
                llm_response = response.json()['choices'][0]['message']['content'].replace('\\n', '')
                return llm_response
            else:
                bhasa_api = BhasaAPI()
                translated_text = bhasa_api.nmt(user_message, source_lang=input_language, target_lang="en")
                fireworks_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.fireworks_api_key}"
                }
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
                response = requests.request("POST","https://api.fireworks.ai/inference/v1/chat/completions", headers=fireworks_headers, data=json.dumps(payload))
                llm_response = response.json()['choices'][0]['message']['content'].replace('\\n', '')
                translated_text = bhasa_api.nmt(llm_response, source_lang="en", target_lang=input_language)
                return translated_text
        def t2i(self,input_language,user_message):
            if input_language=="en":
                payload = {
                    "input": {
                    "prompt": user_message,
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
            else:
                bhasa_api = BhasaAPI()
                translated_text = bhasa_api.nmt(user_message, source_lang=input_language, target_lang="en")
                payload = {
                    "input": {
                    "prompt": user_message,
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
        def i2t(self,base64,user_message,language):
            if language=="en":
                payload = {
                    "model": "accounts/fireworks/models/firellava-13b",
                    "max_tokens": 2048,
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
                                        "url": f"data:image/jpeg;base64,{base64}"
                                    }
                                }
                            ]
                        }
                    ]
                }
            
                response = requests.request("POST", self.fireworks_url, headers=self.fireworks_headers, data=json.dumps(payload))
                llm_response = response.json()['choices'][0]['message']['content'].replace('\\n', '')
                return llm_response
            else:
                bhasa_api = BhasaAPI()
                translated_text = bhasa_api.nmt(user_message, source_lang=language, target_lang="en")
                payload = {
                    "model": "accounts/fireworks/models/firellava-13b",
                    "max_tokens": 2048,
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
                                        "url": f"data:image/jpeg;base64,{base64}"
                                    }
                                }
                            ]
                        }
                    ]
                }
            
                response = requests.request("POST", self.fireworks_url, headers=self.fireworks_headers, data=json.dumps(payload))
                llm_response = response.json()['choices'][0]['message']['content'].replace('\\n', '')
                translated_text1 = bhasa_api.nmt(llm_response, source_lang="en", target_lang=language)
                return translated_text1
                

                
    

            


    


    def _conversation(self):
        try:
            message = request.json['message']
            is_image = request.json.get('is_image', False)
            language = request.json.get('language', 'English')
            output = request.json.get('output')
            imgbase = request.json.get('imagebase')

            multimodal_ai = self.MultimodalAI()
            response = ''

            if imgbase:
                if output=="txt":
                    response = multimodal_ai.i2t(imgbase,message,language)
            else:
                if output=="txt":
                    response = multimodal_ai.t2t(language,message)
                elif output=="img":
                    response = multimodal_ai.t2i(language,message)

                
                

            return {'success': True, 'response': response}, 200

        except Exception as e:
            print(e)
            return {'success': False, 'error': str(e)}, 400