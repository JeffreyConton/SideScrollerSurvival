import json
import os

SAVE_FILE = "savegame.json"


def save_game(player, terrain, time_system):
    data = {
        "player": {
            "x": player.rect.x,
            "y": player.rect.y,
            "vel_x": player.vel_x,
            "vel_y": player.vel_y
        },
        "terrain": terrain,
        "time_system": time_system.save_time()
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file)


def load_game(player, terrain, time_system):
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

        time_system.load_time(data["time_system"])
    return True