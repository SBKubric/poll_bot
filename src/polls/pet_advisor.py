import logging
import pickle
import typing as t

from transitions import EventData
from transitions.extensions.asyncio import AsyncMachine

from db import managers
from polls import enums, models


class PetAdvisorPoll(AsyncMachine):
    def __init__(self, user_id: str, chat_id: str):
        super().__init__(
            model=self,
            states=[
                {"name": enums.PetAdvisorStatesEnum.GREETING, "on_exit": "greet"},
                {
                    "name": enums.PetAdvisorStatesEnum.CAT_OR_DOG,
                    "on_exit": "set_species",
                },
                {
                    "name": enums.PetAdvisorStatesEnum.CALM_OR_ACTIVE,
                    "on_exit": "set_activity",
                },
                {
                    "name": enums.PetAdvisorStatesEnum.SMALL_OR_LARGE,
                    "on_exit": "set_size",
                },
                {
                    "name": enums.PetAdvisorStatesEnum.INDEPENDENT_OR_NOT,
                    "on_exit": "set_independence",
                },
                {
                    "name": enums.PetAdvisorStatesEnum.SHORT_OR_LONG_HAIR,
                    "on_exit": "set_hair_length",
                },
                {
                    "name": enums.PetAdvisorStatesEnum.HAIRY_OR_NOT,
                    "on_exit": "set_hairyness",
                },
                enums.PetAdvisorStatesEnum.RESULT,
            ],
            transitions=[
                {
                    "source": enums.PetAdvisorStatesEnum.GREETING,
                    "dest": enums.PetAdvisorStatesEnum.CAT_OR_DOG,
                    "trigger": "next",
                },
                {
                    "source": enums.PetAdvisorStatesEnum.CAT_OR_DOG,
                    "dest": enums.PetAdvisorStatesEnum.CALM_OR_ACTIVE,
                    "conditions": ["is_greeted"],
                    "trigger": "next",
                },
                {
                    "source": enums.PetAdvisorStatesEnum.CALM_OR_ACTIVE,
                    "dest": enums.PetAdvisorStatesEnum.SMALL_OR_LARGE,
                    "conditions": ["is_dog"],
                    "trigger": "next",
                },
                {
                    "source": enums.PetAdvisorStatesEnum.CALM_OR_ACTIVE,
                    "dest": enums.PetAdvisorStatesEnum.INDEPENDENT_OR_NOT,
                    "conditions": ["is_cat"],
                    "after": "persist",
                    "trigger": "next",
                },
                {
                    "source": enums.PetAdvisorStatesEnum.SMALL_OR_LARGE,
                    "dest": enums.PetAdvisorStatesEnum.SHORT_OR_LONG_HAIR,
                    "conditions": ["is_activity_set"],
                    "trigger": "next",
                },
                {
                    "source": enums.PetAdvisorStatesEnum.INDEPENDENT_OR_NOT,
                    "dest": enums.PetAdvisorStatesEnum.HAIRY_OR_NOT,
                    "conditions": ["is_activity_set"],
                    "after": "persist",
                    "trigger": "next",
                },
                {
                    "source": enums.PetAdvisorStatesEnum.SHORT_OR_LONG_HAIR,
                    "dest": enums.PetAdvisorStatesEnum.RESULT,
                    "conditions": ["is_size_set"],
                    "trigger": "next",
                },
                {
                    "source": enums.PetAdvisorStatesEnum.HAIRY_OR_NOT,
                    "dest": enums.PetAdvisorStatesEnum.RESULT,
                    "conditions": ["is_independence_set"],
                    "trigger": "next",
                },
            ],
            send_event=True,
            initial=enums.PetAdvisorStatesEnum.GREETING,
            finalize_event="persist",
            on_exception="log_error",
        )
        self.poll_id = 0
        self.user_id = user_id
        self.chat_id = chat_id
        self.greeted: bool = False
        self.species: enums.SpeciesEnum = enums.SpeciesEnum.NOT_SET
        self.activity: enums.ActivityEnum = enums.ActivityEnum.NOT_SET
        self.size: enums.SizeEnum = enums.SizeEnum.NOT_SET
        self.independence: enums.IndependenceEnum = enums.IndependenceEnum.NOT_SET
        self.hair_length: enums.HairLengthEnum = enums.HairLengthEnum.NOT_SET
        self.hairyness: enums.HairynessEnum = enums.HairynessEnum.NOT_SET
        self._results = []
        logging.debug("Initialized PetAdvisorPoll")

    def get_result_key(self) -> str:
        if self.species == enums.SpeciesEnum.CAT:
            return f"pet_advisor_{self.species.value}_{self.activity.value}_{self.independence.value}_{self.hairyness.value}"
        if self.species == enums.SpeciesEnum.DOG:
            return f"pet_advisor_{self.species.value}_{self.activity.value}_{self.size.value}_{self.hair_length.value}"

        raise Exception("Invalid species")

    def is_cat(self, _: EventData | None = None) -> bool:
        logging.debug("is_cat: %s", self.species == enums.SpeciesEnum.CAT)
        return self.species == enums.SpeciesEnum.CAT

    def is_dog(self, _: EventData | None = None) -> bool:
        logging.debug("is_dog: %s", self.species == enums.SpeciesEnum.DOG)
        return self.species == enums.SpeciesEnum.DOG

    def is_species_set(self, _: EventData | None = None) -> bool:
        return self.species != enums.SpeciesEnum.NOT_SET

    def is_activity_set(self, _: EventData | None = None) -> bool:
        return self.activity != enums.ActivityEnum.NOT_SET

    def is_independence_set(self, _: EventData | None = None) -> bool:
        return self.independence != enums.IndependenceEnum.NOT_SET

    def is_hair_length_set(self, _: EventData | None = None) -> bool:
        return self.hair_length != enums.HairLengthEnum.NOT_SET

    def is_hairyness_set(self, _: EventData | None = None) -> bool:
        return self.hairyness != enums.HairynessEnum.NOT_SET

    def is_size_set(self, _: EventData | None = None) -> bool:
        return self.size != enums.SizeEnum.NOT_SET

    async def greet(self, event: EventData):
        self.greeted = True

    def is_greeted(self, _: EventData | None = None) -> bool:
        return self.greeted

    async def set_species(self, event: EventData):
        species = event.kwargs.get("user_input")
        if not species or not enums.SpeciesEnum.has_value(species):
            logging.debug(f"Invalid species: {species}")
            raise Exception("Invalid species")
        self.species = t.cast(enums.SpeciesEnum, enums.SpeciesEnum.get_member(species))

    async def set_activity(self, event: EventData):
        activity = event.kwargs.get("user_input")
        if not activity or not enums.ActivityEnum.has_value(activity):
            logging.debug(f"Invalid activity: {activity}")
            raise Exception("Invalid activity")
        self.activity = t.cast(
            enums.ActivityEnum, enums.ActivityEnum.get_member(activity)
        )

    async def set_hair_length(self, event: EventData):
        length = event.kwargs.get("user_input")
        if not length or not enums.HairLengthEnum.has_value(length):
            logging.debug(f"Invalid hair length: {length}")
            raise Exception("Invalid hair length")
        self.hair_length = t.cast(
            enums.HairLengthEnum, enums.HairLengthEnum.get_member(length)
        )

    async def set_hairyness(self, event: EventData):
        hairyness = event.kwargs.get("user_input")
        if not hairyness or not enums.HairynessEnum.has_value(hairyness):
            logging.debug(f"Invalid hairyness: {hairyness}")
            raise Exception("Invalid hairyness")
        self.hairyness = t.cast(
            enums.HairynessEnum, enums.HairynessEnum.get_member(hairyness)
        )

    async def set_size(self, event: EventData):
        size = event.kwargs.get("user_input")
        if not size or not enums.SizeEnum.has_value(size):
            logging.debug(f"Invalid size: {size}")
            raise Exception("Invalid size")
        self.size = t.cast(enums.SizeEnum, enums.SizeEnum.get_member(size))

    async def set_independence(self, event: EventData):
        independence = event.kwargs.get("user_input")
        if not independence or not enums.IndependenceEnum.has_value(independence):
            logging.debug(f"Invalid independence: {independence}")
            raise Exception("Invalid independence")
        self.independence = t.cast(
            enums.IndependenceEnum, enums.IndependenceEnum.get_member(independence)
        )

    async def get_dialog_step(self) -> models.Message:
        steps = await managers.get_poll_steps()
        step = steps.get(f"pet_advisor_{self.state.value}")
        if not step:
            logging.debug(f"Invalid state: {self.state}, steps: {steps}, step: {step}")
            raise Exception("Invalid state")
        image_path = str(step.image) if step.image is not None else ""
        return models.Message(
            message_txt=step.message_txt, image_path=image_path, extras=step.extras  # type: ignore
        )

    async def get_results(self) -> list[models.Message]:
        if self.state != "result":
            raise Exception("Not in result state")
        if self._results:
            return self._results

        result_key = self.get_result_key()
        results = await managers.get_poll_results()
        self_results = results.get(result_key, [])
        if not self_results:
            raise Exception("No results found")
        logging.debug("Found results: %s", self_results)
        self._results = [
            models.Message(
                message_txt=x.message_txt,  # type: ignore
                image_path=str((lambda f: f if f is not None else "")(x.image)),  # type: ignore
                extras=x.extras,  # type: ignore
            )
            for x in self_results
        ]
        await managers.terminate_poll(self.poll_id)
        return self._results

    async def persist(self, event: EventData):
        persist = event.kwargs.get("persist", True)
        if not persist:
            logging.debug("Not persisting")
            return
        if not self.poll_id:
            self.poll_id = await managers.create_poll(self.user_id, self.chat_id)
        pickled = pickle.dumps(self)
        await managers.persist_poll(self.poll_id, pickled)

    async def log_error(self, event: EventData):
        logging.error(event.error)
