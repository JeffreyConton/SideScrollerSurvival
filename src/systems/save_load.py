import json
import os

SAVE_FILE = "savegame.json"

def save_game(player, terrain):
    game_state = {
        "player": {
            "x": player.rect.x,
            "y": player.rect.y
        },
        "terrain": terrain
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(game_state, f)

def load_game(player, terrain):
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            game_state = json.load(f)
            player.rect.x = game_state["player"]["x"]
            player.rect.y = game_state["player"]["y"]
            terrain[:] = game_state["terrain"]