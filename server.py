from fastapi import FastAPI
from starlette.responses import FileResponse

from players_manager import Difference, PlayerMaganer

app: FastAPI = FastAPI()

pm: PlayerMaganer = PlayerMaganer()
pm.load("save.json")


@app.get("/")
def root() -> FileResponse:
    return FileResponse("index.html")


@app.get("/api/get_players")
def get_players() -> dict[str, float]:
    return pm.get_players()


@app.post("/api/game")
def game(player1: str, player2: str, result: float) -> Difference:
    diff: Difference = pm.game(player1, player2, result)
    pm.save("save.json")
    return diff


def run():
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG

    LOGGING_CONFIG["formatters"]["default"]["fmt"] = (
        "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    )
    PORT: int = 3000
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    run()
