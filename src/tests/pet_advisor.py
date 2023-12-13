from unittest.mock import Mock

import pytest
from transitions import EventData

from polls import enums
from polls.pet_advisor import PetAdvisorPoll


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
    pet_advisor_poll.hair_length = enums.HairLengthEnum.SHORT
    assert pet_advisor_poll.get_result_key() == "CAT_CALM_SHORT"


async def test_is_cat(pet_advisor_poll):
    pet_advisor_poll.species = enums.SpeciesEnum.CAT
    assert pet_advisor_poll.is_cat() == True


async def test_is_dog(pet_advisor_poll):
    pet_advisor_poll.species = enums.SpeciesEnum.DOG
    assert pet_advisor_poll.is_dog() == True


async def test_get_dialog_step(pet_advisor_poll):
    with pytest.raises(NotImplementedError):
        pet_advisor_poll.get_dialog_step()


async def test_get_result(pet_advisor_poll):
    with pytest.raises(Exception):
        pet_advisor_poll.get_result()


async def test_persist(pet_advisor_poll):
    with pytest.raises(NotImplementedError):
        pet_advisor_poll.persist()
