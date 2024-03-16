import requests

class ImageGenerator:
    def __init__(self):
        self.api_key = "PX3E31M7X73TBZQW8FL8JZ8I5GD52ALJGMTIGVD1"  # Replace with your actual API key
        self.url = "https://api.runpod.ai/v2/sdxl/runsync"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.api_key
        }

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

        response = requests.post(self.url, json=payload, headers=self.headers)
        data = response.json()
        image_url = data["output"]["image_url"]
        return image_url



#from image_generator import ImageGenerator

# Create an instance of the ImageGenerator class
#image_generator = ImageGenerator()

# Generate an image based on a user prompt
#user_prompt = "A majestic lion standing on a rock, surrounded by a beautiful sunset landscape."
#image_url = image_generator.generate_image(user_prompt)

# Print the image URL
#print(image_url)

