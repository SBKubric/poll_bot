from functools import cache

import sqlalchemy as sa

from db import models
from db.database import SessionLocal


async def persist_poll(poll_id: int, poll: bytes) -> None:
    async with SessionLocal() as session:
        session.add(models.Poll(id=poll_id, dialog_machine=poll))
        await session.commit()


async def create_poll(user_id: str, chat_id: str) -> int:
    async with SessionLocal() as session:
        poll = models.Poll(p_telegram_id=user_id, chat_id=chat_id)
        session.add(poll)
        await session.commit()
        return int(poll.id)  # type: ignore


async def delete_poll(poll_id: int) -> None:
    async with SessionLocal() as session:
        await session.execute(sa.delete(models.Poll).where(models.Poll.id == poll_id))
        await session.commit()


async def get_poll(poll_id: int) -> bytes | None:
    async with SessionLocal() as session:
        poll = await session.get(models.Poll, poll_id)
        if not poll:
            return None
        return poll.dialog_machine  # type: ignore


async def get_poll_id_by_tg_id(user_id: str, chat_id: str) -> int | None:
    async with SessionLocal() as session:
        poll = await session.execute(
            sa.select(models.Poll)
            .where(models.Poll.p_telegram_id == user_id, models.Poll.chat_id == chat_id)
            .order_by(models.Poll.created_at.desc())
            .limit(1)
        )
        if not poll:
            return None
        return int(poll.scalar().id)  # type: ignore


@cache
async def get_poll_steps() -> dict[str, models.PollStep]:
    async with SessionLocal() as session:
        poll_steps = await session.execute(sa.select(models.PollStep))
        return {step.step_key: step for step in poll_steps.scalars().all()}  # type: ignore


@cache
async def get_poll_results() -> dict[str, list[models.PollStep]]:
    async with SessionLocal() as session:
        poll_results = await session.execute(sa.select(models.PollResult))
        results = {}
        for result in poll_results.scalars().all():
            if result.result_key not in results:
                results[result.result_key] = []
            results[result.result_key].append(result)
        return results
