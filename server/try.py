from multimodal import MultimodalAI
import base64

#Instantiate the MultimodalAI class
multimodal_ai = MultimodalAI()

#Generate text response
text_prompt = "Hello, how are you?"
text_response = multimodal_ai.generate_text(text_prompt)
print(f"{text_response}")

#Generate image
image_prompt = "A majestic lion standing on a rock, surrounded by a beautiful sunset landscape."
image_url = multimodal_ai.generate_image(image_prompt)
print(f"{image_url}")

#Generate text response from image Load and example image and encode it as base64
with open("example_image.png", "rb") as image_file:
    image_data = image_file.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

user_message_with_image = "Describe the image."
text_response_from_image = multimodal_ai.generate_text_from_image(image_base64, user_message_with_image)
print(f"{text_response_from_image}")
