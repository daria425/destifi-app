from firebase_admin import auth
from app.utils.logger import logger
def decode_token(id_token:str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        logger.info(f"Token verified")
        return decoded_token
    except auth.InvalidIdTokenError:
        logger.error("Invalid ID token")
        return None

def get_token_data(id_token:str):
    print(id_token)
    decoded_token=decode_token(id_token)
    if decoded_token:
        user_data = {
        "uid": decoded_token["uid"],
        "email": decoded_token.get("email"),
        "display_name": decoded_token.get("name"),
        "photo_url": decoded_token.get("picture"),
        "sign_in_provider": decoded_token["firebase"]["sign_in_provider"],
        "auth_time": decoded_token["auth_time"],
        "created_at": decoded_token["iat"]
    }
        return user_data
    else:
        return None
    
    