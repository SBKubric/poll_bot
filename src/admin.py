from fastapi import FastAPI
from sqladmin import Admin, ModelView

from core.config import settings
from db import models
from db.database import async_engine

app = FastAPI(title=settings.project_name)
admin = Admin(app, async_engine)


class PollAdmin(ModelView, model=models.Poll):
    column_list = [models.Poll.id]  # type: ignore


class PollStepAdmin(ModelView, model=models.PollStep):
    column_list = [models.PollStep.id]  # type: ignore


class PollResultAdmin(ModelView, model=models.PollResult):
    column_list = [models.PollResult.id]  # type: ignore


admin.add_view(PollStepAdmin)
admin.add_view(PollAdmin)
admin.add_view(PollResultAdmin)
