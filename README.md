# Kalaha Game

## Tech Stack
It's browser based web application with simple UI.

### Backend:
- python3 (3.13)
- pip or uv (package manager)
- fastapi (framework)

### Frontend:- Static HTML file hosted on the backend, running in the browser.


## Launch Instructions
- The app runs on port 8000.
- UI is available at http://localhost:8000
- API Docs and a sandbox: http://localhost:8000/docs


### Docker (recommended)
```shell
# Step 1: Build an image
docker build -t kalaha-app .
# Step 2: Run the app
docker run -p 8000:8000 kalaha-app
```

### On Local Machine
#### Prerequisites
- python 3.13
- pip or uv
- virtualenv

#### Using pip
```shell
# Step 1: Create virtualenv
python3.13 -m venv .venv
# Step 2: Activate virtualenv
source .venv/bin/activate
# Step 3: Install requirements
pip install -r requirements.txt
# Step 4: Run  the app
fastapi run main.py
```

#### Using uv
```shell
# Step 1: Sync dependencies (automatically creates a virtualenv)
uv sync
# Step 2: Run  the app
uv run fastapi run main.py
```



### Game Rules
#### Board Setup
Each of the two players has his six pits in front of him. To the right of the six pits,
each player has a larger pit. At the start of the game, there are six stones in each
of the six round pits .

#### Game Play
The player who begins with the first move picks up all the stones in any of his own
six pits, and sows the stones on to the right, one in each of the following pits,
including his own big pit. No stones are put in the opponents' big pit. If the player's
last stone lands in his own big pit, he gets another turn. This can be repeated
several times before it's the other player's turn.

#### Capturing Stones
During the game the pits are emptied on both sides. Always when the last stone
lands in an own empty pit, the player captures his own stone and all stones in the
opposite pit (the other player’s pit) and puts them in his own (big or little?) pit.

#### The Game Ends
The game is over as soon as one of the sides runs out of stones. The player who
still has stones in his pits keeps them and puts them in his big pit. The winner of
the game is the player who has the most stones in his big pit.