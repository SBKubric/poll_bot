import pickle

from db import managers
from polls.pet_advisor import PetAdvisorPoll


async def get_by_ids(user_id: str, chat_id: str) -> PetAdvisorPoll:
    poll_id: int | None = await managers.get_poll_id_by_tg_id(user_id, chat_id)
    if not poll_id:
        return PetAdvisorPoll(user_id, chat_id)
    pickled = await managers.get_poll(poll_id)
    if not pickled:
        return PetAdvisorPoll(user_id, chat_id)
    return pickle.loads(pickled)


async def stop_poll_by_ids(user_id: str, chat_id: str) -> None:
    poll_id: int | None = await managers.get_poll_id_by_tg_id(user_id, chat_id)
    if not poll_id:
        return
    await managers.terminate_poll(poll_id)


async def start_new_poll(user_id: str, chat_id: str) -> PetAdvisorPoll:
    await stop_poll_by_ids(user_id, chat_id)
    return PetAdvisorPoll(user_id, chat_id)
