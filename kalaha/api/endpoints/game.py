from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from kalaha.api.dependencies import GameService, game_schemas as schema

router = APIRouter(prefix="/game")


@router.get("/board", response_model=schema.Board, status_code=status.HTTP_200_OK)
async def board_state():
    game_service = GameService()

    return game_service.get_board_state()


@router.post("/new_game", response_model=schema.Board, status_code=status.HTTP_200_OK)
async def new_game():
    game_service = GameService()
    game_service.new_game()

    return game_service.get_board_state()


@router.post("/make_move", response_model=schema.Board, status_code=status.HTTP_200_OK)
async def make_move(move_details: schema.MoveDetails):
    game_service = GameService()

    try:
        return game_service.make_move(move_details)
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid input data", "detail": str(exc)},
        )
