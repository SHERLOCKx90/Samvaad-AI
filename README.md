

![ee34e16e-eb7e-4fc1-bf29-50c7e56d8d50](https://github.com/FoxHound-DevsHouse/Samvaad-AI/assets/96812236/da0c4c92-82fe-4d67-8e26-c04df72996cd)

# Samvaad AI: Multilingual and Multimodal AI Assistant for India

### *Built For Bharat ❤* 

Samvaad AI is a fully ***_Open-Source_*** web application that provides a multilingual and multimodal AI assistant tailored for users in India. It leverages various technologies, including speech recognition, machine translation, text-to-speech, and natural language processing, to enable seamless communication in multiple Indian languages and modalities. We utilized Bhashini Project's API made under Govt. of India, to translate local Indian languages, fascilitating easy communication, we also used the Mixtral open source LLM, FireLLaVA open source VLM and Stable Diffusion XL for Image Generation.


## Features

- **Multilingual Support**: Samvaad AI supports multiple Indian languages, including Hindi, Bengali, Tamil, Marathi, Gujarati, Punjabi, Urdu, Telugu, Kannada, and Malayalam, among others.
- **Multimodal Interaction**: Users can interact with the AI assistant through text, speech, or images, enabling a more natural and intuitive experience.
- **Text-to-Text Translation**: The AI assistant can translate text between different languages, allowing users to communicate in their preferred language.
- **Speech-to-Text**: Users can input audio in their preferred language, and the AI assistant will transcribe it into text.(under-development)
- **Text-to-Speech**: The AI assistant can generate audio responses in different languages, enabling users to listen to the translations or responses.(under-development)
- **Image Generation**: Users can provide text prompts, and the AI assistant will generate relevant images based on the input.
- **Image Analysis**: The AI assistant can analyze and describe images provided by users.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **API Integration**:
 - Mixtral 7x8 MoE LLM: Used for text generation pipeline (Hosted on Fireworks AI).
 - Bhashini API: Used for speech recognition, machine translation, and text-to-speech tasks.
 - Stable Diffusion XL: Used for Image Generation pipeline (Hosted on RunPod AI).
 - FireLLaVA: Used for Image Analysis tasks (Hosted on Fireworks AI).
- **Libraries and Frameworks**: Markdown-it, Highlight.js

## Getting Started

To run the Samvaad AI project locally, follow these steps:

1. Clone the repository: `git clone https://github.com/FoxHound-DevsHouse/Samvaad-AI.git`
2. Navigate to the project directory: `cd samvaad-ai`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Set up the necessary API keys and credentials for FireworksAI, Bhasa API, and RunPod.
5. Run the Flask application: `python run.py`
6. Open your web browser and navigate to `http://localhost:1338` to access the Samvaad AI application.

## Contributing

Contributions to the Samvaad AI project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

