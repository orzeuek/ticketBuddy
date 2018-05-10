from src.state import StateRepository
from unittest import mock
import json


@mock.patch('random.randint', return_value=12345)
def test_get_state_with_empty_session_id(randint):
    repo = StateRepository(get_storage_mock())
    state = repo.get_state("", None)
    assert state["session_id"] == 12345


def test_get_state_with_not_empty_non_existing_session_id():
    repo = StateRepository(get_storage_mock())
    state = repo.get_state("", "1234")
    assert state["session_id"] == "1234"


def test_get_state_with_existing_session_id():
    storage = {"1234": json.dumps({"a": "b", "c": "d", "session_id": "1234"})}
    repo = StateRepository(get_storage_mock(storage))
    state = repo.get_state("abcd", "1234")

    expected_state = json.loads(storage["1234"])
    expected_state["text"] = "abcd"
    assert state == expected_state
    assert state['session_id'] == "1234"


def get_storage_mock(storage_state={}):
    storage = mock.MagicMock()
    storage.get = lambda id: bytes(storage_state[id], 'utf-8')
    storage.has = lambda id: id in storage_state
    storage.set = mock.MagicMock(side_effect=storage_state.setdefault)
    return storage
