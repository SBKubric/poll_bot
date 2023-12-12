import typing as t

from transitions import EventData
from transitions.extensions.asyncio import AsyncMachine

from polls import enums, models


class PetAdvisorPoll(AsyncMachine):
    def __init__(self, user_id: str):
        super().__init__(
            model=self,
            states=[
                "greeting",
                "cat_or_dog",
                "calm_or_active",
                "short_or_long_hair",
                "hairy_or_not",
                "result",
            ],
            transitions=[
                {"source": "greeting", "dest": "cat_or_dog", "trigger": "next"},
                {
                    "source": "cat_or_dog",
                    "dest": "calm_or_active",
                    "before": "set_species",
                    "trigger": "next",
                },
                {
                    "source": "calm_or_active",
                    "dest": "short_or_long_hair",
                    "before": "set_activity",
                    "trigger": "next",
                },
                {
                    "source": "calm_or_active",
                    "dest": "hairy_or_not",
                    "before": "set_activity",
                    "trigger": "next",
                },
                {
                    "source": "short_or_long_hair",
                    "dest": "result",
                    "before": "set_hair",
                    "trigger": "next",
                },
                {
                    "source": "hairy_or_not",
                    "dest": "result",
                    "before": "set_hair",
                    "trigger": "next",
                },
            ],
            send_event=True,
            initial="greeting",
        )
        self.user_id = user_id
        self.species: enums.SpeciesEnum = enums.SpeciesEnum.NOT_SET
        self.activity: enums.ActivityEnum = enums.ActivityEnum.NOT_SET
        self.hair_length: enums.HairLengthEnum = enums.HairLengthEnum.NOT_SET
        self.hairyness: enums.HairynessEnum = enums.HairynessEnum.NOT_SET

    def get_result_key(self) -> str:
        if self.species == enums.SpeciesEnum.CAT:
            return (
                f"{self.species.value}_{self.activity.value}_{self.hair_length.value}"
            )
        if self.species == enums.SpeciesEnum.DOG:
            return f"{self.species.value}_{self.activity.value}_{self.hairyness.value}"

        raise Exception("Invalid species")

    async def set_species(self, event: EventData):
        species = event.kwargs.get("species")
        if not species:
            raise Exception("Invalid species")
        self.species = t.cast(enums.SpeciesEnum, species)

    async def set_activity(self, event: EventData):
        activity = event.kwargs.get("activity")
        if not activity:
            raise Exception("Invalid activity")
        self.activity = t.cast(enums.ActivityEnum, activity)

    async def set_hair(self, event: EventData):
        if self.species == enums.SpeciesEnum.CAT:
            await self.set_hairyness(event)
            return

        if self.species == enums.SpeciesEnum.DOG:
            await self.set_hair_length(event)
            return

        raise Exception("Invalid species")

    async def set_hair_length(self, event: EventData):
        length = event.kwargs.get("hair_length")
        if not length:
            raise Exception("Invalid hair length")
        self.hair_length = t.cast(enums.HairLengthEnum, length)

    async def set_hairyness(self, event: EventData):
        hairyness = event.kwargs.get("hairyness")
        if not hairyness:
            raise Exception("Invalid hairyness")
        self.hairyness = t.cast(enums.HairynessEnum, hairyness)

    async def get_dialog_step(self) -> models.PollDialogStep:
        ...

    async def get_result(self) -> models.PollResult:
        if self.state != "result":
            raise Exception("Not in result state")
        ...
