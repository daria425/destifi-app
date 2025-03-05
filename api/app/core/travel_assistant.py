from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from mimetypes import guess_type
import base64, os, json

load_dotenv()
url = os.getenv("AZURE_CHAT_COMPLETIONS_URL")
key = os.getenv("AZURE_CHAT_COMPLETIONS_KEY")


class TravelAssistant:
    def __init__(self):
        self.messages = []
        self.client = ChatCompletionsClient(
            endpoint=url, credential=AzureKeyCredential(key)
        )

    def respond_to_user(self, message):
        self.messages.append(message)
        response = self.client.complete(
            messages=self.messages, temperature=0, max_tokens=1000
        )
        assistant_response = {
            "role": "assistant",
            "content": response.choices[0].message.content,
        }
        self.messages.append(assistant_response)
        return response.choices[0].message.content

    def respond_to_uploaded_image(self, image_data_url: str):
        message = {
            "role": "user",
            "content": [
                {
                    "text": "You are a helpful travel assistant. I would like to have a vacation like this image. Suggest some locations and ask me a list of follow up questions such as: budget, duration, time of year, etc. Finish every response with a list of follow up questions",
                    "type": "text",
                },
                {"image_url": {"url": image_data_url}, "type": "image_url"},
            ],
        }

        self.messages.append(message)
        response = self.client.complete(messages=self.messages, max_tokens=1000)
        assistant_response = {
            "role": "assistant",
            "content": response.choices[0].message.content,
        }
        self.messages.append(assistant_response)
        self.messages=self.messages[1:]
        return response.choices[0].message.content
    
    def summarize_conversation(self):
        conversation=json.dumps(self.messages)
        message={"role":"user", "content":f"From the conversation, extract the type of vacation the user would like to have and provide a final recommendation, including any details useful for planning a vacation. Do not state if a user has not mentioned something. Conversation: {conversation}"}
        self.messages.append(message)
        response = self.client.complete(messages=self.messages, temperature=0, max_tokens=1000)
        assistant_response = {
            "role": "assistant",
            "content": response.choices[0].message.content,
        }
        self.messages.append(assistant_response)
        return response.choices[0].message.content




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

# assistant=TravelAssistant()
# image_url = "./app/assets/images/sample_image_2.jpg"
# image_data_url = local_image_to_data_url(image_url)
# response=assistant.respond_to_uploaded_image(image_data_url)
# print(response)
# print("-------")
# user_message={
#     "role":"user",
#     "content":"I would like to go in the summer and stay in a budget accomodation, it will be a solo trip"
  
# }
# response=assistant.respond_to_user(user_message)
# print(response)
# print("-------")
# user_message={
#     "role":"user",
#     "content":"Im interested in experiencing the local culture but I dont want a long flight, I'll be travelling from London"
# }
# response=assistant.respond_to_user(user_message)
# print(response)
# print("-------")
# summary=assistant.summarize_conversation()
# print(summary)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         