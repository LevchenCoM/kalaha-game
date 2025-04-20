import pytest

from kalaha.storage import Storage
from kalaha.storage.crud.game import GameCrud
from kalaha.storage.errors import DoesNotExist


@pytest.fixture
def storage():
    storage = Storage()
    storage.clear()
    return storage


@pytest.fixture
def game_crud(storage):
    return GameCrud()


def test_create_player(game_crud):
    player = game_crud.create_player(1, "Player 1")
    assert player.id == 1
    assert player.name == "Player 1"


def test_get_player(game_crud):
    game_crud.create_player(1, "Player 1")
    player = game_crud.get_player(1)
    assert player.id == 1
    assert player.name == "Player 1"


def test_get_player_not_found(game_crud):
    with pytest.raises(DoesNotExist):
        game_crud.get_player(99)


def test_create_pit(game_crud):
    player = game_crud.create_player(1, "Player 1")
    pit = game_crud.create_pit(1, 0, 4, player.id)
    assert pit.id == 1
    assert pit.column == 0
    assert pit.count == 4
    assert pit.player_id == 1


def test_get_pit(game_crud):
    player = game_crud.create_player(1, "Player 1")
    game_crud.create_pit(1, 0, 4, player.id)
    pit = game_crud.get_pit(1)
    assert pit.id == 1
    assert pit.column == 0
    assert pit.count == 4
    assert pit.player_id == 1


def test_get_pit_not_found(game_crud):
    with pytest.raises(DoesNotExist):
        game_crud.get_pit(99)


def test_create_large_pit(game_crud):
    player = game_crud.create_player(1, "Player 1")
    large_pit = game_crud.create_large_pit(1, 0, player.id)
    assert large_pit.id == 1
    assert large_pit.count == 0
    assert large_pit.player_id == 1


def test_get_large_pit(game_crud):
    player = game_crud.create_player(1, "Player 1")
    game_crud.create_large_pit(1, 0, player.id)
    large_pit = game_crud.get_large_pit(1)
    assert large_pit.id == 1
    assert large_pit.count == 0
    assert large_pit.player_id == 1


def test_create_game_info(game_crud):
    game_info = game_crud.create_game_info(1, None, False)
    assert game_info.next_player_id == 1
    assert game_info.winner_id is None
    assert game_info.draw is False


def test_get_game_info(game_crud):
    game_crud.create_game_info(1, None, False)
    game_info = game_crud.get_game_info()
    assert game_info.next_player_id == 1
    assert game_info.winner_id is None
    assert game_info.draw is False


def test_update_game_info(game_crud):
    game_crud.create_game_info(1, None, False)
    game_info = game_crud.update_game_info(2, 1, True)
    assert game_info.next_player_id == 2
    assert game_info.winner_id == 1
    assert game_info.draw is True


def test_create_multiple_players(game_crud):
    player1 = game_crud.create_player(1, "Player 1")
    player2 = game_crud.create_player(2, "Bob")
    assert len(game_crud.get_players()) == 2
    assert player1.name == "Player 1"
    assert player2.name == "Bob"


def test_clear_game_crud(game_crud):
    game_crud.create_player(1, "Player 1")
    game_crud.create_pit(1, 0, 4, 1)
    game_crud.clear()
    with pytest.raises(DoesNotExist):
        game_crud.get_player(1)
    with pytest.raises(DoesNotExist):
        game_crud.get_pit(1)
