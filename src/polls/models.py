from pydantic import BaseModel


class Message(BaseModel):
    message_txt: str
    image: bytearray
    extras: dict
