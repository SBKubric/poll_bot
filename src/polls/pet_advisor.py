from transitions.extensions.asyncio import AsyncMachine

from polls import enums


class PetAdvisorPoll(AsyncMachine):
    def __init__(self):
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
                {"source": "greeting", "dest": "cat_or_dog", "trigger": "begin"},
                {
                    "source": "cat_or_dog",
                    "dest": "calm_or_active",
                    "trigger": "set_species",
                },
                {
                    "source": "calm_or_active",
                    "dest": "short_or_long_hair",
                    "trigger": "set_activity",
                },
                {
                    "source": "calm_or_active",
                    "dest": "hairy_or_not",
                    "trigger": "set_activity",
                },
                {
                    "source": "short_or_long_hair",
                    "dest": "result",
                    "trigger": "set_hair",
                },
                {"source": "hairy_or_not", "dest": "result", "trigger": "set_hair"},
            ],
            send_event=True,
            initial="greeting",
        )
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

    async def begin(self, event):
        ...

    async def set_species(self, event):
        ...

    async def set_activity(self, event):
        ...

    async def set_hair(self, event):
        if self.species == enums.SpeciesEnum.CAT:
            await self.set_hairyness(event)
            return

        if self.species == enums.SpeciesEnum.DOG:
            await self.set_hair_length(event)
            return

        raise Exception("Invalid species")

    async def set_hair_length(self, event):
        ...

    async def set_hairyness(self, event):
        ...

    async def get_result(self):
        if self.state != "result":
            raise Exception("Not in result state")
        ...
