from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from mimetypes import guess_type
from typing import List
import base64, os

load_dotenv()
ai_foundry_project_key=os.getenv("AZURE_AI_FOUNDRY_PROJECT_KEY")
phi_4_deployment_url = os.getenv("AZURE_PHI_4_MULTIMODAL_DEPLOYMENT_URL")
phi_4_deployment_key = os.getenv("AZURE_PHI_4_MULTIMODAL_DEPLOYMENT_KEY")
gpt_4_o_deployment_url = os.getenv("AZURE_GPT_4_O_DEPLOYMENT_URL")
gpt_4_o_deployment_key = os.getenv("AZURE_GPT_4_O_DEPLOYMENT_KEY")

class Assistant:
    def __init__(self, endpoint, credential, model=None):
        self.client = ChatCompletionsClient(endpoint=endpoint, credential=credential, model=model)
    
    def generate_response(self, messages: List[dict], generation_config: dict = None):
        try:
            response = self.client.complete(messages=messages, **(generation_config or {}))
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred generating response: {e}"

class TravelImageAnalyzer(Assistant):
    def __init__(self, endpoint=phi_4_deployment_url, credential=AzureKeyCredential(phi_4_deployment_key), model="phi-4-multimodal"):
        super().__init__(endpoint, credential, model)

    def respond_to_upload(self, image_data_url:str):
        """Process uploaded image and generate travel insights."""
        # Example: Sending the extracted data to the LLM
        messages=[{
            "role": "user",
            "content": [
                {
                    "text": """
                    You are a travel AI assistant that analyzes images to extract key elements for personalized trip planning. Your goal is to:
- Identify landmarks, scenery, and locations.
- Suggest specific travel destinations.
- Describe the overall vibe and potential travel experience.
- Suggest relevant activities based on the image.
- Extract keywords for trip recommendations.
- Provide your response in a focused and conscice manner. 
                    """,
                    "type": "text",
                },
                {"image_url": {"url": image_data_url}, "type": "image_url"},
            ],
        }]

        response = self.generate_response(messages)
        print(f"Response from image analysis: {response}")
        return response


def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = "application/octet-stream"  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode("utf-8")

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"



