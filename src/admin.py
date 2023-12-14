from fastapi import FastAPI
from sqladmin import Admin, ModelView

from core.config import settings
from db import models as m
from db.database import async_engine

app = FastAPI(title=settings.project_name)
admin = Admin(app, async_engine)


class PollAdmin(ModelView, model=m.Poll):
    column_list = [m.Poll.id]  # type: ignore


class PollStepAdmin(ModelView, model=m.PollStep):
    column_list = [m.PollStep.id, m.PollStep.step_key]  # type: ignore
    column_filters = [m.PollStep.id, m.PollStep.step_key]
    # column_default_sort = [m.PollStep.step_key]
    column_details_list = [  # type: ignore
        m.PollStep.id,
        m.PollStep.created_at,
        m.PollStep.step_key,
        m.PollStep.message_txt,
        m.PollStep.image,
        m.PollStep.extras,
    ]


class PollResultAdmin(ModelView, model=m.PollResult):
    column_list = [m.PollResult.id]  # type: ignore
    column_filters = [m.PollResult.id, m.PollResult.result_key]
    # column_default_sort = [m.PollResult.result_key]
    column_details_list = [  # type: ignore
        m.PollResult.id,
        m.PollResult.created_at,
        m.PollResult.result_key,
        m.PollResult.message_txt,
        m.PollResult.image,
        m.PollResult.extras,
    ]


admin.add_view(PollStepAdmin)
admin.add_view(PollAdmin)
admin.add_view(PollResultAdmin)
