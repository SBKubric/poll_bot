import sqlalchemy as sa
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy.orm import Mapped, relationship

from core.config import settings
from db.database import Base


class Poll(Base):
    __tablename__ = "polls"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    ptype = sa.Column(sa.String(30), default="pet_advisor")
    p_telegram_id = sa.Column(sa.String(255))
    chat_id = sa.Column(sa.String(255))
    is_terminated = sa.Column(sa.Boolean, default=False)
    dialog_machine = sa.Column(sa.LargeBinary, nullable=True)
    result_id = sa.Column(sa.Integer, sa.ForeignKey("poll_results.id"), nullable=True)
    result: Mapped["PollResult"] = relationship("PollResult")

    def __repr__(self):
        return f"<Item(id={self.id}, ptype='{self.ptype}', p_telegram_id={self.p_telegram_id}, chat_id={self.chat_id}, is_terminated={self.is_terminated})>"


class PollResult(Base):
    __tablename__ = "poll_results"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    result_key = sa.Column(sa.String(255), index=True)
    message_txt = sa.Column(sa.Text, nullable=True)
    image = sa.Column(
        FileType(FileSystemStorage(path=settings.media_path)), nullable=True
    )
    extras = sa.Column(sa.JSON, nullable=True)


class PollStep(Base):
    __tablename__ = "poll_steps"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    step_key = sa.Column(sa.String(255), index=True)
    message_txt = sa.Column(sa.Text, nullable=True)
    image = sa.Column(
        FileType(FileSystemStorage(path=settings.media_path)), nullable=True
    )
    extras = sa.Column(sa.JSON, nullable=True)
