import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from kalaha.api.endpoints.game import router as game_router
from kalaha.api import expection_handlers
from kalaha.storage.fixtures import initialize_game
from kalaha.storage import Storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init in memory storage and generate an initial data
    initialize_game()
    yield

    # Drop storage
    del Storage.instance


app = FastAPI(lifespan=lifespan)
app.include_router(game_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

expection_handlers.setup_exception_handlers(app)


# UI HTML
@app.get("/")
def read_root():
    return FileResponse("static/index.html")
