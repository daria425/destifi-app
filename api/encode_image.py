import base64
def encode_image(image_path:str)->bytes:
    with open(image_path,"rb") as image_file:
        encoded_image=image_file.read()
        return encoded_image
