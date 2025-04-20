import pytest
from kalaha.storage.storage import Storage
from kalaha.models.game import Player
from kalaha.storage.errors import DoesNotExist, NotUnique


@pytest.fixture
def storage():
    storage = Storage()
    storage.clear()
    return storage


def test_store_and_get(storage):
    player = Player(1, "Player 1")
    storage.store("players", [player])
    stored = storage.get("players")
    assert len(stored) == 1
    assert stored[0].id == 1


def test_append_new_item(storage):
    player = Player(1, "Player 1")
    storage.append("players", player)
    stored = storage.get("players")
    assert len(stored) == 1
    assert stored[0].name == "Player 1"


def test_append_duplicate_raises(storage):
    player = Player(1, "Player 1")
    storage.append("players", player)
    with pytest.raises(NotUnique):
        storage.append("players", player)


def test_get_by_id_success(storage):
    player = Player(1, "Player 1")
    storage.append("players", player)
    result = storage.get_by_id("players", 1)
    assert result.name == "Player 1"


def test_get_by_id_not_found_raises(storage):
    with pytest.raises(DoesNotExist):
        storage.get_by_id("players", 99)


def test_get_missing_key_raises(storage):
    with pytest.raises(DoesNotExist):
        storage.get("nonexistent")


def test_clear_storage(storage):
    player = Player(1, "Player 1")
    storage.store("players", [player])
    storage.clear()
    with pytest.raises(DoesNotExist):
        storage.get("players")
