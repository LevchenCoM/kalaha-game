from abc import ABC

from kalaha.storage.base import BaseStorageModel


class AbstractPit(ABC):
    def __init__(self, id: int, count: int, player_id: int):
        self.id = id
        self.count = count
        self.player_id = player_id

    def add_stones(self, count: int):
        self.count += count


class Pit(AbstractPit, BaseStorageModel):
    def __init__(self, id: int, column: int, count: int, player_id: int):
        super().__init__(id, count, player_id)
        self.column = column

    def __repr__(self) -> str:
        return f"Pit(id={self.id}, column={self.column}, count={self.count}, player_id={self.player_id})"


class LargePit(AbstractPit, BaseStorageModel):
    def __init__(self, id: int, count: int, player_id: int):
        super().__init__(id, count, player_id)
        self.count = count

    def __repr__(self) -> str:
        return f"LargePit(id={self.id}, count={self.count}, player_id={self.player_id})"


class Player(BaseStorageModel):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f"Player(id={self.id}, name={self.name})"


class GameInfo(BaseStorageModel):
    def __init__(self, next_player_id: int, winner_id: int | None, draw: bool):
        self.next_player_id = next_player_id
        self.winner_id = winner_id
        self.draw = draw

    def __repr__(self) -> str:
        return f"GameInfo(next_player_id={self.next_player_id}, winner_id={self.winner_id}, draw={self.draw})"


class MoveLog(BaseStorageModel):
    def __init__(self, id: int, player_id: int, pit_id: int):
        self.id = id
        self.player_id = player_id
        self.pit_id = pit_id

    def __repr__(self) -> str:
        return (
            f"MoveLog(id={self.id}, player_id={self.player_id}, pit_id={self.pit_id})"
        )
