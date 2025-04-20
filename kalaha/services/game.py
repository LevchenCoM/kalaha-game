from kalaha.services.base import BaseService
from kalaha.storage.crud.game import GameCrud
from kalaha.models.schemas.game import (
    Board,
    Pit,
    LargePit,
    Player,
    MoveDetails,
    GameInfo,
    MoveLog,
)
from kalaha.models.game import (
    Pit as InMemoryPit,
    Player as InMemoryPlayer,
    LargePit as InmMemoryLargePit,
)
from kalaha.utils.iterators import PitsList, PitsListIterator, PitNode
from kalaha.storage.fixtures import initialize_game


class GameService(BaseService[GameCrud]):
    CRUD_CLASS = GameCrud

    def get_board_state(self) -> Board:
        players = self._crud.get_players()
        pits = self._crud.get_pits_list()
        large_pits = self._crud.get_large_pits_list()
        game_info = self._crud.get_game_info()
        move_logs = self._crud.get_move_log_list()

        return Board(
            pits=[
                Pit(id=p.id, column=p.column, count=p.count, player_id=p.player_id)
                for p in pits
            ],
            players=[Player(id=player.id, name=player.name) for player in players],
            large_pits=[
                LargePit(count=p.count, player_id=p.player_id) for p in large_pits
            ],
            game_info=GameInfo(
                next_player_id=game_info.next_player_id,
                winner_id=game_info.winner_id,
                draw=game_info.draw,
            ),
            move_logs=[
                MoveLog(id=m.id, player_id=m.player_id, pit_id=m.pit_id)
                for m in move_logs
            ],
        )

    def _move_stones(
        self,
        pits_list: PitsList,
        start_node: PitNode,
        player: InMemoryPlayer,
        large_pit: InmMemoryLargePit,
    ) -> tuple[bool, int]:
        one_more_move = False

        stones_left = start_node.count
        start_node.count = 0

        large_pit_count = large_pit.count
        prev_node_player = start_node.value.player_id

        for node in PitsListIterator(start_node.next, max_steps=stones_left):
            if not stones_left:
                break

            is_last_step = stones_left == 1
            is_large_pit_step = all(
                (
                    prev_node_player != node.value.player_id,
                    node.value.player_id != player.id,
                )
            )

            if is_large_pit_step:
                large_pit_count += 1
                stones_left -= 1

                if is_last_step:
                    one_more_move = True
                    break

                is_last_step = stones_left == 1

            if is_last_step:
                if node.count == 0 and node.value.player_id == player.id:
                    # Take all from opposite pit and put to large pit of the user
                    opposite_node = pits_list.get_opposite_node(node)
                    large_pit_count += 1 + opposite_node.count
                    opposite_node.count = 0
                else:
                    node.count += 1
            else:
                node.count += 1

            stones_left -= 1
            prev_node_player = node.value.player_id

        return one_more_move, large_pit_count

    def _save_move_results(
        self,
        pits: list[InMemoryPit],
        pits_list: PitsList,
        player: InMemoryPlayer,
        large_pit_count: int,
    ):
        for pit in pits:
            node = pits_list.get_node_by_id(pit.id)
            self._crud.update_pit(pit.id, node.count)

        self._crud.update_large_pit(player.id, large_pit_count)

    def _calculate_game_results(self) -> tuple[int | None, bool]:
        winner = None
        draw = False

        players = self._crud.get_players()
        counts = []
        for player in players:
            pits = self._crud.get_pits_by_player(player.id)
            count = sum([p.count for p in pits])
            counts.append(count)

        if any([count == 0 for count in counts]):
            large_pits = self._crud.get_large_pits_list()

            # Put all stones that left on the board to player's large pit
            for large_pit in large_pits:
                updated_count = large_pit.count
                player_pits = self._crud.get_pits_by_player(large_pit.player_id)
                updated_count += sum([p.count for p in player_pits])
                self._crud.update_large_pit(large_pit.id, updated_count)

            player_1_score, player_2_score = self._crud.get_large_pits_list()
            if player_1_score == player_2_score:
                draw = True
            else:
                winner = sorted(large_pits, key=lambda x: x.count)[1].player_id

        return winner, draw

    def make_move(self, move_details: MoveDetails) -> Board:
        game_info = self._crud.get_game_info()
        if game_info.draw or game_info.winner_id is not None:
            raise ValueError("Game is over. Start new game.")

        player = self._crud.get_player(game_info.next_player_id)
        pit = self._crud.get_pit(move_details.pit_id)
        large_pit = self._crud.get_large_pit(player.id)

        if player.id != pit.player_id:
            raise ValueError("Incorrect pit selected.")

        pits = self._crud.get_pits_list()
        pits_list = PitsList(pits=pits)
        start_node = pits_list.get_node_by_id(pit.id)

        one_more_move, large_pit_count = self._move_stones(
            pits_list, start_node, player, large_pit
        )
        self._save_move_results(pits, pits_list, player, large_pit_count)

        next_player = player.id if one_more_move else int(not bool(player.id))
        winner, draw = self._calculate_game_results()
        self._crud.update_game_info(next_player, winner, draw)

        self._crud.create_move_log(player.id, pit.id)
        return self.get_board_state()

    def new_game(self) -> Board:
        self._crud.clear()
        initialize_game()

        return self.get_board_state()
