import json
import os

SAVE_FILE = "savegame.json"


def save_game(player, terrain):
    data = {
        "player": {
            "x": player.rect.x,
            "y": player.rect.y,
            "vel_x": player.vel_x,
            "vel_y": player.vel_y
        },
        "terrain": terrain
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file)


def load_game(player, terrain):
    if not os.path.exists(SAVE_FILE):
        return False

    with open(SAVE_FILE, "r") as file:
        data = json.load(file)
        player.rect.x = data["player"]["x"]
        player.rect.y = data["player"]["y"]
        player.vel_x = data["player"]["vel_x"]
        player.vel_y = data["player"]["vel_y"]
        for row in range(len(terrain)):
            for col in range(len(terrain[row])):
                terrain[row][col] = data["terrain"][row][col]
    return True