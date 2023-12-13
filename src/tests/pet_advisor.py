from unittest.mock import Mock

import pytest
from transitions import EventData

from polls import enums
from polls.pet_advisor import PetAdvisorPoll

pytestmark = pytest.mark.asyncio


@pytest.fixture
def pet_advisor_poll():
    return PetAdvisorPoll("test_user_id")


async def test_set_activity(pet_advisor_poll):
    mock_event_data = Mock(spec=EventData)
    mock_event_data.kwargs = {"activity": enums.ActivityEnum.CALM}
    pet_advisor_poll.set_activity(mock_event_data)
    assert pet_advisor_poll.activity == enums.ActivityEnum.CALM

    # test for wrong input
    mock_event_data.kwargs = {"activity": "wrong"}
    with pytest.raises(Exception):
        pet_advisor_poll.set_activity(mock_event_data)


async def test_set_hair(pet_advisor_poll):
    mock_event_data = Mock(spec=EventData)
    mock_event_data.kwargs = {"hairyness": enums.HairynessEnum.HAIRY}
    pet_advisor_poll.set_hair(mock_event_data)
    assert pet_advisor_poll.hairyness == enums.HairynessEnum.HAIRY

    # test for wrong input
    mock_event_data.kwargs = {"hairyness": "wrong"}
    with pytest.raises(Exception):
        pet_advisor_poll.set_hair(mock_event_data)


async def test_set_hair_length(pet_advisor_poll):
    mock_event_data = Mock(spec=EventData)
    mock_event_data.kwargs = {"hair_length": enums.HairLengthEnum.LONG}
    pet_advisor_poll.set_hair_length(mock_event_data)
    assert pet_advisor_poll.hair_length == enums.HairLengthEnum.LONG

    # test for wrong input
    mock_event_data.kwargs = {"hair_length": "wrong"}
    with pytest.raises(Exception):
        pet_advisor_poll.set_hair_length(mock_event_data)


async def test_set_hairyness(pet_advisor_poll):
    mock_event_data = Mock(spec=EventData)
    mock_event_data.kwargs = {"hairyness": enums.HairynessEnum.HAIRY}
    pet_advisor_poll.set_hairyness(mock_event_data)
    assert pet_advisor_poll.hairyness == enums.HairynessEnum.HAIRY

    # test for wrong input
    mock_event_data.kwargs = {"hairyness": "wrong"}
    with pytest.raises(Exception):
        pet_advisor_poll.set_hairyness(mock_event_data)


async def test_set_size(pet_advisor_poll):
    mock_event_data = Mock(spec=EventData)
    mock_event_data.kwargs = {"size": enums.SizeEnum.SMALL}
    pet_advisor_poll.set_size(mock_event_data)
    assert pet_advisor_poll.size == enums.SizeEnum.SMALL

    # test for wrong input
    mock_event_data.kwargs = {"size": "wrong"}
    with pytest.raises(Exception):
        pet_advisor_poll.set_size(mock_event_data)


async def test_set_independance(pet_advisor_poll):
    mock_event_data = Mock(spec=EventData)
    mock_event_data.kwargs = {"independance": enums.IndependanceEnum.INDEPENDANT}
    pet_advisor_poll.set_independance(mock_event_data)
    assert pet_advisor_poll.independance == enums.IndependanceEnum.INDEPENDANT

    # test for wrong input
    mock_event_data.kwargs = {"independance": "wrong"}
    with pytest.raises(Exception):
        pet_advisor_poll.set_independance(mock_event_data)


async def test_get_result_key(pet_advisor_poll):
    mock_event_data = Mock(spec=EventData)
    mock_event_data.kwargs = {"independance": enums.IndependanceEnum.INDEPENDANT}
    pet_advisor_poll.set_independance(mock_event_data)
    pet_advisor_poll.species = enums.SpeciesEnum.CAT
    pet_advisor_poll.activity = enums.ActivityEnum.CALM
    pet_advisor_poll.independance = enums.IndependanceEnum.INDEPENDANT
    pet_advisor_poll.hair_length = enums.HairLengthEnum.SHORT
    assert pet_advisor_poll.get_result_key() == "cat_calm_independant_short"


async def test_is_cat(pet_advisor_poll):
    pet_advisor_poll.species = enums.SpeciesEnum.CAT
    assert pet_advisor_poll.is_cat() == True


async def test_is_dog(pet_advisor_poll):
    pet_advisor_poll.species = enums.SpeciesEnum.DOG
    assert pet_advisor_poll.is_dog() == True


async def test_dog_flow(pet_advisor_poll):
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.GREETING

    await pet_advisor_poll.next()
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.CAT_OR_DOG
    await pet_advisor_poll.next(species=enums.SpeciesEnum.DOG)
    assert pet_advisor_poll.is_dog()
    assert not pet_advisor_poll.is_cat()
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.CALM_OR_ACTIVE
    await pet_advisor_poll.next(activity=enums.ActivityEnum.ACTIVE)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.SMALL_OR_LARGE
    await pet_advisor_poll.next(size=enums.SizeEnum.LARGE)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.SHORT_OR_LONG_HAIR
    await pet_advisor_poll.next(hair_length=enums.HairLengthEnum.LONG)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.RESULT
    assert pet_advisor_poll.get_result() == "dog_active_large_long"


async def test_cat_flow(pet_advisor_poll):
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.GREETING

    await pet_advisor_poll.next()
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.CAT_OR_DOG
    await pet_advisor_poll.next(species=enums.SpeciesEnum.CAT)
    assert not pet_advisor_poll.is_dog()
    assert pet_advisor_poll.is_cat()
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.CALM_OR_ACTIVE
    await pet_advisor_poll.next(activity=enums.ActivityEnum.ACTIVE)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.INDEPENDENT_OR_NOT
    await pet_advisor_poll.next(size=enums.IndependanceEnum.INDEPENDANT)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.HAIRY_OR_NOT
    await pet_advisor_poll.next(hair_length=enums.HairynessEnum.HAIRY)
    assert pet_advisor_poll.state == enums.PetAdvisorStatesEnum.RESULT
    assert pet_advisor_poll.get_result() == "cat_active_independant_hairy"
