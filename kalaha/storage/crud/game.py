from kalaha.models.game import LargePit, Player, Pit, GameInfo, MoveLog
from kalaha.storage.crud.base import BaseCrud


class GameCrud(BaseCrud):
    def create_player(self, id: int, name: str) -> Player:
        player = Player(id, name)
        self._storage.append("players", player)
        return player

    def get_player(self, id: int) -> Player:
        return self._storage.get_by_id("players", id)

    def get_players(self) -> list[Player]:
        players = self._storage.get("players")
        return players

    def create_pit(self, id: int, column: int, count: int, player_id: int) -> Pit:
        pit = Pit(id, column, count, player_id)
        self._storage.append("pits", pit)

        return pit

    def get_pit(self, id: int) -> Pit:
        return self._storage.get_by_id("pits", id)

    def get_pits_list(self) -> list[Pit]:
        return self._storage.get("pits")

    def get_pits_by_player(self, player_id: int):
        return [p for p in self._storage.get("pits") if p.player_id == player_id]

    def update_pit(self, id: int, count: int) -> Pit:
        pit = self._storage.get_by_id("pits", id)
        pit.count = count
        return pit

    def create_large_pit(self, id: int, count: int, player_id: int) -> LargePit:
        pit = LargePit(id, 0, player_id)
        self._storage.append("large_pits", pit)

        return pit

    def get_large_pits_list(self) -> list[LargePit]:
        return self._storage.get("large_pits")

    def get_large_pit(self, id: int) -> LargePit:
        return self._storage.get_by_id("large_pits", id)

    def update_large_pit(self, id: int, count: int) -> LargePit:
        pit = self._storage.get_by_id("large_pits", id)
        pit.count = count
        return pit

    def create_game_info(
        self, next_player: int, winner: int | None, draw: bool
    ) -> GameInfo:
        game_info = GameInfo(next_player, winner, draw)
        self._storage.store("game_info", game_info)

        return game_info

    def get_game_info(self) -> GameInfo:
        return self._storage.get("game_info")

    def update_game_info(
        self, next_player_id: int, winner_id: int | None, draw: bool
    ) -> GameInfo:
        game_info = self._storage.get("game_info")
        game_info.next_player_id = next_player_id
        game_info.winner_id = winner_id
        game_info.draw = draw

        return game_info

    def init_move_log(self):
        self._storage.store("move_logs", [])

    def create_move_log(self, player_id: int, pit_id: int) -> MoveLog:
        last_log = self._storage.get_last("move_logs")
        move_log = MoveLog(last_log.id + 1 if last_log else 0, player_id, pit_id)
        self._storage.append("move_logs", move_log)

        return move_log

    def get_move_log_list(self) -> list[MoveLog]:
        return self._storage.get("move_logs")

    def clear(self):
        self._storage.clear()
