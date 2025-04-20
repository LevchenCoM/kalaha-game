from pydantic import BaseModel


class Player(BaseModel):
    id: int
    name: str


class Pit(BaseModel):
    id: int
    column: int
    count: int
    player_id: int


class LargePit(BaseModel):
    count: int
    player_id: int


class PitNode(BaseModel):
    id: int
    value: Pit


class GameInfo(BaseModel):
    next_player_id: int
    winner_id: int | None
    draw: bool


class MoveLog(BaseModel):
    id: int
    player_id: int
    pit_id: int


class Board(BaseModel):
    players: list[Player]
    pits: list[Pit]
    large_pits: list[LargePit]
    game_info: GameInfo
    move_logs: list[MoveLog]


class MoveDetails(BaseModel):
    pit_id: int
