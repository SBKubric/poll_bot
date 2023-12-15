import asyncio

import pytest

from polls import enums
from polls.pet_advisor import PetAdvisorPoll

pytestmark = pytest.mark.asyncio(scope="module")


@pytest.fixture
def pet_advisor_poll():
    poll = PetAdvisorPoll("test_user_id", "test_chat_id")
    return poll


async def test_get_result_key(pet_advisor_poll):
    pet_advisor_poll.species = enums.SpeciesEnum.CAT
    pet_advisor_poll.activity = enums.ActivityEnum.CALM
    pet_advisor_poll.independence = enums.IndependenceEnum.INDEPENDENT
    pet_advisor_poll.hairyness = enums.HairynessEnum.HAIRY
    assert pet_advisor_poll.get_result_key() == "pet_advisor_cat_calm_independent_hairy"


async def test_is_cat(pet_advisor_poll):
    pet_advisor_poll.species = enums.SpeciesEnum.CAT
    assert pet_advisor_poll.is_cat() == True


async def test_is_dog(pet_advisor_poll):
    pet_advisor_poll.species = enums.SpeciesEnum.DOG
    assert pet_advisor_poll.is_dog() == True


async def test_dog_flow(pet_advisor_poll):
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.GREETING
    await pet_advisor_poll.next(persist=False)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.CAT_OR_DOG
    await pet_advisor_poll.next(user_input=enums.SpeciesEnum.DOG, persist=False)
    assert pet_advisor_poll.is_dog()
    assert not pet_advisor_poll.is_cat()
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.CALM_OR_ACTIVE
    await pet_advisor_poll.next(user_input=enums.ActivityEnum.ACTIVE, persist=False)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.SMALL_OR_LARGE
    await pet_advisor_poll.next(user_input=enums.SizeEnum.LARGE, persist=False)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.SHORT_OR_LONG_HAIR
    await pet_advisor_poll.next(user_input=enums.HairLengthEnum.LONG, persist=False)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.RESULT
    assert pet_advisor_poll.get_result_key() == "pet_advisor_dog_active_large_long"


async def test_cat_flow(pet_advisor_poll):
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.GREETING

    await pet_advisor_poll.next(persist=False)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.CAT_OR_DOG
    await pet_advisor_poll.next(user_input=enums.SpeciesEnum.CAT, persist=False)
    assert not pet_advisor_poll.is_dog()
    assert pet_advisor_poll.is_cat()
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.CALM_OR_ACTIVE
    await pet_advisor_poll.next(user_input=enums.ActivityEnum.ACTIVE, persist=False)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.INDEPENDENT_OR_NOT
    await pet_advisor_poll.next(
        user_input=enums.IndependenceEnum.INDEPENDENT, persist=False
    )
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.HAIRY_OR_NOT
    await pet_advisor_poll.next(user_input=enums.HairynessEnum.HAIRY, persist=False)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.RESULT
    assert (
        pet_advisor_poll.get_result_key() == "pet_advisor_cat_active_independent_hairy"
    )
