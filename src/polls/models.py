from pydantic import BaseModel


class PollResult(BaseModel):
    message_txt: str
    image: bytearray


class PollDialogStep(BaseModel):
    message_txt: str
    extras: dict
