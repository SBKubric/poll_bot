import logging

import sqlalchemy as sa
from cache import AsyncTTL

from db import models
from db.database import SessionLocal


async def create_poll(user_id: str, chat_id: str) -> int:
    async with SessionLocal() as session:
        poll = models.Poll(p_telegram_id=user_id, chat_id="temp")
        session.add(poll)
        await session.commit()
        logging.debug("Poll created: %s", poll.id)
        return int(poll.id)  # type: ignore


async def terminate_poll(poll_id: int) -> None:
    async with SessionLocal() as session:
        poll = await session.get(models.Poll, poll_id)
        if not poll:
            return
        await session.execute(
            sa.update(models.Poll)
            .where(models.Poll.id == poll_id)
            .values(is_terminated=True)
        )
        await session.commit()
        logging.debug("Poll terminated: %s", poll)


async def delete_poll(poll_id: int) -> None:
    async with SessionLocal() as session:
        await session.execute(sa.delete(models.Poll).where(models.Poll.id == poll_id))
        await session.commit()


async def get_poll(poll_id: int) -> bytes | None:
    async with SessionLocal() as session:
        poll = await session.get(models.Poll, poll_id)
        if not poll:
            logging.debug('No poll with id "{}"'.format(poll_id))
            return None
        logging.debug("Found poll: %s", poll)
        return poll.dialog_machine  # type: ignore


async def persist_poll(poll_id: int, poll: bytes) -> None:
    async with SessionLocal() as session:
        poll_obj = await session.get(models.Poll, poll_id)
        if not poll_obj:
            logging.error('No poll with id "{}"'.format(poll_id))
            return
        await session.execute(
            sa.update(models.Poll)
            .where(models.Poll.id == poll_id)
            .values(dialog_machine=poll)
        )
        await session.commit()
        logging.debug("Persisted poll: %s", poll_id)


async def get_poll_id_by_tg_id(user_id: str, chat_id: str) -> int | None:
    async with SessionLocal() as session:
        polls = await session.execute(
            sa.select(models.Poll)
            .where(
                models.Poll.p_telegram_id == user_id,
                models.Poll.chat_id == "temp",
                models.Poll.is_terminated == False,
            )
            .order_by(models.Poll.created_at.desc())
            .limit(1)
        )
        poll = polls.scalars().first()
        if not poll:
            logging.debug(
                'No poll with user_id "{}" and chat_id "{}"'.format(user_id, "temp")
            )
            return None
        logging.debug(
            f"Found poll: {poll.id} with user_id: {user_id} and chat_id: temp"
        )
        return int(poll.id)  # type: ignore


@AsyncTTL(time_to_live=60, maxsize=1024)
async def get_poll_steps() -> dict[str, models.PollStep]:
    async with SessionLocal() as session:
        poll_steps = await session.execute(sa.select(models.PollStep))
        return {step.step_key: step for step in poll_steps.scalars().all()}  # type: ignore


@AsyncTTL(time_to_live=60, maxsize=1024)
async def get_poll_results() -> dict[str, list[models.PollStep]]:
    async with SessionLocal() as session:
        poll_results = await session.execute(sa.select(models.PollResult))
        results = {}
        for result in poll_results.scalars().all():
            if result.result_key not in results:
                results[result.result_key] = []
            results[result.result_key].append(result)
        return results
