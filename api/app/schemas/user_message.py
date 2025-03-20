from pydantic import BaseModel

class UserMessage(BaseModel):
    message: str
    thread_id: str