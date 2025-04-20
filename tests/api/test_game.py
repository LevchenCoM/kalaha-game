import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


# Scenario: User 1 wins
def test_user1_wins(client):
    response = client.post("/game/new_game")
    assert response.status_code == 200

    moves = [
        0, 5, 6, 1, 9, 0, 7, 3, 9, 4, 10, 2, 7, 4, 0, 8, 1, 8, 0, 7, 4, 2, 6, 7,
        5, 8, 4, 7, 1, 10, 0, 11, 4, 3, 6, 5, 7, 4, 9, 0, 8, 9, 1, 10, 2, 6, 1, 11
    ]

    for api_pit_id in moves:
        response = client.post("/game/make_move", json={"pit_id": api_pit_id})
        assert response.status_code == 200

    response = client.get("/game/board")
    assert response.status_code == 200
    board_state = response.json()

    winner_id = board_state["game_info"]["winner_id"]
    draw = board_state["game_info"]["draw"]

    assert not draw
    assert winner_id == 0


# Scenario: User 2 wins
def test_user2_wins(client):
    response = client.post("/game/new_game")
    assert response.status_code == 200

    moves = [
        0, 4, 9, 2, 10, 2, 9, 4, 3, 7, 5, 8, 3, 2, 9, 1, 7, 2, 10, 0, 11, 8, 1, 9, 4, 9, 3,
        4, 8, 5, 8, 0, 7, 2, 9, 11, 0, 10, 2, 11, 6, 1, 3, 7, 0, 9, 2, 8, 1, 6, 4, 8, 5
    ]

    for api_pit_id in moves:
        response = client.post("/game/make_move", json={"pit_id": api_pit_id})
        assert response.status_code == 200

    response = client.get("/game/board")
    assert response.status_code == 200
    board_state = response.json()

    winner_id = board_state["game_info"]["winner_id"]
    draw = board_state["game_info"]["draw"]

    assert not draw
    assert winner_id == 1


# Scenario: Game over, try move
def test_game_over_try_move(client):
    response = client.post("/game/new_game")
    assert response.status_code == 200

    moves = [
        0, 5, 6, 1, 9, 0, 7, 3, 9, 4, 10, 2, 7, 4, 0, 8, 1, 8 ,0, 7, 4, 2, 6, 7,
        5, 8, 4, 7, 1, 10, 0, 11, 4, 3, 6, 5, 7, 4, 9, 0, 8, 9, 1, 10, 2, 6, 1, 11
    ]

    for api_pit_id in moves:
        response = client.post("/game/make_move", json={"pit_id": api_pit_id})
        assert response.status_code == 200

    response = client.get("/game/board")
    assert response.status_code == 200
    board_state = response.json()

    winner_id = board_state["game_info"]["winner_id"]
    draw = board_state["game_info"]["draw"]

    assert not draw
    assert winner_id == 0

    response = client.post("/game/make_move", json={"pit_id": 3})
    assert response.status_code == 400


# Scenario: Board State after Reset
def test_board_state_after_reset(client):
    response = client.post("/game/new_game")
    assert response.status_code == 200
    board_state = response.json()

    assert len(board_state["players"]) == 2
    assert len(board_state["pits"]) == 12
    assert len(board_state["large_pits"]) == 2
    assert board_state["game_info"]["next_player_id"] == 0
    assert board_state["game_info"]["winner_id"] is None
    assert board_state["game_info"]["draw"] is False


# Scenario: Making Moves and Updating Board State
def test_make_move_updates_board(client):
    response = client.post("/game/new_game")
    assert response.status_code == 200

    response = client.post("/game/make_move", json={"pit_id": 1})
    assert response.status_code == 200
    board_state = response.json()

    assert board_state["large_pits"][0]["count"] > 0

    response = client.post("/game/make_move", json={"pit_id": 7})
    assert response.status_code == 200
    board_state = response.json()

    assert board_state["large_pits"][1]["count"] > 0
