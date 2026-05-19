from collections import defaultdict
from typing import TypedDict
from elo_calc import EloCalc
import json


class Difference(TypedDict):
    player1: str
    player2: str


class PlayerInfo(TypedDict):
    elo: float
    total_games: int
    wins: int
    loses: int


class PlayerMaganer:
    def __init__(self) -> None:
        self.players: defaultdict[str, PlayerInfo] = defaultdict(
            lambda: {"elo": 500, "total_games": 0, "wins": 0, "loses": 0}
        )
        self.eloCalc: EloCalc = EloCalc()

    def game(self, player1: str, player2: str, result: float) -> Difference:
        self.players[player1]["total_games"] += 1
        self.players[player2]["total_games"] += 1
        if result > 0.5:
            self.players[player1]["wins"] += 1
            self.players[player2]["loses"] += 1
        elif result < 0.5:
            self.players[player1]["loses"] += 1
            self.players[player2]["wins"] += 1

        r1: float = self.players[player1]["elo"]
        r2: float = self.players[player2]["elo"]

        newR1, newR2 = self.eloCalc.calculate_elo(r1, r2, result)

        self.players[player1]["elo"] = newR1
        self.players[player2]["elo"] = newR2

        return self._format_difference(r1 - newR1, r2 - newR2)

    def _format_difference(self, p1: float, p2: float) -> Difference:
        diff1: str = ""
        diff2: str = ""

        if p1 > 0:
            diff1 += "+"

        if p2 > 0:
            diff2 += "+"

        diff1 += str(round(p1))
        diff2 += str(round(p2))

        return {"player1": diff1, "player2": diff2}

    def save(self, path: str) -> None:
        with open(path, "w") as file:
            json.dump(self.players, file)

    def load(self, path: str) -> None:
        try:
            self._load(path)
        except FileNotFoundError:
            with open(path, "w") as file:
                file.write("{}")
            self._load(path)
        except json.JSONDecodeError:
            raise Exception(f"error reading file {path}")

    def _load(self, path: str) -> None:
        with open(path, "r") as file:
            self.players = defaultdict(self.players.default_factory, json.load(file))

    def get_players(self) -> dict[str, PlayerInfo]:
        ret: dict[str, PlayerInfo] = {}
        for p in self.players:
            ret[p] = {
                "elo": round(self.players[p]["elo"]),
                "total_games": self.players[p]["total_games"],
                "wins": self.players[p]["wins"],
                "loses": self.players[p]["loses"],
            }
        return ret


if __name__ == "__main__":
    pm: PlayerMaganer = PlayerMaganer()
    pm.game("p1", "p2", 1)
    pm.game("p1", "p3", 1)
    pm.save("save.json")
    print(pm.players["p1"], pm.players["p2"], pm.players["p3"])

    pm = PlayerMaganer()
    print(pm.players["p1"], pm.players["p2"], pm.players["p3"])

    pm.load("save.json")
    print(pm.players["p1"], pm.players["p2"], pm.players["p3"])
