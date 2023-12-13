from pydantic import BaseModel


class Poll(BaseModel):
    id: int
    created_at: str
    ptype: str
    p_telegram_id: str
    chat_id: str
    dialog_machine: bytes
    result: str


class Message(BaseModel):
    message_txt: str
    image: bytes
    extras: dict


class PollResult(BaseModel):
    id: int
    created_at: str
    result_key: str
    message_txt: str
    image: bytes
    extras: dict


class PollStep(BaseModel):
    id: int
    created_at: str
    step_key: str
    message_txt: str
    image: bytes
    extras: dict
