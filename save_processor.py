import json
from typing import TypeAlias, TypedDict, cast


class PlayerInfo(TypedDict):
    elo: float
    total_games: int
    wins: int
    loses: int


LegacyData: TypeAlias = dict[str, float]
CurrentData: TypeAlias = dict[str, PlayerInfo]
SaveData: TypeAlias = LegacyData | CurrentData


class SaveManager:
    def load(self, path: str) -> dict[str, PlayerInfo]:
        with open(path, "r") as file:
            save: dict = json.load(file)

        if not save:
            return {}

        if save.get("version") is None:
            data: dict[str, PlayerInfo] = self._no_version(save)
            self.save(data, path)
            return data
        return save["data"]

    def _no_version(
        self,
        data: SaveData,
    ) -> CurrentData:
        if not data:
            return {}

        first_value: float | PlayerInfo = next(iter(data.values()))

        if isinstance(first_value, float):
            legacy_data: LegacyData = cast(LegacyData, data)

            return {
                user: {
                    "elo": elo,
                    "total_games": 0,
                    "wins": 0,
                    "loses": 0,
                }
                for user, elo in legacy_data.items()
            }

        return cast(CurrentData, data)

    @staticmethod
    def save(save: dict[str, PlayerInfo], path: str) -> None:
        data: dict = {"version": 2, "data": save}
        with open(path, "w") as file:
            json.dump(data, file)
