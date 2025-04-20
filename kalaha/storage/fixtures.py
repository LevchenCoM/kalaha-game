import logging
from kalaha.storage.crud.game import GameCrud
from kalaha import config
from kalaha.storage.errors import StorageException


logger = logging.getLogger(__name__)


def initialize_game():
    game_crud = GameCrud()

    try:
        # Init players
        players = [game_crud.create_player(i, f"Player {i + 1}") for i in range(2)]
        player_1, player_2 = players
        # Init pits
        # Player 1
        for x in range(config.PITS_PER_USER):
            game_crud.create_pit(x, x, config.STONES_PER_PIT, player_1.id)

        # Player 2
        for x, y in zip(
            range(
                config.PITS_PER_USER,
                config.PITS_PER_USER * player_2.id + config.PITS_PER_USER,
            ),
            range(config.PITS_PER_USER - 1, -1, -1),
        ):
            game_crud.create_pit(x, y, config.STONES_PER_PIT, player_2.id)

        # Init large pits for each player
        for player in players:
            game_crud.create_large_pit(player.id, 0, player.id)

        # Init move logs
        game_crud.init_move_log()

        # Init game info
        game_crud.create_game_info(player_1.id, None, False)

    except StorageException:
        logger.critical("Failed to apply fixtures.")
        raise RuntimeError("Failed to apply fixtures.")
