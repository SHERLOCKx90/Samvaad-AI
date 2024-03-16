import requests
import json

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



#from bhasa_api import BhasaAPI

# Create an instance of the BhasaAPI class
#bhasa_api = BhasaAPI()

# Use the class methods as needed
#transcribed_text = bhasa_api.asr(base64_audio, source_lang="bn")
#translated_text = bhasa_api.asr_nmt(base64_audio, source_lang="hi", target_lang="en")
#audio_base64 = bhasa_api.asr_nmt_tts(base64_audio, source_lang="hi", target_lang="en", gender="male")
#translated_text = bhasa_api.nmt(text, source_lang="hi", target_lang="en")
#audio_uri = bhasa_api.nmt_tts(text, source_lang="en", target_lang="hi", gender="female")
#audio_base64 = bhasa_api.tts(text, source_lang="hi", gender="male")

