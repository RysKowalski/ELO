import json
from players_manager import PlayerInfo


class SaveManager:
    @staticmethod
    def load(path: str) -> dict[str, PlayerInfo]:
        with open(path, "r") as file:
            save: dict = json.load(file)

        return save

    @staticmethod
    def save(save: dict[str, PlayerInfo], path: str) -> None:
        data: dict = {"version": 2, "data": save}
        with open(path, "w") as file:
            json.dump(data, file)
